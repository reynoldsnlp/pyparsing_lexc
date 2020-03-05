import pyparsing_lexc as pplexc

from my_resources import ex1
from my_resources import ex2


def test_ex1():
    parsed1 = pplexc.lexc.parser(ex1)
    assert parsed1 == []
