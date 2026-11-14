"""Daily, long/flat, offline screening engine. All fills are candle proxies."""
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from decimal import Decimal as D, ROUND_CEILING, ROUND_DOWN
import math
import statistics

from .core import Candle, DataError, HoldoutAccessError, Portfolio, Rules, validate_weights

DAY = 86400000
UTC = timezone.utc


def dt(milliseconds):
    return datetime.fromtimestamp(milliseconds/1000, UTC)


@dataclass(frozen=True)
class Settings:
    initial_eth: D = D('.5')
    fee: D = D('.0005')
    friction_round_trip_bps: D = D('15')
    publication_minutes: int = 5
    processing_minutes: int = 5
    extra_delay_bars: int = 0
    quote: str = 'USDC'
    source: str = 'synthetic'
    rules: dict = field(default_factory=dict)

    def validate(self):
        if not self.initial_eth.is_finite() or self.initial_eth <= 0:
            raise ValueError('Invalid initial ETH')
        if not self.fee.is_finite() or not 0 <= self.fee < 1:
            raise ValueError('Invalid fee')
        if not self.friction_round_trip_bps.is_finite() or not 0 <= self.friction_round_trip_bps < 10000:
            raise ValueError('Invalid adverse friction')
        if self.publication_minutes < 0 or self.processing_minutes <= 0 or self.extra_delay_bars < 0:
            raise ValueError('Invalid latency')
        if self.quote not in ['USD','USDC']:
            raise ValueError('This runner requires an explicit USD/USDC quote')


def signals(histories, variant, old_state):
    lookback = int(variant['lookback_days'])
    if lookback < 1:
        raise ValueError('Lookback must be positive')
    state = {}
    for asset, history in histories.items():
        prices = [x.close for x in history]
        if variant['family'] == 'trend':
            state[asset] = len(prices)>lookback and prices[-1]>prices[-1-lookback]
        elif variant['family'] == 'volume_confirmed_trend':
            volume_days = int(variant['volume_lookback_days'])
            multiplier = D(variant['volume_multiplier'])
            if volume_days < 1 or not multiplier.is_finite() or multiplier <= 0:
                raise ValueError('Invalid volume confirmation parameters')
            if len(history) < max(lookback, volume_days) + 1:
                raise DataError('Insufficient volume/trend warmup')
            volumes = [bar.volume for bar in history[-volume_days-1:]]
            if any(not v.is_finite() or v < 0 for v in volumes):
                raise DataError('Invalid volume')
            trend = prices[-1] > prices[-1-lookback]
            mean_volume = sum(volumes[:-1], D(0)) / volume_days
            confirmation = mean_volume > 0 and volumes[-1] > multiplier * mean_volume
            state[asset] = trend and (bool(old_state.get(asset, False)) or confirmation)
        elif variant['family'] == 'reversal':
            if lookback < 2:
                raise ValueError('Reversal requires at least two observations')
            if len(prices)<lookback:
                state[asset] = False
                continue
            logs = [math.log(float(p)) for p in prices[-lookback:]]
            deviation = statistics.stdev(logs)
            if deviation == 0:
                state[asset] = False
                continue
            z = (logs[-1]-statistics.mean(logs))/deviation
            state[asset] = (False if z>=0 else True if z<=-float(variant['entry_z'])
                            else bool(old_state.get(asset,False)))
        else:
            raise ValueError('Unregistered signal family')
    return state


def quantity_floor(quantity, rules):
    return quantity.quantize(D(1).scaleb(-rules.quantity_decimals),rounding=ROUND_DOWN)


def adverse_price(price, side, slip, rules):
    raw = price * (1+slip if side=='buy' else 1-slip)
    return (raw/rules.tick).to_integral_value(rounding=ROUND_CEILING if side=='buy' else ROUND_DOWN)*rules.tick


def target_quantities(portfolio, prices, active, settings):
    weight = D(1)/len(prices)
    assets=sorted(prices)
    weights={a:(weight if active[a] else D(0)) for a in assets[:-1]}
    weights[assets[-1]]=(1-weight*(len(assets)-1)) if active[assets[-1]] else D(0)
    weights=validate_weights(weights)
    equity = portfolio.equity(prices)
    slip = settings.friction_round_trip_bps/D(20000)
    return {a:quantity_floor(equity*weights[a]/(prices[a]*(1+slip)*(1+settings.fee)),
                            settings.rules.get(a,Rules())) for a in prices}


def execute_targets(portfolio, target, prices, at_ms, settings, rejected, tradable=None):
    slip = settings.friction_round_trip_bps/D(20000)
    for side in ['sell','buy']:
        for asset in sorted(prices):
            rule = settings.rules.get(asset,Rules())
            difference = target['quantities'][asset]-portfolio.inventory.get(asset,D(0))
            if (side=='buy' and difference<=0) or (side=='sell' and difference>=0):
                continue
            price = adverse_price(prices[asset],side,slip,rule)
            requested = quantity_floor(abs(difference),rule)
            quantity = requested
            if side=='buy':
                quantity = min(quantity,quantity_floor(portfolio.cash/(price*(1+settings.fee)),rule))
            if quantity<=0 or quantity<rule.minimum_base or quantity*price<rule.minimum_quote:
                rejected.append({'asset':asset,'at_ms':at_ms,'reason':'cash_rounding_or_minimum','requested':str(requested)})
                continue
            if tradable is not None and not tradable.get(asset,True):
                rejected.append({'asset':asset,'at_ms':at_ms,'reason':'market_unavailable','requested':str(requested)})
                continue
            event = portfolio.fill(asset,side,quantity,price,settings.fee,rule,
                                   available_at=target['available_at'],decision_at=target['decision_at'],
                                   ready_at=target['ready_at'],fill_at=dt(at_ms))
            event.update({'source_close_ms':target['source_close_ms'],
                          'available_at':target['available_at'].isoformat(),
                          'decision_at':target['decision_at'].isoformat(),
                          'ready_at':target['ready_at'].isoformat(),
                          'reference_price':str(prices[asset]),'requested_quantity':str(requested),
                          'cash_resized':quantity<requested,
                          'adverse_price_cost':str(quantity*abs(price-prices[asset])),
                          'fill_model':'future_daily_open_proxy_not_observed_fill'})


def metrics(values, initial, elapsed_days):
    floats = [float(x) for x in [initial,*values]]
    if not values or elapsed_days<=0 or any(not math.isfinite(x) or x<=0 for x in floats):
        raise DataError('Invalid equity series')
    returns = [b/a-1 for a,b in zip(floats,floats[1:])]
    peak, drawdown = floats[0], 0.0
    for x in floats[1:]:
        peak=max(peak,x);drawdown=max(drawdown,1-x/peak)
    std=statistics.stdev(returns) if len(returns)>1 else 0
    try:
        cagr=math.expm1(math.log(floats[-1]/floats[0])*365.25/elapsed_days)
    except OverflowError:
        cagr=None
    return {'total_return':floats[-1]/floats[0]-1,
            'cagr':cagr,
            'maximum_drawdown':drawdown,
            'sharpe_zero_reference_365_days':statistics.mean(returns)/std*math.sqrt(365) if std else None}


def run(panel, variant, start_ms, end_ms, settings, *, holdout_start_ms, market_status=None):
    settings.validate()
    if not start_ms<end_ms<=holdout_start_ms or start_ms%DAY or end_ms%DAY:
        raise HoldoutAccessError('Invalid/aligned development window or holdout access')
    if 'ETH' not in panel or not panel:
        raise DataError('ETH price is required for the initial endowment/benchmark')
    indexed = {}
    for asset, bars in panel.items():
        if any(b.timestamp_ms>=holdout_start_ms for b in bars):
            raise HoldoutAccessError('Input includes final holdout data')
        for b in bars:
            prices=[b.open,b.high,b.low,b.close]
            if b.timestamp_ms%DAY or any(not p.is_finite() or p<=0 for p in prices) or not b.volume.is_finite() or b.volume<0 or not b.low<=min(b.open,b.close)<=max(b.open,b.close)<=b.high:
                raise DataError('Invalid incoming candle')
        index = {b.timestamp_ms:b for b in bars}
        if len(index)!=len(bars):
            raise DataError('Duplicate input timestamps')
        if any(t not in index for t in range(start_ms,end_ms,DAY)):
            raise DataError('Missing simulation day; no fill or valuation fabrication')
        indexed[asset]=index
    # Warmup is source data, never a funded simulation or a future feature.
    warmup = {a:sorted((b for b in bars if b.timestamp_ms<start_ms),key=lambda b:b.timestamp_ms)
              for a,bars in panel.items()}
    required = int(variant['lookback_days'])+(1 if variant['family']=='trend' else 0)
    if variant['family'] == 'volume_confirmed_trend':
        required = max(int(variant['lookback_days']), int(variant['volume_lookback_days'])) + 1
    for bars in warmup.values():
        if len(bars)<required or bars[-1].timestamp_ms!=start_ms-DAY:
            raise DataError('Insufficient or nonadjacent warmup')
        if any(y.timestamp_ms-x.timestamp_ms!=DAY for x,y in zip(bars,bars[1:])):
            raise DataError('Gap in warmup')
    opening = {a:index[start_ms].open for a,index in indexed.items()}
    initial = settings.initial_eth*opening['ETH']
    portfolio=Portfolio(inventory={'ETH':settings.initial_eth})
    eth_hold=settings.initial_eth
    slip=settings.friction_round_trip_bps/D(20000)
    # The cash benchmark conversion is predetermined, not derived from a future signal.
    cash_price=adverse_price(opening['ETH'],'sell',slip,settings.rules.get('ETH',Rules()))
    cash_hold=settings.initial_eth*cash_price*(1-settings.fee)
    curve=[]; decisions=[]; rejected=[]; pending={}; old_state={}
    histories={a:list(bars) for a,bars in warmup.items()}
    for t in range(start_ms,end_ms,DAY):
        opens={a:index[t].open for a,index in indexed.items()}
        due=pending.pop(t,None)
        if due is not None:
            execute_targets(portfolio,due,opens,t,settings,rejected,
                            (market_status or {}).get(t))
        # Only yesterday's completed closes enter the signal, after today's open fills.
        source_close=t
        available=dt(t)+timedelta(minutes=settings.publication_minutes)
        ready=available+timedelta(minutes=settings.processing_minutes)
        state=signals(histories,variant,old_state)
        references={a:bars[-1].close for a,bars in histories.items()}
        quantities=target_quantities(portfolio,references,state,settings)
        fill_day=ready.replace(hour=0,minute=0,second=0,microsecond=0)+timedelta(days=1+settings.extra_delay_bars)
        # Intents are timestamped target instructions, not resting venue orders.
        intent={'quantities':quantities,'source_close_ms':source_close,
                'available_at':available,'decision_at':available,'ready_at':ready,
                'fill_ms':int(fill_day.timestamp()*1000)}
        if intent['fill_ms'] in pending:
            raise DataError('Duplicate intent due day')
        pending[intent['fill_ms']]=intent
        decisions.append({'source_close_ms':t,'available_at':available.isoformat(),
                          'ready_at':ready.isoformat(),'fill_ms':intent['fill_ms'],
                          'active':state,'target_quantities':{a:str(q) for a,q in quantities.items()}})
        old_state=state
        closes={a:index[t].close for a,index in indexed.items()}
        equity=portfolio.equity(closes)
        if portfolio.cash<0 or any(x<0 for x in portfolio.inventory.values()):
            raise DataError('Negative spot balances')
        curve.append({'time_ms':t+DAY,'equity':str(equity),
                      'cash_benchmark':str(cash_hold),'eth_benchmark':str(eth_hold*closes['ETH']),
                      'eth_equivalent':str(equity/closes['ETH']),
                      'cash':str(portfolio.cash),'inventory':{a:str(q) for a,q in sorted(portfolio.inventory.items())}})
        for a in histories:histories[a].append(indexed[a][t])
    elapsed=(end_ms-start_ms)/DAY
    return {'evidence_type':'synthetic_software_check' if settings.source=='synthetic' else 'historical_source_proxy_not_venue_replication',
            'variant':variant,'source':settings.source,'quote':settings.quote,
            'usdc_wealth_claimed':settings.quote=='USDC',
            'execution_model':'fixed target quantities from prior available closes; future daily open proxy; quote fees; no EUR leg',
            'initial_eth':str(settings.initial_eth),'initial_quote_equity':str(initial),
            'settings':{'fee_per_execution':str(settings.fee),'noncommission_round_trip_bps':str(settings.friction_round_trip_bps),
                        'extra_delay_bars':settings.extra_delay_bars,
                        'publication_minutes':settings.publication_minutes,
                        'processing_minutes':settings.processing_minutes,
                        'rules':{a:{'quantity_decimals':r.quantity_decimals,'tick':str(r.tick),
                                    'minimum_base':str(r.minimum_base),'minimum_quote':str(r.minimum_quote)}
                                 for a,r in settings.rules.items()}},
            'start_ms':start_ms,'end_exclusive_ms':end_ms,
            'metrics':metrics([D(x['equity']) for x in curve],initial,elapsed),
            'eth_benchmark_metrics':metrics([D(x['eth_benchmark']) for x in curve],initial,elapsed),
            'cash_benchmark_metrics':metrics([D(x['cash_benchmark']) for x in curve],initial,elapsed),
            'commission_quote':str(sum((D(x['fee']) for x in portfolio.events),D(0))),
            'modeled_adverse_price_cost':str(sum((D(x['adverse_price_cost']) for x in portfolio.events),D(0))),
            'orders_executed':len(portfolio.events),'orders_rejected':len(rejected),
            'curve':curve,'fills':portfolio.events,'decisions':decisions,'rejections':rejected,
            'pending_intents_not_filled_at_end':len(pending)}
