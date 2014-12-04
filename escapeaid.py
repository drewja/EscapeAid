#!/usr/bin/python3
# escapeaid.py

# Escape Aid  v0.1
# # xterm 256 color escaping made easy


# this is free software... liscense : gpl V2.0
# written and maintained by Andrew J. Arendt
#   andrewarendt@gmail.com
#    github.com/drewja/escapeaid


import sys
import os
TERM = os.getenv('TERM')

from static import CODE_MAP
from static import STANDARD_COLORS
from static import PALLET_256
from static import COLORS_256
from static import COLOR_GROUP_256
from static import RESET
from static import FSTRING

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

def escape(
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

def colorize(text, color = '', bgcolor = '', **profile):
    """ applies escapes to text based on keyword arguments
       and returns a printable string"""
    try: reset = profile.pop('reset')
    except KeyError: reset = True
    if reset: reset = RESET
    else: reset = ''
    escapes = escape(color, bgcolor, **profile)
    return escapes + text + reset

def cprinter(*args, csep = ' ', sep = '', end = '\n', file = sys.stdout,
            flush = False, **kwargs):
    """ print function combined with colorize function
    can be used with or without color arguments
    optional arguments csep is a string to be colored and placed between
    args, and sep is same thing but will not be colored with the texts.
    define sep or csep but both will ignore csep in favor of sep"""
    output = ''
    if sep: csep = ''
    if csep: sep = colorize(csep, **kwargs)
    for text in args:
        output += colorize(text, **kwargs) + sep
    file.write(output[:-len(sep)]+end)
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
            and pink text on  background colorized to the cooresponding color.
        """
    if not basecolors:
        for i in COLORS_256:
            i = ' '+ ' '*(3-len(str(i))) + str(i)+' '
            print(color(i,i,'black',reverse=True),
                  color('   '+ text +'   ',
                  i, bg, reverse = reverse), color(i, i))
    else:
        for c in basecolors:
            if c not in PALLET_256: continue
            for v in PALLET_256[c]:
                sv = str(v)
                sv = ' ' + ' '*(3-len(str(sv))) + str(sv)+' '
                print(color('  '+c+'  ', v, bg, reverse = reverse),
                      color(sv,v,'black',reverse=True),
                      color('   '+ text + '   ',
                      v, bg, reverse = reverse), color(sv, v))

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
    """ defaults to rainbow colors, same as multi but colorizes preceeding
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

def multi(strings, colors =[], bgcolors = [], sepcolor = '', sep = ' ',
         bold = False,
         reverse = False,
         underscore = False,
         score = False,
         blink = False,
         concealed = False, reset = True, maxwidth = 100, **colorArgs):
    """ colorize each string and return them on the same line until maxwidth then a
        newline is inserted.
        input can be a list of strings and colors
        or colorArgs can be red = ['this', 'phrase', 'hat', 'baseball'],
                            blue = ['etc...',] ""
        keyword colorArgs can be used to override color
        example:
        
        print(multi('this is a sentence of words'.split(),
                    ['red', 'blue', 'yellow', 89], white = 'this', bold=True))

    """
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
    if sep:
        if sepcolor: sep = colorize(sep, bgcolor = sepcolor, reset=False)
    else: sep = ''
    n = 0
    width = 0
    for string in strings:
        width += len(string)
        if width > maxwidth:
            string += RESET+'\n'
            width = 0
        elif n != len(strings)-1: string += sep
        line += colorize(string, colorMap[n], bgMap[n],
                      bold=bold,
                      reverse=reverse,
                      underscore=underscore,
                      score=score,
                      blink=blink,

                      concealed=concealed,
                      reset = False)# + sep
        n+=1
    lensep = len(sep)
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

    def string(self, text):
        return escape(**self)+text+RESET
    
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

        if not texts and 'text' in s:
            texts = [s.pop('text'),]        
        if s.ismulti():
            for stringlist in texts:
                file.write(s.multi(stringlist)+RESET+end)
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

def printer(*texts, color = '', bgcolor = '', **kwargs):
    """ a catch-all print function, accepts multi colors or one color """
    profile(**kwargs).print(*texts)

def cprint(string, color='', bgcolor='', **kwargs):
    """ single string color print with positional color and bgcolor args
        for more convienient less verbose calls.. accepts attribute
        keywords too. like bold = True.
        
        cprint('this message', 'blue', 'black') # is the same as...
            blueonblack = profile(color='blue', bgcolor='black')
            cprint('this message', **blueonblack)  #  or...
                blueonblack.print('this message')
        """
    profile(color=color, bgcolor=bgcolor, **kwargs).print(string)
    
def _run_from_ipython():
    try:
        __IPYTHON__
        return True
    except NameError:
        return False            
if __name__ == '__main__':
    if sys.flags.interactive or _run_from_ipython():
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
