import glob
import os
from pathlib import Path


try:
    import readline
except ModuleNotFoundError:
    print('If you are on windows, you can install pyreadline to have the same functionnalities as readline.')
    raise

HOME = str(Path.home())


def prompt_autocomplete(prompt, complete, default=None):
    """
    Prompt a string with autocompletion

    :param complete: A function that returns a list of possible strings that
        should be completed on a given text. 
        def complete(text: str) -> List[str]: ...
    """

    def real_completer(text, state):
        possibilities = complete(text) + [None]

        if possibilities:
            return possibilities[state]
        return None

    readline.set_completer_delims(' \t\n;')
    readline.parse_and_bind("tab: complete")
    readline.set_completer(real_completer)

    if default is not None:
        r = input('%s [%s]: ' % (prompt, default))
    else:
        r = ''
        while not r:
            r = input('%s: ' % prompt)

    r = r or default

    # remove the autocompletion before quitting for future input()
    readline.parse_and_bind('tab: self-insert')
    readline.set_completer(None)

    return r


def prompt_file(prompt, default=None):
    def complete(text):
        text = text.replace('~', HOME)

        suggs = glob.glob(text + '*')

        if suggs:
            for i, sugg in enumerate(suggs):

                sugg = sugg.replace(HOME, '~')
                sugg = sugg.replace('\\', '/')

                if os.path.isdir(sugg) and not sugg.endswith('/'):
                    sugg += '/'

                suggs[i] = sugg

        return suggs
    
    return prompt_autocomplete(prompt, complete, default)


def prompt_choice(prompt, possibilities, default=None):
    assert len(possibilities) >= 1
    assert default is None or default in possibilities

    def complete(text):
        return [t for t in possibilities if t.startswith(text)]

    r = prompt_autocomplete(prompt, complete, default)
    while r not in possibilities:
        print('%s is not a possibility.' % r)
        r = prompt_autocomplete(prompt, complete, default)

    return r


__all__ = ['prompt_autocomplete', 'prompt_file', 'prompt_choice']