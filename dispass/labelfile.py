'''Dispass labelfile handler'''

# Copyright (c) 2011-2012 Benjamin Althues <benjamin@babab.nl>
#
# Permission to use, copy, modify, and distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

import os
from os.path import expanduser


class FileHandler:
    '''Parsing of labelfiles and writing to labelfiles'''

    default_length = 30
    '''Default passphrase length'''

    algorithm = 'dispass1'
    '''String. The algorithm to use, default is dispass1'''

    filehandle = None
    '''File object, set on init if labelfile is found'''

    file_found = None
    '''Boolean value set on init'''

    file_location = None
    '''String of labelfile location, set on init'''

    file_stripped = []
    '''Labelfile contents with comments and blank lines removed'''

    labels = None
    '''Dict of `{label: length}`'''

    def __init__(self, write=False, file_location=None):
        '''Open file; if file is found: strip comments and parse()'''

        if file_location:
            self.file_location = file_location
        else:
            self.file_location = self.getDefaultFileLocation()

        try:
            if write:
                self.filehandle = open(expanduser(self.file_location), 'r+')
            else:
                self.filehandle = open(expanduser(self.file_location), 'r')
            self.file_found = True
        except IOError:
            self.file_found = False
            return

        # Strip comments and blank lines
        for i in self.filehandle:
            if i[0] != '\n' and i[0] != '#':
                self.file_stripped.append(i)

        if self.file_found:
            if not write:
                self.close()
            self.parse()

    def getDefaultFileLocation(self):
        """Scan default labelfile paths"""

        if os.getenv('DISPASS_LABELFILE'):
            return os.getenv('DISPASS_LABELFILE')
        elif os.getenv('XDG_DATA_HOME'):
            return os.getenv('XDG_DATA_HOME') + '/dispass/labels'
        else:
            return '~/.local/share/dispass/labels'

    def parse(self):
        '''Create dictionary of ``labels = {label: length, ...}``'''

        labels = []
        labels_dispass1 = []

        for i in self.file_stripped:
            wordlist = []
            line = i.rsplit(' ')
            for word in line:
                if word != '':
                    wordlist.append(word.strip('\n'))
            labels.append(wordlist)

        for line in labels:
            labelname = line.pop(0)
            length = self.default_length
            algo = self.algorithm

            for arg in line:
                if 'length=' in arg:
                    try:
                        length = int(arg.strip('length='))
                    except ValueError:
                        print "Warning: Invalid length in: '%s'" % line
                elif 'algo=' in arg:
                    algo = arg.strip('algo=')

            if algo == 'dispass1':
                labels_dispass1.append((labelname, (length, )))

        self.labels = dict(labels_dispass1)
        return self

    def close(self):
        '''Explicitly close filehandle'''
        if self.filehandle:
            self.filehandle.close()

    def search(self, search_string):
        '''Search for substring in labelfile

        :Parameters:
            - `search_string`: String to search for

        :Returns: Boolean False, Integer or Dict

        Searches all labels to find ``search_string`` as a substring of each
        label.

        If no matches are found, return False.
        If multiple matches are found, return Integer of number of matches
        If a unique match is found a dict of ``{label, passphrase_length}``
        is returned.
        '''
        found = []
        count = 0

        for label, length in self.labels.iteritems():
            if search_string in label:
                found.append(label)
                found_length = length
                count += 1

        if not found:
            return False

        if count > 1:
            return count

        return {found.pop(): found_length}

    def getLongestLabel(self):
        '''Return length of longest label name'''
        return len(max(self.labels.keys(), key=len))

    def printLabels(self, fixed_columns=False):
        '''Print a formatted table of labelfile contents

        :Parameters:
            - `fixed_columns`: Boolean.

        If fixed columns is true the output will be optimized for easy
        parsing by other programs and scripts by not printing the header
        and always printing one entry on a single line using the
        following positions:

        * Column 1-50: label (50 chars)
        * Column 52-54: length (3 chars wide)
        * Column 56-70: hash algo (15 chars wide)

        If fixed columns is false an ascii table is printed with a variable
        width depending on the length of the longest label. The table has
        a header but does not display the hash algo until support for multiple
        hashing algos is added.
        '''
        if fixed_columns:
            for label, length in self.labels.iteritems():
                print '{:50} {:3} {:15}'.format(label[:50], str(length)[:3],
                                                "dispass1")
        else:
            divlen = self.getLongestLabel()

            print '+-{:{fill}}-+--------+'.format('-' * divlen, fill=divlen)
            print '| {:{fill}} | Length |'.format('Label', fill=divlen)

            print '+-{:{fill}}-+--------+'.format('-' * divlen, fill=divlen)
            for label, length in self.labels.iteritems():
                print '| {:{fill}} |    {:3} |'.format(label, length,
                                                       fill=divlen)
            print '+-{:{fill}}-+--------+'.format('-' * divlen, fill=divlen)


if __name__ == '__main__':
    fh = FileHandler(write=True)

    if fh.file_found:
        if fh.write():
            print 'Saved to %s' % fh.file_location
        else:
            print 'No labels found'
    else:
        print 'Labelfile not found'
