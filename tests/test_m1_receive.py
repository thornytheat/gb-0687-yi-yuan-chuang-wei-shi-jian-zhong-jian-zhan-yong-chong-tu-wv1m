import pytest
from app.pipeline import run
from app.modules.m1_receive.rules import receive
from app.errors import DomainError
from app.config import SAMPLES

def test_bom_header(raw):
    # TRAP-02
    assert receive(raw)['records'][0]['id']=='00001'

def test_real_count(raw):
    assert receive(raw)['input_count']==47

def test_real_bad_width(raw):
    # TRAP-05
    assert any(q['code']=='COLUMN_COUNT' for q in receive(raw)['quarantine'])

def test_legacy_encoding():
    assert receive((SAMPLES/'legacy.csv').read_bytes())['encoding']=='gb18030'

def test_empty():
    with pytest.raises(DomainError):receive(b'')

def test_blank():
    with pytest.raises(DomainError,match='仅含空行'):receive(b'  \n')

def test_key_preserved(raw):
    # TRAP-08
    assert receive(raw)['records'][0]['patient']=='00001'

