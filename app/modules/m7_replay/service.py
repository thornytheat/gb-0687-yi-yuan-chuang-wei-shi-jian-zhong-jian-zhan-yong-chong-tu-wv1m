from .rules import replay_audit
from app.normalize import number
def execute(ctx):
    ctx['audit']=replay_audit(ctx['records'],ctx['quarantine'],ctx['input_count'],number(ctx['params']['late_minutes']))
    ctx['stages'].append({'title':'补传重算','rows':ctx['audit']['late'],'metrics':{'迟到事件':len(ctx['audit']['late']),'采信事件':len(ctx['records']),'水位':str(ctx['audit']['watermark'])}})
    return ctx
