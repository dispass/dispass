# Copyright (c) 2011, 2012, 2013  Benjamin Althues <benjamin@babab.nl>
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

from collections import OrderedDict
import getopt


def stripargstring(string):
    '''Strip 'argument specifiers' from a string.

    :Parameters:
        - `string`: String in- or exluding '=' and/or ':'`

    :Return:
        - String without '=' and ':' chars
    '''
    return string.replace(':', '').replace('=', '')


class CommandBase(object):
    '''Base class for (sub)commands'''

    usagestr = 'usage: dispass subcommand [options]'
    '''String. Usage synopsis'''

    description = ''
    '''String. Small description of subcommand'''

    optionList = {}
    '''Dictionary of options (as list of 2-tuples).
    This will be transformed to an OrderedDict when initializing the object.

    Example::

        optionList = (
            ('help', ('h', 'show this help information')),
            ('dry-run', ('n', 'only print output without actually running')),

            # Append = and : to specify that the option requires an argument
            ('file=', ('f:', 'use specified file')),

            # Use an empty string to ommit short option
            ('debug', ('', 'show debug information')),
        )

    '''

    usageTextExtra = ''
    '''String. Optional extra usage information'''

    def __init__(self, settings, argv):
        '''Initialize (sub)command object

        :Parameters:
            - `settings`: Instance of `dispass.dispass.Settings`
            - `argv`: List of arguments. E.g. `sys.argv[1:]`
        '''

        # Instance vars
        self.error = None
        '''Thrown by GetoptError when parsing illegal arguments.'''

        self.flags = {}
        '''Dict of parsed options and corresponding arguments, if any.'''

        self.usage = ''
        '''String with usage information

        The string is compiled using the values found for
        `usagestr`, `description`, `optionList` and `usageTextExtra`.
        '''

        self.optionList = OrderedDict(self.optionList)
        self.settings = settings

        # Local vars
        longopts = []
        shortopts = ''

        # Create usage information and build dict of possible flags
        opthelp = ''
        for flag, val in self.optionList.iteritems():
            longopts.append(flag)
            self.flags.update({stripargstring(flag): None})

            if val[0]:
                shortopts += val[0]
                opthelp += ('-{short}, --{flag:15} {desc}\n'
                            .format(short=stripargstring(val[0]),
                                    flag=stripargstring(flag), desc=val[1]))
            else:
                opthelp += ('--{flag:19} {desc}\n'
                            .format(flag=stripargstring(flag), desc=val[1]))

        self.usage = self.usagestr
        if self.description:
            self.usage += '\n\n{desc}'.format(desc=self.description)
        if self.optionList:
            self.usage += '\n\nOptions:\n{opts}'.format(opts=opthelp)
        if self.usageTextExtra:
            self.usage += '\n{help}'.format(help=self.usageTextExtra)

        # Parse arguments and options
        try:
            opts, self.args = getopt.getopt(argv, shortopts, longopts)
        except getopt.GetoptError, err:
            self.error = err
            return  # Stop when an invalid option is parsed

        for opt in opts:
            # Compare each option with optionList
            for flag, val in self.optionList.iteritems():
                if opt[0][1] != '-':
                    # Short tags
                    if opt[0][1] == stripargstring(val[0]):
                        if ':' in val[0]:
                            self.flags[stripargstring(flag)] = opt[1]
                        else:
                            self.flags[stripargstring(flag)] = True
                else:
                    # Long tags
                    if opt[0][2:] == stripargstring(flag):
                        if '=' in flag:
                            self.flags[stripargstring(opt[0][2:])] = opt[1]
                        else:
                            self.flags[stripargstring(opt[0][2:])] = True
