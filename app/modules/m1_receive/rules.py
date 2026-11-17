from app.normalize import rows_from
from app.reasons import rejected
def receive(raw):
    result=rows_from(raw,['id','patient','bed','ward','time','type','version'])
    good=[]
    for row in result['raw']:
        if not row['id'] or not row['patient']: result['quarantine'].append(rejected(row,'MISSING','事件号或患者号缺失'))
        else: good.append(row)
    result['records']=good
    return result
