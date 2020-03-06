import os

import pyparsing_lexc as pplexc

ex1_name = os.path.join(os.path.dirname(__file__), 'resources', 'ex1.lexc')
with open(ex1_name) as f:
    ex1 = f.read()
ex2_name = os.path.join(os.path.dirname(__file__), 'resources', 'ex2.lexc')
with open(ex2_name) as f:
    ex2 = f.read()


def test_ex1():
    parsed1 = pplexc.lexc.parser(ex1)
    assert parsed1 == []
