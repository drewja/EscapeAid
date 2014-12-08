#!/usr/bin/python3
# escapeaid.py

# Escape Aid  v0.1
# # xterm 256 color escaping made easy


# this is free software... liscense : gpl V2.0
# written in pure python and maintained by Andrew J. Arendt
#   andrewarendt@gmail.com
#    github.com/drewja/escapeaid

import sys
import os

from static import CODE_MAP
from static import STANDARD_COLORS
from static import PALLET_256
from static import COLORS_256
from static import COLOR_GROUP_256
from static import RESET
from static import FSTRING


TERM = os.getenv('TERM')

def bgString(bg):
    """helper function for color background of text"""
    return FSTRING.format('48;5;'+str(bg))

def fgString(fg):
    """helper function for color text"""
    return FSTRING.format('38;5;'+str(fg))

def _resolve(color):
    try: return int(color)
    except:
        try: return CODE_MAP[color]
        except KeyError: pass

def _escape(
    color = '', # int or string from codeMap
    bgcolor = '', # int or string from codeMap
    bold = False,
    reverse = False,
    underscore = False,
    score = False,
    blink = False,
    concealed = False,
    **kwargs):
    """ compiles escapes based on the keyword arguments or unpacked profile """
    escapes = ''
    if blink: escapes += FSTRING.format(str(CODE_MAP['blink']))
    if bold: escapes += FSTRING.format(str(CODE_MAP['bold']))
    if score: escapes += FSTRING.format(str(CODE_MAP['scored']))
    if underscore: escapes += FSTRING.format(str(CODE_MAP['underscore']))
    if reverse: escapes += FSTRING.format(str(CODE_MAP['reverse']))
    if concealed: escapes += FSTRING.format(str(CODE_MAP['concealed']))
    color = _resolve(color)
    bgcolor = _resolve(bgcolor)
    if bgcolor: escapes += bgString(bgcolor)
    if color: escapes += fgString(color)
    return escapes

def _colorize(text, color = '', bgcolor = '', **profile):
    """ applies escapes to text based on keyword arguments
       and returns a printable string"""
    try:reset = profile.pop('reset')
    except: reset = True
    if reset: reset = RESET
    else: reset = ''
    escapes = _escape(color, bgcolor, **profile)
    return escapes + text + reset

def cprinter(*args, csep = ' ', sep = '', end = '\n', file = sys.stdout,
            flush = False, **kwargs):
    """ lowest level print function combined with _colorize( function
    can be used with or without color arguments
    optional arguments csep is a string to be colored and placed between
    args, and sep is same thing but will not be colored with the texts.
    define sep or csep but both will ignore csep in favor of sep"""
    output = []
    if sep: csep = ''
    if csep: sep = _colorize(csep, **kwargs)
    for text in args:
        output.append(_colorize(text, **kwargs))
    output = _insertSep(output, sep)
    file.write(stringFromList(output))
    file.write(end)
    if flush: file.flush()


def picker(*basecolors, text = 'some Sample Text $ # @ * & ! { }',
            bg = 'black', reverse = False):
    """ generator of color previews and id's to be used with
        printer or profiles.
        optional basecolor group argument:
            one or more of : (default is all)
            'yellow', 'green','blue','brown', 'gold', 'orange', 'grey', 'red',
            'pink', 'purple'.

        examples:
        escapeaid.picker('blue', 'green')
            will print all colors in the blue group followed by all colors
            in the green group background colored.

        escapeaid.picker(bg='pink', reverse = True) will print all color id's with
            and pink text on  background _colorize(d to the cooresponding color.
        """
    if not basecolors:
        for i in COLORS_256:
            i = ' '+ ' '*(3-len(str(i))) + str(i)+' '
            print(_colorize(i,i,'black',reverse=True),
                  _colorize('   '+ text +'   ',
                  i, bg, reverse = reverse), _colorize(i, i))
    else:
        for c in basecolors:
            if c not in PALLET_256: continue
            for v in PALLET_256[c]:
                sv = str(v)
                sv = ' ' + ' '*(3-len(str(sv))) + str(sv)+' '
                print(_colorize('  '+c+'  ', v, bg, reverse = reverse),
                      _colorize(sv,v,'black',reverse=True),
                      _colorize('   '+ text + '   ',
                      v, bg, reverse = reverse), _colorize(sv, v))

def _insertSep(stringlist, sep):
    seplist = [sep for i in stringlist if i][:-1]
    newlist = []
    for n, sep in enumerate(seplist):
        s = stringlist[n]
        if s:
            if not str(s).isspace():
                newlist.append(stringlist[n])
            newlist.append(sep)
    newlist.append(stringlist[-1])
    return newlist

def stringFromList(stringList):
    r = ''
    for i in stringList:
        r += str(i)
    return r

def rainbow(string, bgcolors = None,
            colors = ['red', 'orange', 'yellow', 'green', 'blue', 'purple'],
                bold = False,
                reverse = False,
                underscore = False,
                score = False,
                blink = False,
                concealed = False,
                rlstrip = True,
                reset = True):
    """ defaults to rainbow colors, same as multi but _colorize(s preceeding
        filler space and following filler space seperately"""
    if type(bgcolors) in (int, str):
        bgcolors = [bgcolors,]
    if reset: reset = RESET
    else: reset = ''
    prefill = ''
    postfill = ''

    if rlstrip:
        for c in string:
            if c != ' ': break
            prefill += c
        string = string.lstrip(prefill)
        for c in reversed(range(len(string)-1)):
            if string[c] != ' ': break
            postfill += ' '
        string = string.rstrip(postfill)
    string = list(string)
    string.insert(0, prefill)
    string.append(postfill)

    return multi(string, colors, bgcolors,
                bold = bold,
                reverse = reverse,
                underscore = underscore,
                score = score,
                blink = blink,
                concealed = concealed,
                reset = True,
                sep = '')

def multi(strings, colors =[], bgcolors = [], sepprofile = None, sep = ' ',
         includesep = False, # include sep in the color pattern
         bold = False,
         reverse = False,
         underscore = False,
         score = False,
         blink = False,
         concealed = False, reset = True, maxwidth = 100, **colorArgs):
    """ color each string and return them on the same line until maxwidth then a
        newline is inserted.
        input can be a list of strings and colors
        or colorArgs can be red = ['this', 'phrase', 'hat', 'baseball'],
                            blue = ['etc...',] ""
        keyword colorArgs can be used to override color
        example:

        print(multi('this is a sentence of words'.split(),
                    ['red', 'blue', 'yellow', 89], white = 'this', bold=True))

    """
    if not sep: includesep = True
    if not includesep:
        try: colors = _insertSep(colors, '')+['']
        except IndexError: pass
        try: bgcolors = _insertSep(bgcolors, '')+['']
        except IndexError: pass
    if sep:
        if sepprofile: sep = _colorize(sep, **sepprofile)
        strings = _insertSep(strings, sep)
    else: sep = ''

    if reset: reset = RESET
    else: reset = ''

    lenStr = len(strings)
    colorMap = {i:'' for i in range(lenStr)}
    if colors:
        n = 0
        while n < lenStr:
            for clr in colors:
                if n == lenStr: break
                colorMap[n] = clr
                n += 1

    bgMap = {i:'' for i in range(lenStr)}
    if bgcolors:
        n = 0
        while n < lenStr:
            for clr in bgcolors:
                if n == lenStr: break
                bgMap[n] = clr#_resolve(clr)
                n += 1
    for clr, strs in colorArgs.items():
        if clr in STANDARD_COLORS:
            if type(strs) is str: strs = [strs,]
            try:
                for s in strs:
                    try: colorMap[strings.index(s)] = _resolve(clr)
                    except: pass
            except: pass
    line = ''

    n = 0
    width = 0
    for string in strings:
        width += len(string)
        if width > maxwidth:
            string += RESET+'\n'
            width = 0
        line += _colorize(string, colorMap[n], bgMap[n],
                      bold=bold,
                      reverse=reverse,
                      underscore=underscore,
                      score=score,
                      blink=blink,
                      concealed=concealed,
                      reset = False)
        n+=1
    return line + reset

class profile(dict):
    """ reusable color profile class for making resuable instances
        of the same text, colors, or attribute combinations.
        blueonblack = profile(color='blue', bgcolor='black')
        blueonblack.bold = True
        printer('this text', **blueonblack)) # ** unpacks the keyword args.
        can set any attribute for any acceptable argument to color or other
        function for that mattter.
        """
    def __setattr__(self, k, v):
        self.__setitem__(k,v)

    def __getattribute__(self, item):
        try:
            return self.__getitem__(item)
        except:
            return super(dict, self).__getattribute__(item)

    def __delattr__(self, name):
        del self[name]

    def string(self, *texts, **kwargs):
        """ the same as profile().print except returns a string and doesn't
            print"""
        s = profile(self.copy())
        s.update(kwargs)
        try: sep = s.pop('sep')
        except: sep = ' '
        if not texts and 'text' in s:
            texts = [s.pop('text'),]
        r = ''
        msep = ''
        if s.ismulti():
            if type(texts[0]) is list: msep = sep
            for text in texts[:-1]:
                r += s.multi(text, sep = msep)+RESET
                r+= sep
            r += s.multi(texts[-1], sep = msep)+RESET
            return r
        else:
            for text in texts[:-1]:
                r += _colorize(text, **s)
                r += sep
            r += _colorize(texts[-1], **s)
        return r

    def ismulti(self):
        if hasattr(self, 'colors') or hasattr(self, 'bgcolors'):
            return True
        return False

    def multi(self, *args, **kwargs):
        s = self.copy()
        s.update(kwargs)
        if not 'colors' in s and 'color' in s:
                s['colors']=[s['color'],]
        if not 'bgcolors' in s and 'bgcolor' in s:
                s['bgcolors']= [s['bgcolor'],]
        return multi(*args, **s)

    def print(self, *texts, **kwargs):
        s = profile(self.copy())
        s.update(kwargs)
        try: file = s.pop('file')
        except: file = sys.stdout
        try: flush = s.pop('flush')
        except: flush = False
        try: end = s.pop('end')
        except: end = '\n'
        try: sep = s.pop('sep')
        except: sep = ' '
        if not texts and 'text' in s:
            texts = [s.pop('text'),]
        if s.ismulti():
            for stringlist in texts:
                if type(stringlist) is list:
                    msep = sep
                else: msep = ''
                file.write(s.multi(stringlist, sep = msep)+RESET)
                file.write(sep)
            file.write(end)
            if flush: file.flush()
        else:
            cprinter(*texts, end = end, file = file, flush = flush, **s)

    def __add__(self, Profile):
        """ add operator overloading for adding profiles together
        returns a profile instance with the leftmost profile
        taking precedence and inherits any new attributes from
        the right profile that it did not have defined
        blue = profile(color = 'blue', bold = 1)
        green = profile(color = 'green', underscore = 1, bold = 0)
        greenunderscore = green + blue # still not bold
        greenunderscore.print('this', bold = 1) # override bold
        blue.print('this', **green) # same as profile().print('this', **green+blue)
        blueboldunderscore = blue + green"""
        return profile(Profile, **self)

    def merge(self, Profile):
        """ Modifies self to inherit any attributes from Profile that it does
            not already have defined.
            for redefinition of attributs use profile().update(Profile)"""
        self = self.__add__(Profile)


def printer(*texts, **kwargs):
    """ a catch-all print function, accepts multi colors or one color """
    profile(**kwargs).print(*texts)

def stringer(*texts, **kwargs):
    """ a proxy function to profile().string()
        accepts same arguments as function printer
        returns an escaped string
        ready for printing or inserting into a string with
        "foo {}".format(stringer('bar', bold = True))"""
    return profile(**kwargs).string(*texts)

def estring(text, color='', bgcolor='', **kwargs):
    """ single string color with positional color and bgcolor args
        for more convienient less verbose calls.. accepts attribute
        keywords too. like bold = True.

        cprint('this message', 'blue', 'black') # is the same as...
            blueonblack = profile(color='blue', bgcolor='black')
            cprint('this message', **blueonblack)  #  or...
                blueonblack.print('this message')
    """
    return profile(color=color, bgcolor=bgcolor, **kwargs).string(text)

def eprint(text, color='', bgcolor='', **kwargs):
    """ single string color print with positional color and bgcolor args
        for more convienient less verbose calls.. accepts attribute
        keywords too. like bold = True.

        cprint('this message', 'blue', 'black') # is the same as...
            blueonblack = profile(color='blue', bgcolor='black')
            cprint('this message', **blueonblack)  #  or...
                blueonblack.print('this message')
        """
    profile(color=color, bgcolor=bgcolor, **kwargs).print(text)

def _run_from_ipython():
    try:
        __IPYTHON__
        return True
    except NameError:
        return False

__doc__ = \
"""escapeaid v0.1 xTerm color escape api
shell usage:
with the enviroment variable 'escapeaid' set:
 escapeaid 'foo bar' black red bold underscore
 {foobarshell}
or...
 python3 -m escapeaid 'foo bar' black red bold underscore
 {foobarshell}
api usage:
for simplest usage use eprint:
>>> eprint('foo bar', 'red')
{foobar1}
>>> eprint('foo bar', 'black', 'blue', bold = True)
{foobar2}
 * eprint accepts 3 positional or keyword optional arguments:
        text, color, bgcolor
   as well as optional keyword attribute arguments:
   defaults :       bold = False
                    reverse = False
                    underscore = False
                    score = False
                    blink = False
                    concealed = False

to build custom strings or to use the literal escaped string in scripts,
the use of the stringer and estring functions will return an escaped string
and not print it.
All api functions accept an unpacked instance of profile as argument.
with estirng, stringer, eprint, printer, the instance must be unpacked like so:
eprint('foo bar', **fooprofile)
or
s = stringer('foo bar', **fooprofile+barprofile)
in the above example two profiles are unpacked and added together,
with the leftmost profile inheriting attributes from the right profile,
instance. With only new attributes inherited.

profile instances also have a built-in interface for convienient reuse,
profile().string and profile().print:
profile().print('foo bar', **barprofile) , is the functionally the same as:
    barprofile.print('foo bar')
    printer('foo bar', **barprofile)
    print(stringer('foo bar', **barprofile))
    print(barprofile.string('foo bar'))

The difference between printer and eprint or stringer and estring is the ability
accept the colors argument for mulitple colors, as well as a list of strings
rather than a single string for multi color distribution accross them is also
acceptable:

## with a list of strings the colors are distributed per string...
>>> printer('this is a mulit-colored sentence'.split(),
             colors=['red', 'blue', 'green', 'purple'],
             bgcolor = 'white', bold = True)
{multi1}
## with one string, the colors are distributed per charactor...
>>> printer('this is a mulit-colored sentence',
             colors=['red', 'blue', 'green', 'purple'],
             bgcolor ='white', bold = 1)
{multi2}

profile().print and profile().string will act the same as printer and stringer
and if the profile instace has a colors attribute profile().colors or profile.bgcolors()
these will be used rather than profile().color or profile().bgcolor
if only one of the .colors or .bgcolors are defined then the it will look to
.color or .bgcolor for a single color to use with the multi foreground or
background.

""".format(\
   profile = estring('profile', bold=True),
   cprint = estring('cprint', bold=True),
   foobarshell = estring('foo bar','black', 'red', bold = True, underscore = True),
   foobar1 = estring('foo bar', 'red'),
   foobar2 = estring('foo bar', 'black', 'blue', bold =True),
   foobar3 = estring('foo bar', 'blue', 'black') ,
   foobar3bold = estring('foo bar', 'blue', 'black', bold =True) ,
   foobar4 = multi('foo bar', colors=['blue', 'cyan'], sep = ''),
   multi1 = stringer('this is a mulit-colored sentence'.split(),
                     colors=['red', 'blue', 'green', 'purple'],
                     bgcolor = 'white', bold = True),
   multi2 = stringer('this is a mulit-colored sentence',
                     colors=['red', 'blue', 'green', 'purple'],
                     bgcolor = 'white', bold=True ),
   foobar5 = estring('foo bar', 'red', 'green'),
   foobar6 = profile({'colors': ['blue', 'cyan'],
                      'bgcolor': 'black',
                      'bold':True,'underscore': True}).string('foo bar test'),
   foobar7 = None
   )
def isnumeric(x):
    try:
        int(x)
        return True
    except: return False

def argCheck(arg, result, colors):
    if arg in STANDARD_COLORS or isnumeric(arg):
        colors.append(arg)
    elif arg in ['bold', 'underscore', 'score', 'blink', 'reverse', 'concealed']:
        result[arg] = True
    return result, colors

def fromShell(*args):
    """ prints arguments from call to escapeaid directly from the shell
        example: python3 -m escapeaid 'foo bar' black red bold underscore"""

    if args[0][0] == '-':
        args = list(args)
        arg1 = args.pop(0)
        if arg1 in ['--picker', '-p']:
            if args:
                try:
                    picker(args.pop(0))
                except:
                    picker()
            else: picker()
            return
    args = list(args)
    colors = []
    result = profile(text=args.pop(0))
    for arg in args:
        result, colors = argCheck(arg, result, colors)
    if colors:
        result.color = colors.pop(0)
    if colors:
        result.bgcolor = colors.pop(0)
    result.print()

def helpDocs():
    print(__doc__)
if __name__ == '__main__':
    """   blueonblack = profile(color='blue', bgcolor='black')
    blueonblack.print('foo bar')

    blueonblack.bold = True
    printer('foo bar', **blueonblack)

    blueonblack.colors = ['blue', 'cyan']
    blueonblack.print('foo bar')

    redongreen = profile(color='red', bgcolor='green', underscore=True)
    redongreen.print('foo bar')
    printer(**blueonblack+redongreen)
    redongreen.update(blueonblack)
    redongreen.print('foo bar')"""
    if len(sys.argv) > 1:
        if sys.argv[1] in ['-h', '--help']: helpDocs()
        else:
            try:
                fromShell(*[i.strip('\'').strip('\"') for i in sys.argv[1:]])
            except: helpDocs()

    elif sys.flags.interactive or _run_from_ipython():
        greys = list(range(238,250))
        b = '233 '*25
        b = b.split(' ')
        blackspace = [int(i) for i in b if i]
        gradient = list(reversed(greys))+ blackspace + list(reversed(greys))
        gradient = profile(bgcolors = gradient, colors = [13,12, 111, 80])
        gradient.bold = True
        gradient.sep = ''
        message = '             ...<<< EscapeAID                                    '
        nmessage= '                  interactive >>>...                             '
        hf = ' '*len(message)
        gradient.print(hf)
        gradient.print(message)
        gradient.print(nmessage)
        gradient.print(hf)
        try:
            assert 'xterm' in TERM
        except AssertionError:
            cprint('Warning', 'red', bold = True, end= ' ')
            cprint('could not confirm terminal is Xterm', 'yellow', 'black', bold =True)
            cprint('but if this is red you should be ok !', 'red')
