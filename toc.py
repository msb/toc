#!/usr/bin/env python

"""
Produces a table of contents for the set of PDF files found in <pages_dir> (each assumed to be a
chapter). The title and number of pages of each PDF is inferred from the file name as follows:

    - {TOC entry}[#{no of pages}].pdf
    - {TOC entry}[#{no of pages}].pdf
    -  :
    - {TOC entry}[#{no of pages}].pdf

The TOC pages will be written to <pages_dir> and be named:

    - 01.toc.html
    - 02.toc.html
    -  :

Note that:
    - if no of pages hashes is omitted, it is assumed to be 1.
    - the order is alphabetic (case insensitive)

Usage:
  toc.py <pages_dir> [--toc-rows=<rows>] [--toc-cols=<cols>]
  toc.py -h | --help

Options:
  -h --help          Show this screen.
  --toc-rows=<rows>  The max number of TOC rows [default: 50].
  --toc-cols=<cols>  The max number of TOC cols [default: 3].
  <pages_dir>        The folder containing the book pages.
"""

import os
import os.path as path
import math
from typing import List, TextIO, Tuple
from docopt import docopt

# A CSS style sheet for the TOC.
STYLE = """
  td {
    font-size: 10px;
  }
  table tr td:nth-child(2), td:nth-child(4), td:nth-child(6), td:nth-child(8), td:nth-child(10) {
    padding-right: 8px;
  }
"""


def main(args):

    # define the parameters
    pages_dir = args['<pages_dir>']
    toc_rows = int(args['--toc-rows'])
    toc_cols = int(args['--toc-cols'])

    title_page_length, entries = get_entries(pages_dir)

    # Calculate the entries per page and the number of TOC pages.
    entries_per_page = toc_rows * toc_cols
    toc_pages = math.ceil(len(entries) / entries_per_page)

    counted_entries: List[Tuple[str, int]] = []
    # initialise the `page_no` counter
    page_no = toc_pages + title_page_length + 1

    # create a list of counted entries: each being title and page no.
    for title, length in entries:
        counted_entries.append((title, page_no))
        page_no += length

    # for each TOC page ..
    for page in range(toc_pages):
        # .. write an HTML table to a file and ..
        toc_html_name = path.join(pages_dir, f'{(page + 1):02d}.toc.html')
        with open(toc_html_name, 'w') as toc_html_fd:
            write_toc_html(
                toc_html_fd, toc_rows, toc_cols, entries_per_page, page, counted_entries
            )


def write_toc_html(
    # text file object
    toc_html_fd: TextIO,
    # the max numbers of TOC rows in a page
    toc_rows: int,
    # the max numbers of TOC cols in a page
    toc_cols: int,
    # the max number of entries per page (toc_rows * toc_cols)
    entries_per_page: int,
    # the index of the page being written to
    page: int,
    # a list of counted entries: each being title and page no.
    counted_entries: List[Tuple[str, int]]
):
    """
    This function writes a list of TOC entries as an HTML page to a file object.
    The function has to transpose the entries.
    """
    toc_html_fd.write(f'<html><head><style>{STYLE}</style></head><body><table>')

    for row in range(toc_rows):
        toc_html_fd.write('<tr>')
        for col in range(toc_cols):
            index = row + col * toc_rows + entries_per_page * page
            if index < len(counted_entries):
                title, page_no = counted_entries[index]
                toc_html_fd.write(f'<td>{title}</td><td>{page_no}</td>')
        toc_html_fd.write('</tr>')

    toc_html_fd.write('</table></body></html>')


def get_entries(pages_dir: str) -> Tuple[int, List[Tuple[str, int]]]:
    """
    This function lists all the PDF's in `pages_dir` in alphabetic order and returns
    a `Tuple` of the length of the book's title page and a `List` of tuples
    each of which represents the name of the PDF to be used in the TOC and it's number of pages.
    The expected PDF format is {TOC entry}[#{no of pages}].pdf and
    the expected title page format is 00.{title}[#{no of pages}].pdf .
    """
    title_page_length, entries = (0, [])

    for file_name in sorted(os.listdir(pages_dir), key=lambda k: k.lower()):
        file_root, file_ext = os.path.splitext(file_name)
        if file_ext == '.pdf':
            file_root_parts = file_root.split('#')
            length = 1
            title = file_root_parts[0]
            # parse length
            if len(file_root_parts) > 1:
                length = int(file_root_parts[1])
            # append the entry unless it's a title page or an existing TOC
            if title.startswith('00.'):
                title_page_length = length
            elif not title.endswith('.toc'):
                entries.append((title, length))

    return title_page_length, entries


if __name__ == '__main__':
    main(docopt(__doc__))
