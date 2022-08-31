# Title Case

def title(text, ignore=['in', 'the', 'of', 'with', 'or', 'and']):
    return ' '.join(w[0].upper()+w[1:] if w not in ignore else w for w in text.split(' '))

title('trends in machine learning')
