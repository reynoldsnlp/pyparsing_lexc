ex1 = """! Comments begin with !

! Multichar_Symbols (separated by whitespace, terminated by first declared LEXICON)
Multichar_Symbols +A +N +V  ! +A is adjectives, +N is nouns, +V is verbs
+Adv  ! This one is for adverbs
+Punc ! punctuation
! +Cmpar ! This is broken for now, so I commented it out.

! The bulk of lexc is made of up LEXICONs, which contain entries that point to
! other LEXICONs. "Root" is a reserved lexicon name, and the start state.
! "#" is also a reserved lexicon name, and the end state.

LEXICON Root  ! Root is a reserved lexicon name, if it is not declared, then the first LEXICON is assumed to be the root
big Adj ;  ! This 
bigly Adv ;  ! Not sure if this is a real word...
dog Noun ;
cat Noun ;
crow Noun ;
crow Verb ;
Num ;        ! This continuation class generates numbers using xfst-style regex

! NB all the following are reserved characters

sour% cream Noun ;  ! escaped space
%: Punctuation ;    ! escaped :
%; Punctuation ;    ! escaped ;
%# Punctuation ;    ! escaped #
%! Punctuation ;    ! escaped !
%% Punctuation ;    ! escaped %
%< Punctuation ;    ! escaped <
%> Punctuation ;    ! escaped >

%:%:%::%: # ; ! Should map ::: to :

LEXICON Adj
+A: # ;      ! # is a reserved lexicon name which means end-of-word (final state).
! +Cmpar:er # ;  ! Broken, so I commented it out.

LEXICON Adv
+Adv: # ;

LEXICON Noun
+N+Sg: # ;
+N+Pl:s # ;

LEXICON Num_start
<[0|1|2|3|4|5|6|7|8|9]> Num ; ! This is an xfst regular expression

LEXICON Num
<[0|1|2|3|4|5|6|7|8|9]> Num ; ! This is an xfst regular expression and a cyclic continuation
# ;

LEXICON Verb
+V+Inf: # ;
+V+Pres:s # ;

LEXICON Punctuation
+Punc: # ;

END

This text is ignored because it is after END"""


#==============================================================================
#==============================================================================
#==============================================================================
#==============================================================================


ex2 = """LEXICON Root  ! Root is a reserved lexicon name, if it is not declared, then the first LEXICON is assumed to be the root
! Each LEXICON contains at least one entry, which is minimally a continuation to
! a LEXICON, but usually also includes "data"
! A minimal entry is: continuation ;
big Adj ;           ! upper='big'           lower='big'         cc='Adj'
bigly Adv ;         ! upper='bigly'         lower='bigly'       cc='Adv'
dog Noun ;          ! upper='dog'           lower='dog'         cc='Noun'
crow Noun ;         ! upper='crow'          lower='crow'        cc='Noun'
crow Verb ;         ! upper='crow'          lower='crow'        cc='Verb'
Num ;               ! upper=''              lower=''            cc='Num'
<[1|2|3]+> Num ;    ! upper=Regex('[1|2|3]+') lower=Regex('[1|2|3]+') cc='Num'
be: Verb_be ;       ! upper='be'            lower=''            cc='Verb_be'
sour% cream Noun ;  ! upper='sour cream'    lower='sour cream'  cc='Noun'
%: Punctuation ;    ! upper=':'             lower=':'           cc='Punctuation'
%; Punctuation ;    ! upper=';'             lower=';'           cc='Punctuation'
%# Punctuation ;    ! upper='#'             lower='#'           cc='Punctuation'
%! Punctuation ;    ! upper='!'             lower='!'           cc='Punctuation'
%% Punctuation ;    ! upper='%'             lower='%'           cc='Punctuation'
%< Punctuation ;    ! upper='<'             lower='<'           cc='Punctuation'
%> Punctuation ;    ! upper='>'             lower='>'           cc='Punctuation'
%:%:%::%: # ;       ! upper=':::'           lower=':'           cc='#'
%%%%%::%# # ;       ! upper='%%:'           lower='#'           cc='#'

LEXICON Adj ;
+Adj: # ;

LEXICON Num
+Num: # ;           ! upper='+Num'          lower=''            cc='#'"""


#==============================================================================
#==============================================================================
#==============================================================================
#==============================================================================
