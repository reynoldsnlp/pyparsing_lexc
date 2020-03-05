import sys

from .lexc import lexicon_section

result = lexicon_section.parseString(sys.stdin.read())
print(result.dump())
