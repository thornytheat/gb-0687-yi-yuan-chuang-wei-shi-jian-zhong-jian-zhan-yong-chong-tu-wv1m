from app.normalize import instant,number
from app.errors import DomainError
WARD={'W1':'一病区','一病区':'一病区','W2':'二病区','二病区':'二病区'}
BEDS={**{f'{i:03d}':'一病区' for i in range(1,5)},**{f'{i:03d}':'二病区' for i in range(101,105)}}
def normalize(row):
    out=dict(row);ward=WARD.get(row['ward'])
    if ward is None or BEDS.get(row['bed'])!=ward: raise DomainError('UNMAPPED','床号与病区不匹配')
    out['ward']=ward;out['time']=instant(row['time'])
    version=number(row['version'])
    if version<1 or version!=version.to_integral(): raise DomainError('RANGE','版本无效')
    out['version']=int(version)
    if out['type'] not in ('admit','transfer','discharge'): raise DomainError('STATE','未知事件类型')
    return out
