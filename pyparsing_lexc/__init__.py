"""Parse lexc using pyparsing."""

import pyparsing as pp

# define punctuation and special words
COLON,SEMI = map(pp.Suppress, ":;")
HASH = pp.Literal('#')
LEXICON, END = map(pp.Keyword, "LEXICON END".split())

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

# use a parse action to normalize the parsed values
def fixup_value(tokens):
    if 'value' in tokens[0]:
        # pyparsing makes this a nested element, just take zero'th value
        if isinstance(tokens[0].value, pp.ParseResults):
            tokens[0]['value'] = tokens[0].value[0]
    else:
        # no value was given, expand 'name' as if  parsed 'name:name'
        tokens[0]['value'] = tokens[0].name
lexicon_decl.setParseAction(fixup_value)

# define a whole LEXICON section
# TBD - make name optional, define as 'Root'
lexicon_section = pp.Group(LEXICON
                        + ident("name")
                        + pp.ZeroOrMore(lexicon_decl, stopOn=LEXICON | END)("declarations"))

# this part still TBD - just put in a placeholder for now
multichar_symbols_section = pp.empty()

# tie it all together
parser = (pp.Optional(multichar_symbols_section)('multichar_symbols')
          + pp.Group(pp.OneOrMore(lexicon_section))('lexicons')
          + END)

# ignore comments anywhere in our parser
comment = '!' + pp.Optional(pp.restOfLine)
parser.ignore(comment)

if __name__ == '__main__':
    with open('../toyLEXICON.lexc') as toyLEXICONFile:
        lex_str = toyLEXICONFile.read()
        result = lexicon_section.parseString(lex_str)
        print(result.dump())
