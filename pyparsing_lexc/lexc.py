"""Parse lexc using pyparsing.

Based on https://stackoverflow.com/a/42848414/2903532. The author of the
answer was not familiar with lexc, so some decisions may not be appropriate.
"""

import pyparsing as pp

# define punctuation and special words
COLON = pp.Suppress(':')
SEMI = pp.Suppress(';')
HASH = pp.Literal('#')
LEXICON = pp.Keyword('LEXICON')
END = pp.Keyword('END')

# use regex and Combine to handle % escapes
escaped_char = pp.Regex(r'%.').setParseAction(lambda t: t[0][1])
ident_lit_part = pp.Word(pp.printables, excludeChars=':%;')
xfst_regex = pp.Regex(r'<.*?>')
ident = pp.Combine(pp.OneOrMore(escaped_char | ident_lit_part | xfst_regex))
value_expr = ident()


# handle the following lexicon declarations:
#    name ;
#    name:value ;
#    name value ;
#    name value # ;
lexicon_decl = pp.Group(ident("name")
                        + pp.Optional(pp.Optional(COLON)
                                      + value_expr("value")
                                      + pp.Optional(HASH)('hash'))
                        + SEMI)


def fixup_value(tokens):
    """Use a parse action to normalize the parsed values."""
    if 'value' in tokens[0]:
        # pyparsing makes this a nested element, just take zero'th value
        if isinstance(tokens[0].value, pp.ParseResults):
            tokens[0]['value'] = tokens[0].value[0]
    else:
        # no value was given, expand 'name' as if  parsed 'name:name'
        tokens[0]['value'] = tokens[0].name


lexicon_decl.setParseAction(fixup_value)


# define a whole LEXICON section
# TODO make name optional, define as 'Root'
lexicon_section = pp.Group(LEXICON
                           + ident("name")
                           + pp.ZeroOrMore(lexicon_decl,
                                           stopOn=LEXICON | END)("declarations"))  # noqa: E501

# TODO just put in a placeholder for now
multichar_symbols_section = pp.empty()

# tie it all together
parser = (pp.Optional(multichar_symbols_section)('multichar_symbols')
          + pp.Group(pp.OneOrMore(lexicon_section))('lexicons')
          + END)


# ignore comments anywhere in our parser
comment = '!' + pp.Optional(pp.restOfLine)
parser.ignore(comment)
