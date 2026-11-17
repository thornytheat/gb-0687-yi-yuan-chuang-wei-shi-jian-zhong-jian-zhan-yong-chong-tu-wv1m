from .rules import calendar
def execute(ctx):
    rows=calendar(ctx['intervals']);ctx['calendar']=rows
    ctx['stages'].append({'title':'日占床','rows':rows,'metrics':{'床日桶':len(rows),'总占床 min':str(sum((x['minutes'] for x in rows),0)),'超占桶':sum(x['state']=='超占' for x in rows)}})
    return ctx
