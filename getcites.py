#!/usr/local/bin/python3

# GetCites
# --------
# cp 2019
# Extracts everything that looks like a citation from a text file

from argparse import ArgumentParser
from ODTReader.odtreader import odtToText
from collections import OrderedDict
from pathlib import Path
import re

def get_author(string):
    authorMatch = re.search('[A-Z][^\s]*', string)
    return authorMatch.group() if authorMatch else '' 

def get_year(string):
    yearMatch = re.search('\d{2,4}', string)
    return int(yearMatch.group()) if yearMatch else 0

def get_author_year(string):
    return (get_author(string), get_year(string))

def distinct_by_key(key, iterable, first=True):
    "Returns distinct values, using a key function to determine distinctness"
    it = reversed(iterable) if first else iterable
    distinct = OrderedDict((key(i), i) for i in it).values()
    return reversed(distinct) if first else distinct

def tidy(string):
    return re.sub('\s+', ' ', string).strip()

def trim_cite(string):
    "Returns from the first capitalized word to the last parentheses, if possible"
    citeMatch = re.search('[A-Z\(].*\)', string)
    return citeMatch.group() if citeMatch else string

def pagenum(string):
    "Extracts page numbers from citations. Fails to find roman numerals because I don't care."
    pageMatch = re.search('\(\s*p{1,2}\.?\s*(\d+)\s*\)', string)
    return int(pageMatch.group(1)) if pageMatch else None

if __name__ == '__main__':
    parser = ArgumentParser("Extract citations from a text file")
    parser.add_argument("source")
    parser.add_argument("-f", "--format", default="odt", choices=["odt", "text"], help='Input format')
    parser.add_argument('-n', '--narrative_order', action='store_true', help='Show citations in narrative order (default is sorted by author and year)')
    parser.add_argument('-t', '--trim', action='store_true', help='Trim to just the citation')
    parser.add_argument('-d', '--distinct', action='store_true', help='Return entries with distinct author and year value')
    parser.add_argument('-B', '--words_before', type=int, default=4, help='Number of words to select before the parenthesis')
    parser.add_argument('-C', '--words_after', type=int, default=2, help='Number of words to select after the parenthesis')
    args = parser.parse_args()

    if args.format == "odt":
        text = odtToText(args.source)
    elif args.format == "text":
        text = Path(args.source).read_text()
    pattern = '[^\s]+\s*' * args.words_before + '\(.*?\)' + '\s*[^\s]+' * args.words_after
    cites = re.findall(pattern, text)
    cites = filter(lambda c: pagenum(c) is None, cites)
    if not args.narrative_order:
        cites = sorted(cites, key=get_author_year)
    if args.distinct:
        cites = distinct_by_key(get_author_year, cites)
    for cite in cites:
        if args.trim:
            print(trim_cite(tidy(cite)))
        else:
            print(tidy(cite))
            
