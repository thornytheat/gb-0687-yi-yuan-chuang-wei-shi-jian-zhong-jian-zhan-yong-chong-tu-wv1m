from app.pipeline import run
from app.normalize import instant
from app.modules.m3_episodes.rules import episodes
def e(id,t,kind='admit',bed='001',version=1,patient='P'):
 return dict(id=id,time=instant('2026-11-16T'+t+':00+08:00'),type=kind,bed=bed,ward='一病区',version=version,patient=patient,_line=int(id)+1)
END=instant('2026-11-17T00:00:00+08:00')

def test_transfer_split():
    good,bad,parts=episodes([e('1','08:00'),e('2','10:00','transfer','002'),e('3','12:00','discharge','002')],END)
    assert len(parts)==2 and parts[0]['end']==parts[1]['start'] and len(good)==3

def test_orphan_discharge():
    good,bad,parts=episodes([e('1','08:00','discharge')],END)
    assert good==[] and bad[0]['code']=='ORPHAN'

def test_same_version_conflict():
    # TRAP-14
    good,bad,parts=episodes([e('1','08:00'),e('1','09:00')],END)
    assert good==[] and len(bad)==2

def test_open_interval():
    assert episodes([e('1','08:00')],END)[2][0]['open'] is True

def test_real_parts(raw):
    assert len(run(raw,stop=3,persist=False)['intervals'])>=20

def test_real_event_conservation(raw):
    x=run(raw,stop=3,persist=False);assert len(x['records'])+len(x['quarantine'])==47

def test_real_conflict_quarantine(raw):
    assert sum(q['code']=='CONFLICT' for q in run(raw,stop=3,persist=False)['quarantine'])==2

