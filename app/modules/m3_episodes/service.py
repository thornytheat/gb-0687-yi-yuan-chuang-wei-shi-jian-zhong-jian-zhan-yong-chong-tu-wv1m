from .rules import episodes
def execute(ctx):
    rows,bad,intervals=episodes(ctx['records'],ctx['observation_end']);ctx['records']=rows;ctx['quarantine'].extend(bad);ctx['intervals']=intervals
    ctx['stages'].append({'title':'占床分段','rows':intervals,'metrics':{'住院段':len(intervals),'开放段':sum(x['open'] for x in intervals),'采信事件':len(rows)}})
    return ctx
