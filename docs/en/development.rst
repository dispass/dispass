Related projects
================

There are three related projects of DisPass, all are created by Tom
Willemse (https://ryuslash.org/).

dispass.el
----------

dispass.el is an emacs wrapper around DisPass.

- Website: http://ryuslash.org/projects/dispass.el.html
- Github: https://github.com/ryuslash/dispass.el

cDisPass
--------

cdispass is a JavaScript-based wrapper around DisPass for the Conkeror
Web Browser.

- Github: https://github.com/ryuslash/dispass.el


libdispass
----------

C library of DisPass algorithms

- Github: https://github.com/ryuslash/libdispass


Development
===========

Setting up a development environment
------------------------------------

The project lacks any CONTRIBUTING instructions at the moment.

Installing necessary tools
##########################

Clone git repo:

.. code:: console

   git clone git://github.com/dispass/dispass.git
   cd dispass

Create and activate virtualenv:

.. code:: console

   python -m venv .virtualenv
   source .virtualenv/bin/activate

Install development requirements and install with the editable flag.

.. code:: console

   pip install -r requirements-dev.txt
   pip install -e .

Please use Github for bug reports, questions or submitting
pull-requests. You can also discuss dispass on the Gitter.im channel
babab/DisPass.

- Issue tracker at Github: https://github.com/babab/dispass/issues
- Gitter.im: https://gitter.im/babab/DisPass


Acknowledgements
----------------

Many thanks go out to Tom (ryuslash) Willemse for valuable contributions
to `gdispass` and the new `dispass2` algorithm. He also wrote
`dispass.el`, `cDisPass` and `libdispass`.

.. Include ChangeLog section from base path
.. include:: ../../ChangeLog.rst


Software license
==============================================================================

DisPass is released under an ISC license, which is functionally
equivalent to the simplified BSD and MIT/Expat licenses, with language
that was deemed unnecessary by the Berne convention removed.

::

   Copyright (c) 2012-2016  Tom Willemse <tom@ryuslash.org>
   Copyright (c) 2011-2018  Benjamin Althues <benjamin@babab.nl>

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
