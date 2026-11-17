import pytest
from app.pipeline import run
from app.normalize import instant
from app.errors import DomainError
from app.modules.m7_replay.rules import replay_audit
def e(id,hour,line):return dict(id=id,patient='P',time=instant('2026-11-16T'+hour+':00:00Z'),_line=line)

def test_late_replayed():
    # TRAP-13
    x=replay_audit([e('1','09',2),e('2','08',3)],[],2,30);assert x['late'][0]['late_minutes']==60

def test_watermark_monotonic():
    x=replay_audit([e('1','09',2),e('2','08',3)],[],2,30);assert x['watermark']==instant('2026-11-16T09:00:00Z')

def test_row_balance_failure():
    with pytest.raises(DomainError):replay_audit([],[],1,30)

def test_optimistic_lock(client):
    # TRAP-26
    x=client.post('/api/runs',json={}).json;url='/api/review/'+x['manifest']['run_id'];body={'version':1,'decision':'通过'}
    assert client.post(url,json=body).status_code==200
    assert client.post(url,json=body).status_code==409

def test_real_late_present(raw):
    assert len(run(raw,persist=False)['audit']['late'])>0

def test_real_fingerprint_stable(raw):
    assert run(raw,persist=False)['audit']['fingerprint']==run(raw,persist=False)['audit']['fingerprint']

def test_real_replay_no_loss(raw):
    x=run(raw,persist=False);assert len(x['records'])+len(x['quarantine'])==47

