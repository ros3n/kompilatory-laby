#! -*- coding: utf-8 -*-


import os
import sys
import re
import codecs
import itertools


def parse_meta(key, content):
    pattern = re.compile(r'<META NAME="{0}" CONTENT="(.*?)">'.format(key))
    res = pattern.findall(content)

    if res:
        res = filter(lambda x: len(x), res)
        return ", ".join(res)
    else:
        return None


def get_data(content):
    pattern = re.compile(r'^(<P>.*</P>)$', re.DOTALL | re.MULTILINE)
    res = pattern.search(content)

    return res.group(1) if res else None


def parse_floating(content):
    pattern = re.compile(r'((\d*\.\d+|\d+\.\d*)((e|E)(\+|-)?\d+)?)[^$]')
    return pattern.findall(content)


def parse_mails(content):
    pattern = re.compile(r'([a-zA-Z0-9]+(\.[a-zA-Z0-9]+)?@[a-zA-Z0-9]+(\.[a-zA-Z0-9]+)+)')
    return pattern.findall(content)


def parse_abbreviations(content):
    data = get_data(content)
    res = re.sub(r'<.*?>', '', data)
    abbr = lambda x: re.findall(r'(?:^|\s)([a-zA-Z]{1,3}\.)(?!$|\s[A-Z])', x)
    abbrs = filter(lambda x: bool(x), map(abbr, [r.strip() for r in res.split('\n')]))
    res = set(itertools.chain(*abbrs))
    return res


def parse_dates(content):
    month_lengths = (
        ('3(0|1)', ('01', '03', '05', '07', '08', '10', '12')),
        ('30', ('04', '06', '09', '11')),
        ('29', ('02',)),
    )

    days = r'(0[1-9]|[1-2][0-9]|{0})'
    months = r'({0})'
    years = r'\d\d\d\d'
    pattern = r'({0}(\.|/|-){1}(\.|/|-){2})'

    patterns_eu = map(
        lambda x: pattern.format(days.format(x[0]), months.format('|'.join(x[1])), years),
        month_lengths
    )

    patterns_us = map(
        lambda x: pattern.format(years, days.format(x[0]), months.format('|'.join(x[1]))),
        month_lengths
    )

    date_pattern = '{0}|{1}'.format('|'.join(patterns_eu), '|'.join(patterns_us))

    res = re.findall(date_pattern, content)
    dates = []
    for r in res:
        dates.extend(filter(lambda x: len(x) > 2, r))

    delimiters = '[-/.]'
    date_set = {tuple(re.split(delimiters, date)) for date in dates}
    return date_set


def parse_ints(content):
    patterns = [
        r'3276[0-7]',
        r'327[0-5]\d',
        r'32[0-6]\d\d',
        r'3[0-1]\d\d\d',
        r'[1-2]\d\d\d\d',
        r'\d{1,4}',
    ]

    pattern = r'((-?({0}))|(-32768))'.format("|".join(patterns))
    return re.findall(pattern, content)


def parse_sentences(data, abbrs):
    data = re.sub(r'<.*?>', '', data)
    delimiters = '\s' + '\s|\s'.join(abbrs) + '\s'
    delimiters.replace('.', '\.')
    data = re.sub(delimiters, '', data)
    data = filter(lambda x: len(x) > 3 and x.strip(), re.split('[.?!\n]', data))
    return data


def process_file(filepath):
    fp = codecs.open(filepath, 'rU', 'iso-8859-2')

    content = fp.read()

#
#  INSERT YOUR CODE HERE
#

    data = get_data(content)

    fp.close()
    print "nazwa pliku:", filepath
    print "autor:", parse_meta('AUTOR', content)
    print "dzial:", parse_meta('DZIAL', content)
    print "slowa kluczowe:", parse_meta('KLUCZOWE_\d+', content)
    abbrs = parse_abbreviations(data)
    print "liczba zdan:", len(parse_sentences(data, abbrs))
    print "liczba skrotow:", len(abbrs)
    print "liczba liczb calkowitych z zakresu int:", len(parse_ints(data))
    print "liczba liczb zmiennoprzecinkowych:", len(parse_floating(data))
    print "liczba dat:", len(parse_dates(data))
    print "liczba adresow email:", len(parse_mails(data))
    print "\n"

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
