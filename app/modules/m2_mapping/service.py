from .rules import normalize
from app.errors import DomainError
from app.reasons import rejected
from app.normalize import instant,number
def execute(ctx):
    end=instant(ctx['params']['observation_end']);offset=number(ctx['params']['day_offset']);late=number(ctx['params']['late_minutes'])
    if offset!=8 or late<0: raise DomainError('RANGE','日期偏移须为8，迟到阈值非负')
    good=[]
    for row in ctx['records']:
        try:
            item=normalize(row)
            if item['time']>end: raise DomainError('RANGE','事件晚于观测终点')
            good.append(item)
        except DomainError as exc:ctx['quarantine'].append(rejected(row,exc.code,exc.message))
    ctx['records']=good;ctx['observation_end']=end
    ctx['stages'].append({'title':'病区归一','rows':good,'metrics':{'床位':8,'有效事件':len(good),'日期偏移 h':8}})
    return ctx
