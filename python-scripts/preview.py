#!/usr/bin/env python3
from __future__ import print_function
import codecs
import os.path
import sys

from docutils import core

# If Python 3, get a binary STDOUT
if sys.version_info >= (3,):
    sys.stdout = sys.stdout.detach()

# Make STDOUT utf-8
sys.stdout = codecs.getwriter('utf8')(sys.stdout)

def main(argv=None):
    # Some sanity checks on if the path exists.
    filepath = argv[1] if argv is not None else sys.argv[1]
    filepath = os.path.abspath(filepath)
    if not os.path.exists(filepath):
        return 'File Not Found'

    writer_name = argv[2] if argv is not None else sys.argv[2]

    # open in binary, decode utf-8, and live in unicode
    with codecs.open(filepath, 'r', 'utf8') as f:
        page_string = f.read()

    html_inc = ''
    rst_inc = ''
    last_dir = '//\\//\\'
    cur_dir = filepath
    while last_dir != cur_dir:
        conf_file = cur_dir + '-doc-inc.html'
        if os.path.exists(conf_file):
            with codecs.open(conf_file, 'r', 'utf8') as f:
                html_inc = f.read()
        conf_file = cur_dir + '-doc-inc.rst'
        if os.path.exists(conf_file):
            with codecs.open(conf_file, 'r', 'utf8') as f:
                rst_inc = f.read()
        last_dir = cur_dir
        cur_dir = os.path.dirname(cur_dir[0:-1]) + '/'

    overrides = {
        'initial_header_level': 1,
        'halt_level': 5,
    }

    parts = core.publish_parts(
        source=rst_inc + page_string,
        source_path=filepath,
        writer_name=writer_name,
        settings_overrides=overrides,
    )

    part_name = argv[3] if argv is not None else sys.argv[3]
    html_document = parts[part_name]
    html_document = html_document.replace('\ufeff', '')

    # the REAL print function in python 2, now... see top of file
    print(html_inc + html_document)

if __name__ == '__main__':
    sys.exit(main(sys.argv))
