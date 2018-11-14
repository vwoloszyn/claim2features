

def treat_text(text, removes=['\n', '\r', '\t'], strip=True):
    if type(text) == list:
        text_ = []
        for t in text:
            text_.append(treat_text(t))
        return text_
    text_ = text
    for remove in removes:
        text_ = text_.replace(remove, ' ')
    if strip:
        text_ = text_.strip()
    return text_


def pure_words(text, dividers=['-', '_'], uppercase=True, low_upper=True):
    "Split a word in words. For example 'main_container' or 'mainContainer' -> 'main container'."

    upper = list('ABCDEFGHIJKLMNOPQRSTUVWYZ')
    text_ = ''
    last_space = True
    for c in text:
        if not last_space:
            if c in dividers:
                text_ += ' '
            elif uppercase and c in upper:
                c_ = c
                if low_upper:
                    c_ = c.lower()
                text_ += ' ' + c_
            else:
                text_ += c
        else:
            if c not in dividers:
                text_ += c
        if c == ' ':
            last_space = True
        else:
            last_space = False
    return text_


def words_count(sentence, split=[' ', '\t', '\n', '\r']):
    for s in split:
        sentence.replace(s, ' ')
    return len(sentence.strip().split(' '))
