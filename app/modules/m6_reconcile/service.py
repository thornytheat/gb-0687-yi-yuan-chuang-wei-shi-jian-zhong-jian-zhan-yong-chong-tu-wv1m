from .rules import reconcile
def execute(ctx):
    rows=reconcile(ctx['intervals'],ctx['calendar']);ctx['reconciliation']=rows
    ctx['stages'].append({'title':'病区对账','rows':rows,'metrics':{'病区':len(rows),'守恒差 min':str(sum((x['delta'] for x in rows),0)),'待复核冲突':len(ctx['conflicts'])}})
    return ctx
