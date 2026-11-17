from datetime import timedelta,timezone,datetime
from decimal import Decimal as D
from collections import defaultdict
def calendar(intervals):
    buckets=defaultdict(lambda:D(0));zone=timezone(timedelta(hours=8))
    for item in intervals:
        cursor=item['start'];end=item['end']
        while cursor<end:
            local=cursor.astimezone(zone);midnight=datetime.combine(local.date()+timedelta(days=1),datetime.min.time(),zone)
            stop=min(end,midnight)
            buckets[(local.date().isoformat(),item['ward'],item['bed'])]+=D(str((stop-cursor).total_seconds()))/60
            cursor=stop
    return [{'date':key[0],'ward':key[1],'bed':key[2],'minutes':value,'state':'超占' if value>1440 else '通过'} for key,value in sorted(buckets.items())]
