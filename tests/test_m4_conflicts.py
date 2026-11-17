from app.pipeline import run
from app.normalize import instant
from app.modules.m4_conflicts.rules import conflicts
def part(patient,start,end,bed='001'):
 return dict(patient=patient,bed=bed,start=instant('2026-11-16T'+start+':00Z'),end=instant('2026-11-16T'+end+':00Z'))

def test_touching_not_overlap():
    # TRAP-23
    assert conflicts([part('A','08:00','09:00'),part('B','09:00','10:00')])==[]

def test_overlap_minutes():
    x=conflicts([part('A','08:00','10:00'),part('B','09:30','11:00')]);assert x[0]['minutes']==30

def test_different_beds():
    assert conflicts([part('A','08:00','10:00'),part('B','08:00','10:00','002')])==[]

def test_same_patient_no_double():
    assert conflicts([part('A','08:00','10:00'),part('A','08:00','10:00')])==[]

def test_real_overlap_present(raw):
    assert len(run(raw,stop=4,persist=False)['conflicts'])>0

def test_real_overlap_positive(raw):
    assert all(float(x['minutes'])>0 for x in run(raw,stop=4,persist=False)['conflicts'])

def test_real_bed_source(raw):
    x=run(raw,stop=4,persist=False);assert set(r['bed'] for r in x['conflicts'])<=set(r['bed'] for r in x['intervals'])

