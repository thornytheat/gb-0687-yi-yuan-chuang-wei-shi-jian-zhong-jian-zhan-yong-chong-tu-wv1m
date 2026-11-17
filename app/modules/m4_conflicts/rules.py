from collections import defaultdict
from decimal import Decimal as D
def conflicts(intervals):
    beds=defaultdict(list)
    for item in intervals:beds[item['bed']].append(item)
    result=[]
    for bed,items in sorted(beds.items()):
        ordered=sorted(items,key=lambda x:(x['start'],x['end'],x['patient']))
        for i,left in enumerate(ordered):
            for right in ordered[i+1:]:
                if right['start']>=left['end']:break
                start=max(left['start'],right['start']);end=min(left['end'],right['end'])
                if start<end and left['patient']!=right['patient']:
                    result.append({'bed':bed,'patient':left['patient']+' / '+right['patient'],'start':start,'end':end,'minutes':D(str((end-start).total_seconds()))/60,'state':'双占'})
    return result
