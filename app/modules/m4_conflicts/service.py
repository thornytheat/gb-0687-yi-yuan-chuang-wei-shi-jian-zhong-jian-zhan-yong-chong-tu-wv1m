from .rules import conflicts
def execute(ctx):
    rows=conflicts(ctx['intervals']);ctx['conflicts']=rows
    ctx['stages'].append({'title':'双占裁决','rows':rows,'metrics':{'冲突段':len(rows),'涉床':len({x['bed'] for x in rows}),'双占 min':str(sum((x['minutes'] for x in rows),0))}})
    return ctx
