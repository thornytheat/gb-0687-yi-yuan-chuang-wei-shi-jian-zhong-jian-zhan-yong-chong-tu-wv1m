from app.pipeline import run
from app.normalize import instant
from app.modules.m5_calendar.rules import calendar
def p(start,end):return dict(patient='A',ward='一病区',bed='001',start=instant(start),end=instant(end))

def test_midnight_split():
    x=calendar([p('2026-12-31T23:00:00+08:00','2027-01-01T01:00:00+08:00')]);assert [r['minutes'] for r in x]==[60,60]

def test_midnight_endpoint():
    x=calendar([p('2026-11-16T23:00:00+08:00','2026-11-17T00:00:00+08:00')]);assert len(x)==1 and x[0]['minutes']==60

def test_zero_interval():
    assert calendar([p('2026-11-16T00:00:00Z','2026-11-16T00:00:00Z')])==[]

def test_full_day():
    assert calendar([p('2026-11-16T00:00:00+08:00','2026-11-17T00:00:00+08:00')])[0]['minutes']==1440

def test_real_dates(raw):
    assert all(x['date'] in ['2026-11-16','2026-11-17'] for x in run(raw,stop=5,persist=False)['calendar'])

def test_real_positive_minutes(raw):
    assert all(float(x['minutes'])>0 for x in run(raw,stop=5,persist=False)['calendar'])

def test_real_calendar_present(raw):
    assert len(run(raw,stop=5,persist=False)['calendar'])>=8

