DisPass
*******
:Author: Benjamin Althues
:Copyright: Copyright 2011-2012, Benjamin Althues.
:Revision: 3
:Date: 2012/05/28

DisPass is a passphrase generator for Windows and Unix / Linux.
You can use it to create unique passwords for logging in to websites, servers
or any other kind of thing that requires login.
DisPass does not keep your passwords in a database but rather lets you
generate a unique passphrase formed from a master password and a label.
It is a command line app, but also has a simple graphical interface.


Downloading/Installing
======================


Using pip
---------

The recommended way is to download and install directly from the PyPI
repository using pip.

::

   $ sudo pip install dispass

You must have python's docutils installed in able to do so.
This will install the dispass module in python's dist-packages folder.
You can now run dispass using the 'dispass' and 'gdispass' scripts
placed under '/usr/local/bin/' or '/usr/bin/'.

PyPI project page - http://pypi.python.org/pypi/DisPass/


Clone git repo and use setup.py
-------------------------------

::

   $ git clone git://github.com/babab/dispass.git
   $ cd dispass
   $ sudo python setup.py install


Single module
-------------
The file 'dispass.py' is a single python module and it is the only file
you really need to use dispass. You can manually copy it to /home/bin/ or
/usr/local/bin/ and give it exec rights with chmod.


Using the command line app
==========================

**label**

The label is a string that you use to identify the password.
i.e. this can be a domainname of the service the password is used for
like 'google.com'.

**password**

This is a master password that, together with the label is used to generate
the passphrase.


Unix/Linux/Mac
--------------

::

   DisPass 0.1(posix) - http://dispass.babab.nl/

   When DisPass is executed as 'gdispass' or 'dispass -g',
   the graphical version will be started.

   USAGE: dispass [-co] label [label2] [label3] [...]
          dispass -g | -h | -V
          gdispass

   Options:
   -c, --create    use if this passphrase is new (check input PW)
   -g, --gui       start guided graphical version of DisPass
   -h, --help      show this help and exit
   -o, --output    output passphrases to stdout (instead of the
                   more secure way of displaying via curses)
   -V, --version   show full version information and exit


Windows
-------

::

   DisPass 0.1(nt) - http://dispass.babab.nl/

   When DisPass is started without arguments, the graphical
   version will be started. To use the command line,
   submit one or more labels.

   USAGE: dispass [options] [label] [label2] [label3] [...]

   Options:
   -c, --create    use if this passphrase is new (check input PW)
   -h, --help      show this help and exit
   -V, --version   show full version information and exit


Using the graphical version
---------------------------

No info yet.


Software license
****************

Copyright (c) 2011-2012 Benjamin Althues <benjamin@babab.nl>

Permission to use, copy, modify, and distribute this software for any
purpose with or without fee is hereby granted, provided that the above
copyright notice and this permission notice appear in all copies.

THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.





.. vim: set et ts=3 sw=3 sts=3 ai: