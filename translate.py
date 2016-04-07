#!/usr/bin/env python3
# Copyright 2016 Canonical Ltd.
# Written by:
#   Maciej Kisielewski <maciej.kisielewski@canonical.com>
#
# This is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3,
# as published by the Free Software Foundation.
#
# This file is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this file.  If not, see <http://www.gnu.org/licenses/>.
"""
translate.py FILE

Run a simple string substitutions.
Substitutions are done in place.
Every file mentioned in a spec is copied to $FILE.orig.
If .orig file already exists, it will be used as the source for translations,
and it will not be overwritten.

FILE should be a file with three \t seperated columns.
First column should specify a file which should be translated. If empty, the
last specified will be used.
Second column specifies a string to replace.
Third column specifies what string to replace it with.

I.e.:
foo.file\tfoo\tBOO
\tfoobar\tBOOBAZ
bar.file\t;-)\t(-;
\t:-)\t(-:

Note that the longest string will be translated, so in foo.file foobar gets
precedence over foo
"""

from collections import OrderedDict
import os
import shutil
import sys


def main():
    the_dict = OrderedDict()
    if len(sys.argv) != 2:
        print('Usage: {} FILE'.format(sys.argv[0]))
        return
    with open(sys.argv[1], 'rt') as f:
        filename = ''
        for liennum, line in enumerate(f.readlines(), 1):
            fields = line.rstrip().split('\t')
            if len(fields) == 3:
                first = fields.pop(0)
                if first:
                    filename = first
                    the_dict[filename] = OrderedDict()
            assert(len(fields) == 2)
            assert(filename)
            the_dict[filename][fields[0]] = fields[1]

    for filename, tr in the_dict.items():
        orig = filename + '.orig'
        if not os.path.exists(orig):
            shutil.copy(filename, orig)
        translate_file(orig, filename, tr)


def translate_file(origfile, trfile, dic):
    with open(origfile, 'rt') as orig:
        with open(trfile, 'wt') as tr:
            for line in orig:
                tr.write(translate_line(line, dic))


def translate_line(line, dic):
    for key in sorted(dic.keys(), key=lambda x: len(x), reverse=True):
        if line.find(key) >= 1:
            if key == dic[key]:
                continue
            translated = line.replace(key, dic[key])
            return translate_line(translated, dic)
    return line

if __name__ == '__main__':
    main()
