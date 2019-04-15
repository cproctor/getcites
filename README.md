# GetCites

A command line utility for automating tedious citation work. GetCites can extract everything that 
looks like a citation from a text file.

## Usage

'''
usage: Extract citations from a text file [-h] [-f {odt,text}] [-n] [-t] [-d]
                                          [-B WORDS_BEFORE] [-C WORDS_AFTER]
                                          source

positional arguments:
  source

optional arguments:
  -h, --help            show this help message and exit
  -f {odt,text}, --format {odt,text}
                        Input format
  -n, --narrative_order
                        Show citations in narrative order (default is sorted
                        by author and year)
  -t, --trim            Trim to just the citation
  -d, --distinct        Return entries with distinct author and year value
  -B WORDS_BEFORE, --words_before WORDS_BEFORE
                        Number of words to select before the parenthesis
  -C WORDS_AFTER, --words_after WORDS_AFTER
                        Number of words to select after the parenthesis
'''

