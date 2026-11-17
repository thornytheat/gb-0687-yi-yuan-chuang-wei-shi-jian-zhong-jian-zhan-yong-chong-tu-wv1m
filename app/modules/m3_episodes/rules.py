from collections import defaultdict
from datetime import timedelta
from app.reasons import rejected
def episodes(rows,end):
    groups=defaultdict(list);bad=[];retained=[];intervals=[]
    keys=defaultdict(list)
    for row in rows: keys[row['id']].append(row)
    for key,group in sorted(keys.items()):
        version=max(x['version'] for x in group);latest=[x for x in group if x['version']==version]
        sig=lambda x:(x['patient'],x['bed'],x['ward'],x['time'],x['type'])
        if len({sig(x) for x in latest})>1:bad.extend(rejected(x,'CONFLICT','同版事件矛盾') for x in group);continue
        chosen=min(latest,key=lambda x:x['_line']);groups[chosen['patient']].append(chosen)
        bad.extend(rejected(x,'DUPLICATE','重复或旧版事件') for x in group if x is not chosen)
    for patient,events in sorted(groups.items()):
        active=None
        for row in sorted(events,key=lambda x:(x['time'],{'discharge':0,'transfer':1,'admit':2}[x['type']],x['id'])):
            action=row['type']
            if action=='admit':
                if active is not None:bad.append(rejected(row,'STATE','已有占床段'));continue
                active=row
            else:
                if active is None:bad.append(rejected(row,'ORPHAN','没有入院事件'));continue
                if action=='discharge' and row['bed']!=active['bed']:bad.append(rejected(row,'STATE','出院床号不符'));continue
                if row['time']>active['time']:
                    intervals.append({'patient':patient,'bed':active['bed'],'ward':active['ward'],'start':active['time'],'end':row['time'],'open':False,'source':active['id']})
                active=row if action=='transfer' else None
            retained.append(row)
        if active and end>active['time']:intervals.append({'patient':patient,'bed':active['bed'],'ward':active['ward'],'start':active['time'],'end':end,'open':True,'source':active['id']})
    return retained,bad,intervals
