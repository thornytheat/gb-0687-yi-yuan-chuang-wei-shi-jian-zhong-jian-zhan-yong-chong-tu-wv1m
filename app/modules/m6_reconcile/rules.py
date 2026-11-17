from decimal import Decimal as D
from collections import defaultdict
from app.errors import DomainError
def reconcile(intervals,buckets):
    original=defaultdict(lambda:D(0));split=defaultdict(lambda:D(0))
    for row in intervals:original[row['ward']]+=D(str((row['end']-row['start']).total_seconds()))/60
    for row in buckets:split[row['ward']]+=row['minutes']
    return [{'ward':ward,'episode_minutes':original[ward],'calendar_minutes':split[ward],'delta':original[ward]-split[ward],'state':'通过' if original[ward]==split[ward] else '差异'} for ward in sorted(set(original)|set(split))]
