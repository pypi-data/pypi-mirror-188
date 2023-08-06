dls-pairstream
=======================================================================

Simple data streaming protocol

Intended advantages:

- agnostic of type of underlying transport mechanism
- meta/data message envelope
- reusable across projects

Installation
-----------------------------------------------------------------------
::

    pip install git+https://gitlab.diamond.ac.uk/kbp43231/dls-pairstream.git 

    dls-pairstream --version

Documentation
-----------------------------------------------------------------------

See https://www.cs.diamond.ac.uk/dls-pairstream for more detailed documentation.

Building and viewing the documents locally::

    git clone git+https://gitlab.diamond.ac.uk/kbp43231/dls-pairstream.git 
    cd dls-pairstream
    virtualenv /scratch/$USER/venv/dls-pairstream
    source /scratch/$USER/venv/dls-pairstream/bin/activate 
    pip install -e .[dev]
    make -f .dls-pairstream/Makefile validate_docs
    browse to file:///scratch/$USER/venvs/dls-pairstream/build/html/index.html

Topics for further documentation:

- TODO list of improvements
- change log


..
    Anything below this line is used when viewing README.rst and will be replaced
    when included in index.rst

