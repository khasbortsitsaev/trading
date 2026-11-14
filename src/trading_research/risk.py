"""Conservative marked-equity envelopes, not reconstructed intraday paths."""
from decimal import Decimal as D
from .core import Candle


def equity_envelope(states: list[tuple[D, dict[str, D]]], candles: dict[str, Candle],
                    suspended: set[str]) -> tuple[D, D]:
    """Bound all balance states using daily lows/highs, allowing unknown ordering.

    Extrema across assets and balance states need not coincide. This deliberately
    loose bound includes intermediate rebalance states and modeled trading costs.
    A suspended holding has zero recovery in the lower envelope, not a fake fill.
    """
    lows, highs = [], []
    for cash, inventory in states:
        lows.append(cash + sum((q * (D(0) if a in suspended else candles[a].low)
                                for a, q in inventory.items() if q), D(0)))
        highs.append(cash + sum((q * candles[a].high
                                 for a, q in inventory.items() if q), D(0)))
    return min(lows), max(highs)


def drawdown_upper_bound(curve: list[dict], initial: D) -> float:
    """Worst compatible high-before-low ordering, including same-day ambiguity."""
    peak, drawdown = initial, D(0)
    for row in curve:
        peak = max(peak, D(row['equity_upper_bound']))
        drawdown = max(drawdown, 1 - D(row['equity_lower_bound']) / peak)
    return float(drawdown)
