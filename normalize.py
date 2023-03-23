import string


CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", 
               "y", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", 
               "ya", "je", "i", "ji", "g")

TRANS = {}

for c, t in zip(CYRILLIC_SYMBOLS, TRANSLATION):
    TRANS[ord(c)] = t
    TRANS[ord(c.upper())] = t.upper()


def normalize(filename):
    valid_chars = '-_.() %s%s' % (string.ascii_letters, string.digits)
    print(f'Before transliteration: {filename}')
    filename = filename.translate(TRANS)
    filename = ''.join(c for c in filename if str(c) in valid_chars)
    print(f'After transliteration: {filename}')
    return filename

if __name__ == '__main__':
    print(normalize("Білі?мухи-налетіли№."))