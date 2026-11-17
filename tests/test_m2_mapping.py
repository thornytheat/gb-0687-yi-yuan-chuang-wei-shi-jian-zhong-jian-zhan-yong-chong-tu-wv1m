import pytest
from app.pipeline import run
from app.modules.m2_mapping.rules import normalize
from app.normalize import instant
from app.errors import DomainError
def row(**kw):
 x=dict(id='1',patient='01',bed='001',ward='W1',time='2026-11-16T08:00:00+08:00',type='admit',version='1');x.update(kw);return x

def test_timezone_equivalence():
    # TRAP-11
    assert normalize(row())['time']==instant('2026-11-16T00:00:00Z')

def test_wrong_ward():
    with pytest.raises(DomainError):normalize(row(ward='W2'))

def test_missing_offset():
    with pytest.raises(DomainError):normalize(row(time='2026-11-16T00:00:00'))

def test_zero_bed():
    assert normalize(row())['bed']=='001'

def test_real_alias(raw):
    assert run(raw,stop=2,persist=False)['records'][0]['ward']=='一病区'

def test_real_mapping_isolation(raw):
    assert any(q['code']=='UNMAPPED' for q in run(raw,stop=2,persist=False)['quarantine'])

def test_real_times_utc(raw):
    assert all(x['time'].endswith('+00:00') for x in run(raw,stop=2,persist=False)['records'])

