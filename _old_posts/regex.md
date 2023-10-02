---
title: "Regex"
subtitle: "Cheatsheet"
tags: [tools, cheatsheet]

date: 2021-11-13
featured: false
draft: false

reading_time: true
profile: false
commentable: true
summary: " "

---

My regular expression cheatsheet, focused on the Python engine. A lot of
content is heavily based on (and often shamelessly copied from) the amazing
[RexEgg](https://www.rexegg.com) and
[Regular-Expressions.info](https://www.regular-expressions.info) sites.


## Basics

- A regex is a text string that a regex engine uses to find text or positions
  in a body of text, typically for the purposes of validating, finding,
  replacing, and splitting.

- To differentiate between the string that makes up the regex and the string
  that is being searched, the former is often called *regex* or *pattern* and
  the latter *string* or *subject*.

- A (lexical) token is a string with an assigned and thus identified meaning
  (more [here](https://en.wikipedia.org/wiki/Lexical_analysis#Token)). For
  instance, the token `\w` in a pattern stands for a word-character, and will
  be replaced by that when the engine parses the string.

- The Python regex engine (and all other modern engines) is regex-directed: it
  attempts all possible permutations of the regex at a character position of
  the subject before moving on to the next character (which can involve lots of
  backtracking). In contrast, text-directed engines visit each character in the
  subject text only once. This makes them faster but also less powerful.

- A regex engine is *eager*: it scans alternatives in the regex from left to
  right and returns the first possible match – `Jane|Janet` would return
  *Jane* as a match in *Janet is tall*.


## Characters

- There are four types of characters: literal characters (e.g. `a`),
  metacharacters (`^`), non-printable characters (`\n`), and shorthand
  character classes (`\w`).

- Literal characters simply match themselves: the single literal character `a`
  matches the first *a* in the string, the sequence of literal characters `cat`
  the first occurrence of *cat*.

- Metacharacters are the twelve punctuation characters from the ACSII
  [table](https://www.asciitable.com) that make regex work its magic: `$`, `(`,
  `)`, `*`, `+`, `.`, `?`, `[`, `\`, `^`, `{`, `|`. To match metacharacters as
  literals, escape them with a backslash, as in `1\+2=3`. Exceptions are `{`
  and `}`, which are only treated as metacharacters when part of a quantifier,
  and `]`, which only takes on special meaning when part of a character class).

- Non-printable characters or formation marks are characters used to tell word
  processors how text needs to look and do not appear in printed text.

- Shorthand character classes are tokens for certain common character classes.

Non-printable characters

| Character             | Legend |
| - | - |
| `\r`                  | Carriage return |
| `\n`                  | Newline |
| `\r\n`                | Line-break on Windows |
| `\t`                  | Tab |
| `\f`                  | Form-feed |

Shorthand character classes

| Character             | Legend |
| - | - |
| `\d`                  | Single digit, short for `[0-9]` |
| `\D`                  | Complement of `\d`, short for `[^\d]` |
| `\w`                  | Word character, short for `[a-zA-Z\_]` |
| `\W`                  | Complement of `\w`, short for `[^\w]` |
| `\s`                  | Whitespace character, short for `[\r\n\t\f\v ]` |
| `\S`                  | Complement of `\s`, short for `[^\s]` |
| `\v`                  | Vertical whitespace, short for `[\n\f\r]` |
| `\V`                  | Complement of `\v` |


## Character classes

- Character classes tell the engine to match one of several characters. 

- Importantly: `[^a-z]u` does *not* mean "u not preceded by a lowercase
  letter", but "u preceded by *something* that isn't a lowercase letter".
  Hence, the pattern doesn't match a *u* at the beginning of a string. (In
  contrast to the `.`, the negated character class does match invisible line
  breaks, though, so the above pattern would match the string *\nu*.)

- Within a character class, metacharacters are literals with the exception of
  *^*, *-*, *\\* and *]* if they are used in places where they have special
  meaning: ^ at the beginning, *-* as part of a range, *]* at the end, and *\\*
  to escape another special character or to form a token (i.e. always), and *]*
  at the end. Hence, this regex matches them all as literals: `[]\\-^]` (for
  details on how to includ metacharacters indide character classes without
  escaping them, see relevant section here
  [here](https://www.regular-expressions.info/charclass.html)].

Character classes examples

| Regex                 | Match |
| - | - |
| `[ab]`                | One of *a* or *b* |
| `[^ab]`               | Any character that isn't *a* or *b* (incl. newline) |
| `[\w\s]`              | One word or whitespace character |
| `[A-By-z1-2]`         | One of *A*, *B*, *y*, *z*, *1*, *2* |
| `[ -~]`               | Any character in the printable section of the ASCII |
| [table](https://www.asciitable.com) |

Exercises:

1. Match *gray* and *grey* in *London is grey; New York, gray.*.

2. Match any character that is neither a digit nor a (hidden) line break
  character. 

3. What does `q[^u]` match in *Iraq* and *Iraq is a country*?

4. How could we match any *q* not followed by a *u*?

5. Search for a literal * or +. 

6. Match any number greater than 10 made up of all the same digit (e.g. 222,
   33, 5555).

7. In *b ab cb*, match *b* either at the beginning of the string or when
   preceded by an *a*.

8. What's the difference between `[\D\S]` and `[^\d\s]`?

Solutions:

1. `\bgr[ae]y\b`. Discussion: need global flag on or use `findall()` in Python
   to match both words, otherwise I'll just get the first one.

2. `[\D\V]`. Discussion: the negated character classs matches hidden line break
   character by default (unlike the .), so need to explicitly exclude them.

3. Nothing and `q `. Discussion: the regex means "q followed by something that
   is not a u", not "q not followed by a u", so it requires something to follow
   the q, and that something to not be a u. That something, which happens to be
   a whitespace in the second string, is part of the match.

4. `q(?!u)`.

5. `[*+]`. Discussion: these two characters have no special meaning within a
   character class, so no need to escape them.

6. `(\d)\1+`. Discussion: need a capturing group for this (`[\d]{2,}`, for
   instance, would match any two digit number).

7. `(?:^|a)b`. Discussion: `[a^]b` would not work here, since `^` is matched
   literally inside a character class, so need a non-group with an alternation.

8. `[\D\S]` matches a single character present inside the character class, so a
   character that is either not a digit or not a space, which is every
   character. `[^\d\s]` matches a single character that is not present inside
   the character class, so that is neither a digit nor a space, which is all
   letters.


## Quantifiers

- A quantifier tells the engine to match the immediately preceding character,
  token, or subexpression (e.g. `(a|b)`) a certain number of times.

Nomenclature:

- *Greedy* quantifiers: the default property of quantifiers to match as many
  characters as possible and thus return the longest possible match. E.g. `\d+`
  matches *123* (not *1* or *12*) against *123*.

- *Docile* quantifiers: the property of a greedy quantifier to backtrack and
  give up characters to try the rest of the pattern to match. This is the
  property behind the "possible" in the above definition: a greedy quantifier
  matches as many characters of the quantified token as it can for the overall
  pattern to match. E.g. `.*c` will run all the way to the end of the string *abc*,
  fail to match the *c* in the pattern, backtrack and give up the *c* character
  matched by dot-star, try again to match *c*, succeed, and return.

- *Lazy* quantifiers: the property of a quantifier to match as few characters
  as necessary and thus return the shortest possible match. Quantifiers are
  made lazy by appending `?`. Example: `\d+?` matches *1* against *123*.  Lazy
  quantifiers are expensive: laziness and helpfulness make the engine advance
  from the beginning to the end of a string character by character, at each
  step expanding the match by including the next character, advancing and
  attempting to match the rest of the pattern, fail, backtrack, and repeat
  until it finds a match or reaches the end of the string.

- *Helpful* quantifiers: the property of a lazy quantifier to backtrack and
  match additional characters of the quantified token in the attempt to match
  the rest of the pattern. This is the property behind the "necessary" in the
  above definition: a lazy quantifier matches as few characters as it can for
  the overall pattern to match. E.g. `a*?b` will first match zero *a*s against
  `aab`, advance and try to match the *b*, fail, backtrack and match the first
  *a*, advance and try to match the *b*, fail again, backtrack and match the
  second *a*, advance and try to match the *b*, succeed and return.

- *Possessive* quantifiers: an optional property of a quantifier that prevents
  it from giving up previously matched characters if the rest of the pattern
  doesn't match (i.e. it makes the quantifier non-docile). We can make a
  quantifier possessive by appending a `+`. Example: `a++` greedily matches as
  many *a*s as it can and never gives any of them back.

Quantifiers and modifiers:

| Token          | Legend |
| - | - |
| `?`            | Match zero or once |
| `\*`           | Match zero or more |
| `+`            | Match once or more |
| `{n}`          | Match n times |
| `{n,m}`        | Match between n and m times, n defaults to 0, m to infinity
| | |
| `?`            | Make quantifier lazy |
`{quantifier}+`| Make quantifier possessive

Matches in string *a5aa5*:

| Pattern       | Matches in GLOBAL mode (total: list) |
| - | - |
| `a`           | 3: a, a, a |
| `a+`          | 2: a, aa |
| `a+?`         | 3: a, a, a |
| `a*`          | 5: a, '', aa, '', '' |
| `a*?`         | 6: '', '', '', '', '', '', '' |
| `a?`          | 6: a, '', a, a, '', '' |
| `a??`         | 6: '', '', '', '', '', '' |
| `a{2}`        | 1: aa |
| `a{,2}`       | 5: a, '', aa, '', '' |
| `a{,2}?`      | 6: '', '', '', '', '', '' |
| `a{1,}`       | 2: a, aa |

The [greedy trap](https://www.rexegg.com/regex-quantifiers.html#greedytrap)

In the string *{start} Mary {end} had a {start} little lamb {end}*, match all
tokens that start with *{start}* and end with *{end}*. The naive solution is,
`{start}.*{end}`, which will run over the first *{end}* to match entire string
since `.*` is greedy -- this is the greedy trap.

Solutions:

- *Lazy quantifier*: `{start}.*?{end}`. Computationally inefficient as it
  proceeds character-by-character left to right with successive backtracking.

- *Negated character class*: `{start}[^{]*{end}`. An example of the contrast
  principle, but works only if *{* never appears inside the delimiters.

- *Tempered greedy token*: `{start}(?:(?!{end}).)*{end}`. Ensures that the `.`
  never matches the opening bracket of *{end}*, thus making sure we don't run
  over an end token. This allows the *{* to occur inside the string. Because it
  requires a lookahead at east step, it is no more efficient than the lazy
  quantifier solution in this case, though. 

- *Explicit greedy alternation*: `{start}(?:[^{]|{(?!end}))*{end}`. This is an
  example of the *say what you want* principle: we either want to match
  characters that aren't an opening brace or an opening brace not followed by
  *end}*. This requires a lookahead only in the rare case where we find an
  opening brace rather than at each step and is thus more efficient than the
  tempered greedy token or lazy quantifier solutions. We can optimise the
  pattern in two ways: avoiding exiting the alternation at each step and
  instead matching entire sequences of non-brace characters, and avoiding
  backtracking if the *{end}* token at the end of the pattern fails to match,
  which will never be useful. We can achieve these optimisations by either
  using possessive quantifiers `{start}(?:[^{]++|{(?!end}))*+{end}` (`++` is
  required to avoid an explosive quantifier) or atomic groups
  `{start}(?>(?:(?>[^{]+)|{(?!end}))*){end}`.

The [lazy trap](https://www.rexegg.com/regex-quantifiers.html#lazytrap)

In *{start} Mary {end}00A {start} little {lamb {end}01B*, match all
tokens that start with *{start}* and end with *{end}*, followed by a sequence
of digits and a *b*, which are to be included in the match. The naive solution,
`{start}.*?{end}\d+B` doesn't work, as it runs over the first *{end}* to match
the entire string (why?) -- this is the lazy trap.

Solutions:

- *Atomic groups*: `{start}(?>.*{end}\d+B)` prevents the engine from
  backtracking once *B* can't be matched after the first *{end}00* and thus
  prevents the `.*` to expand further.

- *Negated character class*: `{start}[^{]*{end}\d+B` works, but with the usual
  limitation that it requires the assumption that there are no *{* between the
  start and end tokens.

- *Tempered greedy token*: `{start}(?:(?!{end}).)*{end}\d+B` works just as in
  the greedy trap solution above.

- *Explicit greedy alternation*: `{start}(?:[^{]++|{(?!end}))*+{end}\d+B` also
  works just as in the greedy trap solution above.

Exercises:

1. What does the quantifier apply to in the following patterns: `\w+`,
   `carrots?`, `(a|b)*`, `\Qab\E+`, `(?:(?!{end}).)*`. 

2. What's the simplest way to match *color* or *colour*?

4. Why is `<.+?>` not an ideal solution? 

5. Match digits of length 2, 4, or 6. 

6. If the above solution matches *123456*, what does `\1` contain?

7. Adapt the regex from above so it always captures the full match.

8. Does `A+.` match *AAA*? What about `A++.`? Explain.

9. Write a regex that matches strings of digits that end with an *a*, such as
   *123a*, with maximal efficiency.

10. Explain, step-by-step, what happens if we try to match *aaac* with the
   pattern `^(a+)*b`.

11. In *{start} Mary {end} had a {start} little lamb {end}*, match all tokens
    that start with *{start}* and end with *{end}*, but only if the string
    doesn't contain *{mid}* or *{restart}*.

Solutions:

1. `\w`, `s`, `(a|b)`, `b`, `.`.

2. `colou?r`.

3. Because by default, quantifiers are greedy and so `.+` matches as many
   characters as it can, initially racing all the way to the end of the string,
   then failing to match `>`, then backtracking once, trying again, succeeding
   and (eagerly) returning. To only match the opening token, use `<[^>]+>`.

4. Because it's computationally expensive.

5. `(\d\d){1,3}`.

6. *56.* Explanation: the backreference always contains the content of the last
   iteration of the group, so `(\d\d){3}` captures the same text as
   `\d\d\d\d(\d\d).`

7. `((?:\d\d){1,3})`. Explanation: wraps the full match in a capturing
   group and turns the subexpression we don't want to capture in a
   non-capturing group.

8. Solution: yes and no. Explanation: the first pattern first greedily matches
   all three *A*s in the string, then advances in the pattern and fails to
   match the dot, backtracks and gives up the last matched *A*, advances again,
   succeeds in matching the dot with the last *A* in the string, and returns.
   The second pattern also fails to match the dot at first, but because it is
   possesive it doesn't backtrack and give up the last-matched *A* and so
   simply fails.

9. Solution: `\d++a`. A possessive quantifier improves efficiency because `\d`
   and *a* are mutually exclusive, so there is never a good reason for the
   engine to give up characters and backtrack as there cannot be an *a* inside
   the (greedily) matched sequence of digits.  Hence, if the last matched digit
   isn't followed by an *a* we want the engine to fail immediately. This is
   what the possessive quantifier does. If we know that the regex can only
   match at the beginning of the string, then prepending the `\A` anchor
   improves efficiency by failing when we can't match the pattern starting from
   the first digit in the string instead of stepping through all remaining
   digits, which can't possibly match.

10. This is an example of an [explosive
    quantifier](https://www.rexegg.com/regex-explosive-quantifiers.html#example):
    a case where the number of combinations the engine attempts to match by
    successive backtracking increases exponentially in the length of the
    string. What happens? `a+` matches *aaa*, `*`, nothing, and the `b` fails
    to match against *c*. The engine backtracks and makes `a+` give up the last
    matched character, so this now matches *aa*, `*` can now repeat the
    previous pattern -- remember, it matches the pattern `a+`, not the match
    *aa* -- and matches *a*, but `b` again fails to match against *c*. In the
    next backtrack, the `a+` matched by `*` gives up the last matched
    character, the third *a*, so the first `a+` still matches *aa*, the second
    `a+`, nothing, and `b` fails to match. This keeps going. RexEgg has a
    useful
    [table](https://www.rexegg.com/regex-explosive-quantifiers.html#combinations)
    to show the match of different repetitions of the `a+` component:

| `a+`    | `a+`  | `a+` |
| - | - | - |
| aaa     | -     | - |
| aa      | a     | - |
| aa      | -     | -  |
| a       | aa    | - |
| a       | a     | a |
| a       | a     | - |
| a       | -     | - |
| \-      | -     | - |


11. `{start}(?:(?!{mid})(?!{restart}).)*?{end}`.


## Anchors and word boundaries

- Anchors assert that the engine's current position in a string matches a
  certain position like the beginning or the end, while boundaries make
  assertions about what can and cannot be matched to the left and the right of
  the current position.

- `^` matches the position just before the first character of the string, so
  `^a` means "position just before start of string followed by a". Similarly,
  `$` matches position just after the last character in the string, and `c$`
  means "c followed by the position just after the end of the string".

- Multiline mode makes `^` and `$` match positions just before first and just
  after last character of the line rather than the entire string.

- `$` subtlety: if the very last character in a line is a line break, `$`
  matches both just before it and at the very end just after it (i.e. `\d+$`
  matches *123* in both *123* and *123\n*. This is true regardless of whether
  multiline mode is turned on. (If there are multiple line breaks at the end,
  the above behaviour only applies to the final one, so `\d+$` would not match
  *123* in *123\n\n*.)

- `\z` vs `\Z:` similar to the above point, in most engines `\z` matches only
  at the very end of a string (i.e. after the linebreak if there is one), while
  `\Z` is the flexible end-of-string anchor that can match before and after the
  linebreak at the end of a string. In Python, `\Z` behaves like `\z,` and `\z`
  doesn't exist.

| Character         | Legend |
| - | - |
| `^`               | Matches beginning of string or line (in multiline mode) |
| `$`               | Matches end of string or line (in multiline mode) |
| `\A`              | Matches only beginning of string |
| `\Z`              | Matches only very end of string (same as `\z` in most other engines) |
| `\b`              | Matches if one side is a word character and the other isn't |
| `\B`              | Matches wherever `\b` doesn't |

Exercises:

1. Match *cat* a) on its own or at the end of a word (e.g. *tombcat*), b) on
its own or at the beginning of a word (e.g. *catwalk*), c) only on its own, d)
fully surrounded by word characters, e) fully surrounded or at the beginning or
the end but not on its own.

2. Match *Jane* or *Janet*.

3. Create a boundary that detects the edge between a letter and a non-letter.

4. In the string *0# 1 #2 #3# 4# #5*, match digits where each side is either a
   hash or the edge of the string (i.e. 0, 3, 5).

5. Within the vernacular of RexEgg, explain the difference between an anchor, a
   boundary, and a delimiter.

6. Implementing `^` manually: write patterns that match *a* at the beginning of
   a) the string, b) each line, c) line three and beyond.

Solutions:

1. a) `cat\b` b) `\bcat`, c) `\bcat\b`, d) `\Bcat\B`, e) `\Bcat|cat\B`.

2. `\bJanet?\b` or `\b(Jane|Janet)\b`.

3. `(?i)(?<![a-z])(?=[a-z])|(?<=[a-z])(?![a-z])`. Discussion: RexEgg uses the
   following
   [alternative](https://www.rexegg.com/regex-boundaries.html#real-word-boundary):
   `(?i)(?<=^|[^a-z])(?=[a-z])|(?<=[a-z])(?=$|[^a-z])`.  The two versions are
   the same, but I find the first version easier to read.  Using negated
   character classes requires that we explicitly allow for `^` and `$`, since
   otherwise the regex engine tries to match a character that isn't a letter
   and [fails](https://www.regular-expressions.info/charclass.html). Using
   negative lookarounds solves this, since these succeed whenever the engine
   cannot match a lowercase letter in the specified position in the string,
   which is also true if there is a beginning or end of line character in that
   [position](https://www.regular-expressions.info/lookaround.html).

4. Using capturing group: `(?:^|#)(\d)(?:$|#)`. Using lookarounds:
   `(?<=[#^])\d(?=[#$])`. Using [double negative
   delimiter](https://www.rexegg.com/regex-boundaries.html#double-negative-delimiter):
   `(?<![^#])\d(?![^#])`. The lookbehind asserts: "what immediately precedes
   the current position is not a character that is not a hash", which, turning
   the logic around, is equivalent to "either not a character or a hash". The
   logic of the lookahead is similar. This is thus a clever way to match either
   a particular (set of) characters or the edge of a string. (This works for
   single-line strings only, as in multiline strings, `\n` characters at the
   beginning and end are characters that aren't a hash.)

5. They all make assertions about the current position in the string: *anchors*
   assert that what immediately precedes or follows the furrent position is a
   particular position in the string such as the beginning of the string or the
   end of the line; *boundaries* make assertions about that is immediately to
   the left and the right of the current position such as a non-word character
   on the left and a word character to the right; and *delimiters* are similar
   to bouldaries but only look on one side, asserting, for instance, that what
   immediately precedes the current position is not a character. These lines
   are [blurry](https://www.rexegg.com/regex-anchors.html#semantics), however.

6. a) `(?s)(?<!.)a`, b) `(?<!.)a`, c) `(?<\n.*\n)a`. Discussion: in a) we need
   DOTALL mode so that `.` matches linebreaks to prevent the engine from
   matching at the beginning of new lines, in b) we want the engine to match at
   the beginning of new lines and thus omit DOTALL mode, for c) we need the
   flexible-width lookbehinds from the `regex` module.


## Alternation

- Character classes like `[ab]` tell the regex engine to match a single
  character out of several possible characters; alternations like `(Jane|Bob)`,
  to match a single regex out of several possible regexes.

Exercises:

1. What do `cat|dog`, `\bcat|dog\b`, and `\b(cat|dog)\b` match?

2. Find all occurrences of *Get*, *GetValue*, *Set*, *SetValue*. 

Solutions:

1. The first matches any occurrences of the strings (e.g. *cat* in
   *uncategorised* or *dog* in *dogmatic*), the second matches words that begin
   with *cat* and words that end with *dog*, the third *cat* and *dog* on their
   own.

2. `(Get|Set)(Value)?` is reasonably concise and easy to read. It works because
   `?` is greedy, which means it attempts to match *GetValue* before *Get*,
   assuring that it never matches *Get* in *GetValue*.


## Groups

- Grouping part of a regex together can be useful to apply a quantifier to a
  group of tokens, to restrict alternation to a part of the pattern, and to use
  backreference.

- There are three types of groups: capturing, non-capturing, and atomic. 

- Capturing groups have three main uses: 1) reuse matches using backreferences,
  2) use captured text as replacement text in search and replace, 3) use
  captured parts in applications. Capturing groups get numbered from left to
  right, and, if they have a quantifier, return the value of the last captured
  iteration.

- Non-capturing groups allow for avoiding the capturing overhead when grouping
  is needed but capturing isn't.

- Atomic groups become solid as a block once the engine leaves the group and
  thus prevent the engine from backtracking into the group even if the rest of
  the expression fails to match. This can be useful to avoid unwanted
  backtracking when groups contain quantifiers or alternation. In the former
  case, we could also use possessive quantifiers.

| Character             | Legend |
| - | - |
| `(regex)`             | Capturing group |
| `\1, ..., \99`        | Backreferences to capturing groups |
| `(?:regex)`           | Non-capturing group |
| `(?P<name>regex)`     | Named capturing group in `re` module |
| `(?P=name)`           | Backreference to named capturing group in `re` |
| `(?<name>regex)`      | Named capturing group in `regex` module |
| `\g<name>`            | Backreference to named capturing group in `regex` |
| `(?>regex)`           | Atomic group |

Exercises:

1. Find magical dates, dates where the two final year digits are identical to
   the day and month digits (e.g. *2008-08-08*).

2. Capture day, month, year in *dd-mm-yyyy* dates.

3. Name the groups in the above example (use the `regex` module).

4. Search for magic dates using a named group. 

5. What's the difference between the result returned from `(\w+)` and `(\w)+`
   when matching the string *Hello*? 

6. Find all patterns of the form *sum of digits = reversed sum of digits* (e.g.
   *22 + 333 = 333 + 22*). 

7. Find all cases of repeated words in *Hello world world this was some great
   greatness, wasn't wasn't it?*. 

8. A typical URL has the form `<protocol>://<host>/<path>` (e.g.
   `https://www.abc.com/index.html`). Write a regex that captures the host and,
   if available, the path but not the protocol, yet validates that the protocol
   is either *http* or *https* (inspired by
   [this](https://stackoverflow.com/a/3513858) SO post).

9. Write a regex similar to the previous one, but now validate that the host is
   one of *http*, *https*, or *s3*.

10. In strings containing *Bob says: word*, group the entire regex but only
    capture the word Bob says (e.g. in *Bob says: hello* capture *hello*.

11. In strings containing tokens of the form *upNUMBER* or *downNUMBER*,
    capture the tokens. 

12. Does `(?>A|.B)C` match against *ABC*? 

13. Does `(?>a+)[a-z]c` match against *aac*? 

Solutions:

1. `\d\d(\d\d)-\1-\1`.

2. `(\d{2})-(\d{2})-(\d{4})`.

3. `(?<day>\d{2})-(?<month>\d{2})-(?<year>\d{4})`.

4. `\d\d(?<yy>\d\d)-\g<yy>-\g<yy>`

5. `(\w+)` returns *Hello*; `(\w)+`, *o*. Discussion: a capturing group with a
   quantifier contains the last matched iteration.

6. `(\d+) \+ (\d+) = \2 \+ \1`.

7. `(\b[\w']++\b) \b\1\b`. Discussion: If we don't use word boundaries we'd
   also match the *s*s in *was some* and *great* in *great greatness*, and
   without allowing for *'* we'd miss the repetition of *wasn't*. Adding a
   possessive quantifier avoids unnecessary backtracking, which we never want
   here, as we always want to capture full words only.

8. `https?://([^/\s]+)(\S+)?`. Discussion: The `\s` inside the character class
   ensures the match doesn't include characters that follow the url. We could
   include `/` in the second capturing group to be explicit that what
   immediately follows the host starts with a forward slash, but it's redundant
   because the first group matches up to a space character or a forward slash
   and the second group only matches if what follows directly thereafter is not
   a space, character, which implies that the second group can only return a
   match if its content starts with a forward slash.

9. `(?:https?|s3)://([^/\s]+)(\S+)?`. Discussion: remind yourself why we cannot
   just add an alternation without a non-capturing group.

10. `(?:Bob says: (\w+))`. Discussion: a contrived use of a capturing group
    within a non-capturing group.

11. `((?:up|down)\d+)`. Discussion: an example of capturing the content of a
    non-capturing group by wrapping it in a capturing group.

12. No, the engine will match *A* at beginning of the string and then fail to
    match *C*. Because the group is atomic, it won't backtrack into the group
    to match *.B* and fail.

13. No. Similarly to above, the engine greedily matches both *a*s, then the
    character class matches *c*, and the final *c* in the regex fails to match.
    Because the grouped expression is atomic, the engine doesn't backtrack and
    give up one of the two matched *a*s.


## Lookarounds

- Just like anchors, lookarounds are zero-length assertions that determine
  whether a match is possible in a given location. The difference to anchors is
  that lookarounds match characters rather than positions in the string, but
  then give up the matched strings and simply return whether or not they
  existed. The last step is what makes them zero-length matches, which means
  the regex engine stays at the current position in the subject string rather
  than advancing.

- Lookaheads can contain any regex, lookbehinds can't: they have to be
  fixed-length expressions (i.e. literalse, character escapes, character
  classes, or alternations where all alternatives are of equal length, but not
  quantifiers or backreferences). This is because the regex engine steps back by
  the length of the lookbehind to evaluate matches, and thus needs to know said
  length. (Actually, the `regex` module can handle flexible-width lookbehinds.)

- As a result of the above, capturing groups can only be used in lookaheads.
  To use them, simply wrap the regex in parentheses.

- Lookarounds don't look way into the distance: `(?=A)` doesn't mean "there is
  an A somewhere to the right", it asserts that what immediately follows is an
  A. To look into the distance, you have to include
  ["binoculars"](https://www.rexegg.com/regex-lookarounds.html#stand_their_ground)
  such as `.*` or, if possible, more specific tokens.

| Lookaround  | Name                  | What it does |
| - | - | - |
| `(?=foo)`   | Lookahead             | Asserts that what immediately follows the current position in foo |
| `(?<=foo)`  | Lookbehind            | Asserts that what immediately precedes the current position is foo |
| `(?!foo)`   | Negative\nLookahead   | Asserts that what immediately follows the current position is not foo |
| `(?<!foo)`  | Negative\nLookbehind  | Asserts that what immediately precedes the current position is not foo |

Practice:

- Write `\A` using a lookaround. Solution if DOTALL mode is on: `(?<!.)`
  Solution if DOTALL mode is off: `(?<![\D\d])`. Discussion: If DOTALL mode is
  on an `.` matches every character including linebreaks, the first lookbehind
  asserts that what precedes the current position is not any character, so the
  position must be the beginning of the string. `[\D\d]` matches any character
  that is a digit or not a digit, which is any character, and thus achieves the
  same thing if DOTALL mode is off.

- Match e if followed either by aa or bb. Solution: e(?=([ab])\1).

- What does `q(?=u)i` match in "quit"? Solution: nothing. The regex tries to
  match a u and an i at the same position.

- Match words that don't end in s. Solution: `\b\w+(?<!s)\b.` Explanation:
  approach matches words and, at the end postition, looks back to check that
  the character that immediately precedes the current position, which is the
  last character, is not an "s". Needs word boundaries to prevent engine from
  backtracking and match word without final s.

- Explain why `A(?=5)(?=[a-z])` doesn't match `A5k` and write a regex that does.
  Solution: Because lookarounds [stand their
  ground](https://www.rexegg.com/regex-lookarounds.html#stand_their_ground):
  they don't alter the position in the string, so the second lookahead also
  starts at A and finds a 5 rather than a letter. `A(?=5[a-z])` does the job.

- Validate that a password meets the following
  [conditions](https://www.rexegg.com/regex-lookarounds.html#password): 1) must
  have between 6 and 10 word characters, 2) must include at least one lowercase
  character, 3) must include at least three uppercase characters, 4) must
  include a digit. Match valid passwords. Solution: 1) `\A(?=\w{6,10}\Z)`, 2)
  `(?=[^a-z]*[a-z])`, 3) `(?=(?:[^A-Z]*[A-Z]){3})`, 4) `(?=[\D]*\d)`, to
  match: `.*`. Complete solution:
  `\A(?=\w{6,10}\Z)(?=[^a-z]*[a-z])(?=(?:[^A-Z]*[A-Z]){3})(?=\D*\d).*`
  Discussion: Why can't we just use `[a-z]` to check for condition 2? This will
  find a match if the string contains a lowercase letter, but, naturally, the
  engine will also move to the position of that matching character, whereas we
  want to stay at the first character to perform subsequent lookaheads, so we
  need a match that starts at the first character.

- Show two ways how to remove the redundant lookahead in the above solution.
  Solution 1: `\A(?=[^a-z]*[a-z])(?=(?:[^A-Z]*[A-Z]){3})(?=\D*\d)\w{6,10}\Z`
  Solution 2: `\A(?=\w{6,10}\Z)(?=[^a-z]*[a-z])(?=(?:[^A-Z]*[A-Z]){3})\D*\d.*\Z`
  Discussion: When using n lookaheads to validate n conditions we can always put
  the regex from any of the lookaheads at the end and use it to validate a
  particular pattern *and* to match the entire string. If the condition doesn't
  already match the entire string as in solution 1, we can always add `.*\Z`.
  Why do we need the \Z? Because unless we are in dotall mode, `.` doesn't match
  linebreaks and thus gets us to the end of the line rather than the end of the
  string. To ensure that the pattern works for the entire string, we thus need
  \Z.

- Explain why, to validate the password above, we need the contrast pattern for
  parts 2-4 of the solution (i.e. why do we need `[^a-z]*[a-z]` instead of
  `[a-z]`? Solution: because the lookahead doesn't look into the distance but at
  the character that immediately follows the current position. `[a-z]` checks
  whether what immediately follows the current position is a lowercase
  character. What we want is to check whether, immediately following the current
  position.

- Validation: Match a single word character that is not an A. Do so using 1)
  character class set operations, 2) a lookahead, 3) a lookbehind. Solutions:
  1) `[\w--Q]`, 2) `(?!Q)\w`, 3) `\w(?<!Q)`. The latter two are the password
  validation approach from above.

- Tempering the scope of a token: Match any character as long as it's not
  followed by *{end}*. Solution: `(:(?!{end}).)*`. Discussion: each `.` is
  tempered by the negative lookahead, which specifies that the dot cannot be
  the beginning of the string *{end}*. We have thus a tempered version of `.*`
  -- making sure it matches anything except a particular pattern, which can be
  useful if, for instance, we want to match anything up to a certain pattern
  (see tempered greedy token
  [solution](https://www.rexegg.com/regex-quantifiers.html#tempered_greed)).

- Delimiters: Match everything between *#start#* and *#end#*. Solution:
  `(?<=#end#).*?(?=#end#)`. Discussion: we make the dot-start lazy by adding
  `?` to ensure that the engine matched the first end tag that accurs after the
  start string rather than the last one.

- Inserting text at a
  [position](https://www.rexegg.com/regex-lookarounds.html#camelinsert): Insert
  an underscore between words in strings that are in CamelCase. Solution:
  `(?<=[a-z])(?=[A-Z])` finds the positions, string replacement tool does the
  rest (see
  [here](https://fabiangunzinger.github.io/blog/python/2021/09/11/regex-in-python.html#Insert-text-in-position)
  for an example).

- Finding overlapping
  [matches](https://www.rexegg.com/regex-lookarounds.html#overlapping): Write a
  pattern that extracts *abc*, *bc*, *c* from *abc*. Solution: `(?=(\w))` with
  GLOBAL flag (`re.findall()` in Python). Discussion: an unanchored lookaround
  with a capturing group is just what we need here: at each position, the
  engine looks ahead until `\w+` stops matching and captures the string in
  between, then moves one position forward in the string and repeats.

- Compound
  [lookarounds](https://www.rexegg.com/regex-lookarounds.html#back_to_the_future):
  1) match a number that is preceded and followed by exactly one underscore.
  Solution: `(?<=(?<!_)_)\d+(?=_(?!_))`. Discussion: the compound lookbehind
  asserts that what precedes the position at the beginning of the number is a
  position that is not preceded by an underscore but itself contains an
  underscore. The compound lookahead asserts that what immediately follows the
  position at the end of the number is a position with an underscore that is
  not followed by another underscore.

- In the string `_rabbit _dog _mouse DIC:cat:dog:mouse`, where the DIC list
  at the end contains the list of allowed animals, match each *_token*
  named after animals in the allowed list. Solution: `_(\w+)\b(?=.*:\1\b)`.
  Discussion: don't forget the second word boundary, as without it, we'd also
  match *_dog* if only *doggie* were in the allowed list. It's not clear to me,
  though, why I need the first boundary.

- In the above string, why does `_(?=.*:(\w+)\b)\1\b)` only match *_mouse*?
  Solution: Two reasons: 1) because `*` is greedy and, upon finding an
  underscore in the string, shoots all the way to the end of the string and
  backtracks only far enough to match the first colon, which is the one before
  *mouse*. Second: because the engine doesn't backtrack into lookarounds. Once
  the lookaround has evaluated as true of false, a failure to match further
  down in the regex doesn't cause the engine to go back into the lookaround and
  backtrack further. Hence, lookarounds are
  [atomic](https://www.rexegg.com/regex-lookarounds.html#atomic). 


## Flags and inline modifiers

- To use flags in Python's `re` module, pass the keyword `flags=re.FLAGNAME` to
  the method (e.g. `re.findall(pattern, string, flags=re.MULTILINE)`).

| Flag (inline modifier) | Legend |
| - | - |
| [A]SCII (?a)           | Make tokens match ASCII rather than Unicode |
| GLOBAL                 | Don't return after first match (use `re.findall()`)|
| [I]GNORECASE (?i)      | Case insensitive matching |
| [M]ULTILINE (?m)       | Make ^ and $ match end of line (not end of string) |
| S, DOTALL (?s)         | Make . match newline (also called single-line) |
| X, VERBOSE (?x)        | Allow linebreaks for easier-to-read regexes |


## Subroutines and recursive expressions

- The backreference `\1` repeats the *characters captured* by the first capturing group;
  subroutine `(?1)`, the *pattern defined* by the first capturing group. This can be very
  useful to make long expressions shorter.

- There is lots
  [more](https://www.rexegg.com/regex-disambiguation.html#subroutines) to
  subroutines, but for my current use cases, the basics are enough.

- Recursive patterns are related to subroutines in that a soubroutine can call
  itself recursively. In addition, `(?R)` tries to match the entire pattern
  recursively ([This](https://www.regular-expressions.info/recurse.html)
  description of the steps the engine takes is very useful).

Exercises:

1. Match instances of *Harry meets Sally* and *Sally meets Harry*.

2. Match strings of the form *ab*, *aabb**, *aaabbb***.

3. Match the same strings as above, but now as part of a larger string that
   might contain other characters, including *aab*, which we'd not want to
   match.

4. Match stand-alone strings of the form *bbmmee*, *bme*, *bbbmmmeee* that
   might possibly occur as part of a larger string.
`\b(b(?>(?1)|m)*e)\b`

Solutions:

1. `(Harry|Sally) meets (?1)`.

2. `a(?R)?b`.

3. `\b(a(?1)b)\b`. Discussion: this requires wrapping a recursively called
   subroutine in word boundaries. Using `(?R)` instead of `(?1)` would only
   match *ab*, since the recursion would also try to match repeated word
   boundaries.

4. `\b(b(?>(?1)|m)+e)\b`. Discussion: We need to use a subroutine rather than a
   recursion of the entire pattern for the same reason as in the previous
   exercise. The real action happens inside the capturing group:
   `(b(?>(?1)|m)+e)` represents the [generic
   pattern](https://www.regular-expressions.info/recurse.html) pattern to match
   balanced constructs (I use a `+` instead of a `*` quantifier on the atomic
   group, which ensures there is at least one middle element). How does it
   work? For the string *bbmmee*, the first *b* in the pattern matches, so the
   engine advances and reaches the alternation inside the atomic group, from
   which the subroutine matches the second *b*. The engine again moves on to
   the alternation, which now matches *m* greedily one or more times, meaning
   it eats up all the *m*s in the centre of the pattern.  Finally, the engine
   tries to match the first *e* and succeeds, which means it has successfully
   matched the entire recursive call.  The engine now goes back to the initial
   pattern and tries to match the final *e*, which also succeeds and results in
   a successful overall match. We use an atomic group to avoid the engine from
   unnecessary backtracking (e.g.  after matching multiple *m*s but failing to
   match an *e*, the engine would release each *m* and attempt to match *e*
   again, which will never succeed).


## Character class set opetations

- The `regex` module has supports the set operations intersection, union, and
  subtraction on character classes. (Inner brackets are optional but can help
  with readability.)

| Operation           | Pattern               | String        | Matches |
| - | - | - | - |
| Intersection        | `r'[\W]&&[\S]]'`      | *a.k$_8*      | *['.', '$']* |
| Union               | `r'[ab\|\|\d]'`         | *a.k$_8*      | *['a', 8]* |
| Subtraction         | `r'[\w--k]'`          | *a.k$_8*      | *['a', '_', 8]*|


## Gotchas

- Based on [this](https://www.rexegg.com/regex-gotchas.html) page.

Exercises:

1. Why doesn't `[a-z]+` match *Cat*? How can you fix it?

2. Why doesn't `My .* cat` match the below string? How can you fix it?

    *My dog
    and my cat*

3. How can we avoid the regex `cat` from matching in the string *certificate*
   but find it in patterns like *_cat12*?

4. The regex `[128]|18` is supposed to match *1*, *2*, *8*, and *18*. In the
   string *18 18*, (a) what does it match without any flags? (b) what does it
   match with the *global* flag on? (c) when would it match *18* and why? (d)
   how could it be improved to achieve its aim?

5. We use the pattern `x*` with replacement string *y*. Running it on *x*, we get
   *yy*, running it on *a* we get *yay*. What's going on?

Solutions:

1. Because regex is case-sensitive by default and thus, as writte, only matches
   lowercase characters. Could either us an inline modifier `(?i)[a-z]+` or
   explicitly search for uppercase and lowercase characters `[A-Za-z]+`.

2. Because `.` does not match line breaks by default. The easiest way to fix
   this is to use *DOTALL mode* (also called *single-line mode*) `(?s) My .*
   cat`.

3. If we only ever wanted *cat* on its own, simple word boundaries `\bcat\b`
   would do. To match it when surrounded by non-letter word characters, we need
   [real-word
   boundaries](https://www.rexegg.com/regex-boundaries.html#real-word-boundary).

4. (a) *1*, (b) *[1, 8, 1, 8]*. This surprised me for a moment: remember that
   the engine scans alternatives in the regex left to right, eagerly returns
   the first match, and then moves on to the next character in the string. (c)
   Never, since it will always match the *1* and move on without attempting to
   match the right-hand side of the alternation in the pattern. (d) Depending
   on the context, we could just reverse the alternation to `18|[128]`, or,
   more securely, use anchors or boundaries `\b(?:[128]|18)\b`.

5. Zero matches! In the first case, `x*` first matches *x* at position 0 of the
   string and replaces it with *y*, and then matches the empty space at
   position 1 after the *x* and replaces it as well. In the second case, the
   regex matches the empty string at position zero and replaces it, moves past
   the *a* to position 1, and again matches and replaces the empty string,
   giving us *yay*.


## The elements of regex style

Inspired and heavily based on
[this](https://www.rexegg.com/regex-style.html#contrast) fantastic section from
the RexEgg page.

> To write good regex, say shat you mean. Say it clearly.

> A string goes from \A to \Z (in `re`; to \z, in `regex`).

- Summary mnemonic: **Greedy atoms anchor again.**: greedy vs lazy, the cost of
  greedy and workarounds (say what you want, contrast); should parts be made
  atomic?; should I use anchors or boundaries?; should I use repeating
  subpattern syntax?

- To match or to capture? The full match is just another capture, in Python and
  many other engines referred to as group 0 and, by convention called "the
  match". So there is no difference between the two approaches. Best practice
  advise: use whatever gets the job done, while aiming to reduce overhead by
  reducing the number of capturing groups (use non-capturing groups if useful).

- To split or to match all? They are a different way of looking at the same
  approach, so use whichever is easier to get the job done.

- Whenever possible, anchor. It ensures that the engine finds the match in the
  right place, and often saves unnecessary backtracking.

- Say what you want and don't want, and avoid "dot-star soup". It saves
  unnecessary backgtracking and is clearer to read.

- Create contrast with consequtive tokens that are mutually exclusive (`\D` and
  `\d`, or `[^a-z]` and `[a-z]`). It can simplify patterns and save unnecessary
  backtracking. Example: to find strings with exactly three digits that are
  located at the end, I might start with ^.+\d{3}$. This doesn't work because .
  also matches digits, so I'd match abc12345. I could use negative lookbehind
  like so: `^.+(?\<!\d)`, but this would still match ab3c123. The real solution
  is to use mutually exclusive tokens to start with: ^\D+\d{3}$.

- Beware of lazyness. Avoid lazy quantifiers in favour and use contrast to say
  what you want to save unnecessary backtracking. Example: `{.*?}` matches
  everything inside curly brackets, but backtracking is
  [costly](https://www.rexegg.com/regex-quantifiers.html#lazy_expensive) as
  they backtrack at every step. `{[^}]*}` is more direct and faster.

- Use greediness and laziness deliberately. A greedy quantifier may shoot all
  the way to the end of the string, a lazy one tuck along backtracking at every
  step. Either can be useful when employed for a suitable purpose.

- Use atomic quantifiers. They can save a lot of backtracking.

- Design to fail: Compose regexes to minimise the number of unnecessary
  unsuccessful attempts. Example: with GLOBAL and MULTILINE modes on,
  `(?=.*flea).*` matches lines that contain "flea". But for lines that don't
  contain flea, it unnecessarily tries the lookahead at every single character.
  Anchoring the lookahead at the start of the line, `^(?=.*flea).*`, remedies
  that by only looking ahead from the first position of each line.

- Trust the dot-star to get you to the end of the line. It allows you to
  simplify patterns. Example: in a string such as *@abc @bcd* you want to match
  the last token if and only if the string contains more than one token.
  `@[a-z]+$` won't do because it also matches the last token if there is only
  one. `@[a-z].*\K@[a-z]+` does the trick, as the dot-start will shoot all the
  way to the end and then backtrack as as needed to match the rest of the
  pattern.

- To validate n conditions and capture strings that meet them, use n-1
  [lookaheads](https://www.rexegg.com/regex-lookarounds.html#n-1conds).


## Miscellaneous

- From tokens of the form *abc_12*, return only the digits. Solution: a simple
  way is to use the keep out token, which discards anything matched before it:
  `\w+_\K\d+`.

- Check whether string length is a multiple of 2, then a multiple of n.
  Solution: `^(?:..)+$` checks for multiples of two, `^(?:.{n})+$` for
  multiples of *n*.


## Frequently used patterns

Work in progress: 

- Match all strings inside quotation marks in the below block.

These are 'string one' and 'string
two' and 'that's string three'.

Thus far (with global flag/`findall()`):
- '.\*' Doesn't work because \* is greedy and matches 'string one' and ' and
  similar match on second line.
- '.\*?' Doesn't match string two since . doesn't match line-breaks and get's
  mixed up on second line.
- [^'\v]+ Behaves as the above
- [^']+ Now matches second string but including the linebreak, which we don't
  want as part of the match, and still gets tripped up by that's.
- Wanted: match string two but then exclude \v from match, ignore ' that are
  part of a word.


## Resources

- [Regular expressions
  cookbook](https://www.oreilly.com/library/view/regular-expressions-cookbook/9781449327453/)

- [RexEgg, awesome online regex resource](https://www.rexegg.com)

- [Regular-Expressions.info, another excellent online
  resource](https://www.regular-expressions.info)

- [Regular Expressions 101, very good regex tester](https://regex101.com)

