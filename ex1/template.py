
import os
import sys
import re
import codecs


def parse_meta(key, content):
    pattern = re.compile('<META NAME="{0}" CONTENT="(.*?)">'.format(key))
    res = pattern.findall(content)

    if res:
        res = filter(lambda x: len(x), res)
        return ", ".join(res)
    else:
        return None


def process_file(filepath):
    fp = codecs.open(filepath, 'rU', 'iso-8859-2')

    content = fp.read()

#
#  INSERT YOUR CODE HERE
#

    fp.close()
    print("nazwa pliku:", filepath)
    print("autor:", parse_meta('AUTOR', content))
    print("dzial:", parse_meta('DZIAL', content))
    print("slowa kluczowe:", parse_meta('KLUCZOWE_\d+', content))
    print("liczba zdan:")
    print("liczba skrotow:")
    print("liczba liczb calkowitych z zakresu int:")
    print("liczba liczb zmiennoprzecinkowych:")
    print("liczba dat:")
    print("liczba adresow email:")
    print("\n")

if __name__ == '__main__':

    try:
        path = sys.argv[1]
    except IndexError:
        print("Brak podanej nazwy katalogu")
        sys.exit(0)

    tree = os.walk(path)

    for root, dirs, files in tree:
        for f in files:
            if f.endswith(".html"):
                filepath = os.path.join(root, f)
                process_file(filepath)
