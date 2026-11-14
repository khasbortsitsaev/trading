"""Official public Bitstamp daily history collector; no credentials/private APIs."""
from datetime import datetime, timezone
from decimal import Decimal as D
import hashlib
import json
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from .core import audit_candles, DataError, HoldoutAccessError

DAY = 86400000


def bitstamp_rows(payload, expected_pair):
    try:
        data=payload['data']
        pair=data.get('market',data.get('pair'))
        if pair.replace('/','').lower()!=expected_pair.lower():
            raise DataError('Unexpected source pair')
        rows=[]
        for x in data['ohlc']:
            t=D(x['timestamp'])
            if not t.is_finite() or t!=t.to_integral_value():
                raise DataError('Invalid source timestamp')
            rows.append([int(t)*1000,x['open'],x['high'],x['low'],x['close'],x['volume']])
        return rows
    except (KeyError,TypeError,AttributeError) as e:
        raise DataError('Invalid source response, not a candle page') from e


def collect_bitstamp(output, start_ms, end_ms, holdout_start_ms):
    output=Path(output).resolve()
    checkout=Path(__file__).resolve().parents[2]
    if output==checkout or checkout in output.parents:
        raise ValueError('Keep raw source data outside the public Git checkout')
    if start_ms%DAY or end_ms%DAY or not start_ms<end_ms<=holdout_start_ms:
        raise HoldoutAccessError('Invalid development request or holdout overlap')
    output.mkdir(parents=True,exist_ok=True)
    manifest={'provider':'Bitstamp public OHLC API','quote':'USD',
              'source_url':'https://www.bitstamp.net/api/','start_ms':start_ms,'end_exclusive_ms':end_ms,
              'holdout_start_ms':holdout_start_ms,'raw_redistribution_claimed':False,
              'use_scope':'Private research via supported public API; no raw dataset redistribution or exchange-fill replication',
              'markets':{},'requests':[]}
    normalized={}
    for asset,pair in [('BTC','btcusd'),('ETH','ethusd')]:
        pages=[];cursor=end_ms;page=0
        while cursor>start_ms:
            lower=max(start_ms,cursor-1000*DAY)
            count=(cursor-lower)//DAY
            # Official docs: end wins if both start/end are sent. Use end only,
            # inclusive to the final second before the desired half-open boundary.
            query=urlencode({'step':86400,'limit':count,'end':cursor//1000-1,
                             'exclude_current_candle':'true'})
            url=f'https://www.bitstamp.net/api/v2/ohlc/{pair}/?{query}'
            page+=1;path=output/f'{pair}-{page}.json'
            request=Request(url,headers={'User-Agent':'trading-research-quality-audit/1.0'})
            with urlopen(request,timeout=30) as response:
                if response.status!=200:
                    raise DataError('Non-successful source response')
                body=response.read(4*1024*1024+1)
                if len(body)>4*1024*1024:
                    raise DataError('Unexpectedly large candle response')
            if path.exists() and path.read_bytes()!=body:
                raise DataError('Refusing to overwrite a changed captured response; choose a new output directory')
            path.write_bytes(body)
            rows=bitstamp_rows(json.loads(body),pair)
            # Reject a server that ignores the historical boundary before use.
            audit_candles([rows],lower,cursor,holdout_start_ms=holdout_start_ms)
            pages.append(rows)
            manifest['requests'].append({'asset':asset,'url':url,'http_status':200,
                'observed_at_utc':datetime.now(timezone.utc).isoformat(),
                'raw_file':path.name,'sha256':hashlib.sha256(body).hexdigest(),
                'requested_start_ms':lower,'requested_end_exclusive_ms':cursor,'returned_rows':len(rows)})
            cursor=lower
        bars,quality=audit_candles(pages,start_ms,end_ms,holdout_start_ms=holdout_start_ms)
        manifest['markets'][asset]=quality
        normalized[asset]=[[x.timestamp_ms,str(x.open),str(x.high),str(x.low),str(x.close),str(x.volume)] for x in bars]
    normalized_body=(json.dumps(normalized,sort_keys=True,separators=(',',':'))+'\n').encode()
    (output/'normalized.json').write_bytes(normalized_body)
    manifest['normalized_sha256']=hashlib.sha256(normalized_body).hexdigest()
    manifest['complete']=all(x['missing_count']==0 for x in manifest['markets'].values())
    (output/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    return manifest


def load_panel(path, expected_sha256, holdout_start_ms, interval_ms=DAY):
    path=Path(path)
    raw=path.read_bytes()
    if hashlib.sha256(raw).hexdigest()!=expected_sha256:
        raise DataError('Dataset hash does not match the admitted manifest')
    data=json.loads(raw);panel={}
    for asset,rows in data.items():
        if not rows:
            raise DataError('Empty asset history')
        timestamps=[int(x[0]) for x in rows]
        bars,quality=audit_candles([rows],min(timestamps),max(timestamps)+interval_ms,interval_ms=interval_ms,
                                  holdout_start_ms=holdout_start_ms)
        if quality['missing_count']:
            raise DataError('Incomplete candle panel; no automatic forward fill')
        panel[asset]=bars
    if not panel:
        raise DataError('Empty panel')
    return panel


def load_admitted_dataset(root, admission, holdout_start_ms, interval_ms=DAY):
    """Bind provider/quote/quality metadata as well as normalized price bytes."""
    root=Path(root)
    raw=(root/'manifest.json').read_bytes()
    if hashlib.sha256(raw).hexdigest()!=admission['manifest_sha256']:
        raise DataError('Source manifest changed after admission')
    manifest=json.loads(raw)
    if (not manifest['complete'] or manifest['provider']!=admission['source']
            or manifest['quote']!=admission['quote']
            or (interval_ms != DAY and manifest.get('interval_ms') != interval_ms)
            or manifest['normalized_sha256']!=admission['normalized_sha256']):
        raise DataError('Admitted provider, quote, quality or dataset identity mismatch')
    return load_panel(root/'normalized.json',admission['normalized_sha256'],holdout_start_ms,interval_ms),manifest
