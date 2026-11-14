"""Official public Bitstamp OHLC collector; no credentials/private APIs."""
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


def collect_bitstamp(output, start_ms, end_ms, holdout_start_ms, step_seconds=86400):
    """Collect the registered daily/15-minute grids with immutable page caching."""
    if type(step_seconds) is not int or step_seconds not in [900,86400]:
        raise ValueError('Only daily and 15-minute collection protocols are registered')
    interval_ms=step_seconds*1000
    output=Path(output).resolve()
    checkout=Path(__file__).resolve().parents[2]
    if output==checkout or checkout in output.parents:
        raise ValueError('Keep raw source data outside the public Git checkout')
    if start_ms%interval_ms or end_ms%interval_ms or not start_ms<end_ms<=holdout_start_ms:
        raise HoldoutAccessError('Invalid development request or holdout overlap')
    output.mkdir(parents=True,exist_ok=True)
    manifest={'provider':'Bitstamp public OHLC API','quote':'USD',
              'source_url':'https://www.bitstamp.net/api/','start_ms':start_ms,'end_exclusive_ms':end_ms,
              'interval_ms':interval_ms,
              'holdout_start_ms':holdout_start_ms,'raw_redistribution_claimed':False,
              'use_scope':'Private research via supported public API; no raw dataset redistribution or exchange-fill replication',
              'markets':{},'requests':[]}
    normalized={}
    for asset,pair in [('BTC','btcusd'),('ETH','ethusd')]:
        pages=[];cursor=end_ms;page=0
        while cursor>start_ms:
            lower=max(start_ms,cursor-1000*interval_ms)
            count=(cursor-lower)//interval_ms
            # Official docs: end wins if both start/end are sent. Use end only,
            # inclusive to the final second before the desired half-open boundary.
            query=urlencode({'step':step_seconds,'limit':count,'end':cursor//1000-1,
                             'exclude_current_candle':'true'})
            url=f'https://www.bitstamp.net/api/v2/ohlc/{pair}/?{query}'
            page+=1;path=output/f'{pair}-{page}.json'
            meta_path=path.with_suffix('.meta.json')
            if path.exists() or meta_path.exists():
                if not path.exists() or not meta_path.exists():
                    raise DataError('Incomplete cached page; retain it and use a new capture directory')
                body=path.read_bytes();record=json.loads(meta_path.read_text())
                if (record['url']!=url or record['sha256']!=hashlib.sha256(body).hexdigest()
                        or record['asset']!=asset or record['raw_file']!=path.name
                        or record['http_status']!=200
                        or record['requested_start_ms']!=lower or record['requested_end_exclusive_ms']!=cursor):
                    raise DataError('Cached page identity or bytes changed; no silent replacement')
            else:
                request=Request(url,headers={'User-Agent':'trading-research-quality-audit/1.0'})
                with urlopen(request,timeout=30) as response:
                    if response.status!=200:
                        raise DataError('Non-successful source response')
                    body=response.read(4*1024*1024+1)
                    if len(body)>4*1024*1024:
                        raise DataError('Unexpectedly large candle response')
                record={'asset':asset,'url':url,'http_status':200,
                        'observed_at_utc':datetime.now(timezone.utc).isoformat(),
                        'raw_file':path.name,'sha256':hashlib.sha256(body).hexdigest(),
                        'requested_start_ms':lower,'requested_end_exclusive_ms':cursor}
            rows=bitstamp_rows(json.loads(body),pair)
            # Reject a server that ignores the historical boundary before use.
            audit_candles([rows],lower,cursor,interval_ms=interval_ms,holdout_start_ms=holdout_start_ms)
            if record.get('returned_rows',len(rows))!=len(rows):
                raise DataError('Cached page row count changed')
            record['returned_rows']=len(rows)
            if not path.exists():
                path.write_bytes(body)
                meta_path.write_text(json.dumps(record,indent=2)+'\n')
            pages.append(rows)
            manifest['requests'].append(record)
            cursor=lower
        bars,quality=audit_candles(pages,start_ms,end_ms,interval_ms=interval_ms,holdout_start_ms=holdout_start_ms)
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
            or admission.get('interval_ms',interval_ms)!=interval_ms
            or manifest['normalized_sha256']!=admission['normalized_sha256']):
        raise DataError('Admitted provider, quote, quality or dataset identity mismatch')
    panel=load_panel(root/'normalized.json',admission['normalized_sha256'],holdout_start_ms,interval_ms)
    for key in ['start_ms','end_exclusive_ms']:
        if key in admission and admission[key]!=manifest.get(key):
            raise DataError('Admitted dataset window changed')
    if 'markets' in admission and set(panel)!=set(admission['markets']):
        raise DataError('Admitted dataset universe changed')
    if 'start_ms' in manifest and 'end_exclusive_ms' in manifest:
        start,end=manifest['start_ms'],manifest['end_exclusive_ms']
        if not start<end<=holdout_start_ms or start%interval_ms or end%interval_ms:
            raise HoldoutAccessError('Invalid manifest window or holdout overlap')
        if any(bs[0].timestamp_ms!=start or bs[-1].timestamp_ms!=end-interval_ms
               or len(bs)!=(end-start)//interval_ms for bs in panel.values()):
            raise DataError('Dataset does not cover the full declared window')
    return panel,manifest
