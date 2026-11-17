from app.pipeline import run
from app.normalize import instant
from decimal import Decimal as D
from app.modules.m6_reconcile.rules import reconcile
def p():return dict(ward='一',start=instant('2026-11-16T00:00:00Z'),end=instant('2026-11-16T01:00:00Z'))

def test_duration_balance():
    assert reconcile([p()],[{'ward':'一','minutes':D(60)}])[0]['delta']==0

def test_missing_bucket():
    assert reconcile([p()],[])[0]['delta']==60

def test_unexpected_bucket():
    assert reconcile([],[{'ward':'二','minutes':D(30)}])[0]['delta']==-30

def test_empty():
    assert reconcile([],[])==[]

def test_real_ward_balance(raw):
    assert all(x['state']=='通过' for x in run(raw,stop=6,persist=False)['reconciliation'])

def test_real_two_wards(raw):
    assert len(run(raw,stop=6,persist=False)['reconciliation'])==2

def test_real_zero_delta(raw):
    assert sum(D(x['delta']) for x in run(raw,stop=6,persist=False)['reconciliation'])==0

