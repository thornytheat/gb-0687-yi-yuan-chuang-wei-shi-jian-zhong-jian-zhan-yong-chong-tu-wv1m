from app.errors import DomainError
from decimal import Decimal as D
from datetime import timedelta
import hashlib,json
from app.normalize import serial
def replay_audit(rows,bad,total,late_minutes):
    if len(rows)+len(bad)!=total: raise DomainError('INCOMPLETE','事件行数不平衡')
    watermark=None;late=[]
    for row in sorted(rows,key=lambda r:r['_line']):
        if watermark is not None and row['time']<watermark-timedelta(minutes=float(late_minutes)):
            late.append({'id':row['id'],'patient':row['patient'],'time':row['time'],'late_minutes':D(str((watermark-row['time']).total_seconds()))/60,'state':'已重算'})
        watermark=max(watermark,row['time']) if watermark else row['time']
    return {'watermark':watermark,'late':late,'fingerprint':hashlib.sha256(json.dumps(serial(sorted(rows,key=lambda r:r['id'])),sort_keys=True).encode()).hexdigest()}
