"""Deterministic artificial fixtures, never financial evidence."""
from datetime import datetime,timezone
from decimal import Decimal as D
import random
from .core import Candle
from .engine import DAY


def panel(days=800, seed=20261113):
    rng=random.Random(seed)
    start=int(datetime(2020,1,1,tzinfo=timezone.utc).timestamp()*1000)
    result={}
    for asset,initial in [('BTC',D(1000)),('ETH',D(100))]:
        bars=[];previous=initial
        for i in range(days):
            opening=(previous*(1+D(rng.randint(-5,5))/10000)).quantize(D('.00000001'))
            drift=15 if (i//70)%2==0 else -15
            close=(opening*(1+D(drift+rng.randint(-40,40))/10000)).quantize(D('.00000001'))
            bars.append(Candle(start+i*DAY,opening,max(opening,close)*D('1.01'),
                               min(opening,close)*D('.99'),close,D(100+rng.randint(0,100))))
            previous=close
        result[asset]=bars
    return result
