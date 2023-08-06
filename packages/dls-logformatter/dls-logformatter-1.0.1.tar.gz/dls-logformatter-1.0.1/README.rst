dls-logformatter
=======================================================================

Python logging formatter for readability.

Implemented as an override for the logging.Formatter class.

Intended advantages:

- readable nested traceback exception cause chains
- compose message for either user, developer or log server
- reusable library for consistency across multiple projects

Installation
-----------------------------------------------------------------------
::

    pip install git+https://gitlab.diamond.ac.uk/scisoft/dls-logformatter.git 

    dls-logformatter --version

Usage
-------------------------------------------------
.. code-block:: python

    import logging

    from dls_logformatter.dls_logformatter import DlsLogformatter

    # Make handler which writes the logs to console.
    handler = logging.StreamHandler()

    # Make the formatter from this library.
    dls_logformatter = DlsLogformatter()

    # Let handler write the custom formatted messages.
    handler.setFormatter(dls_logformatter)

    # Let root logger use the handler.
    root_logger = logging.getLogger()
    root_logger.addHandler(handler)

Example output
-----------------------------------------------------------------------
``dls_logformatter --example long``

::

    2022-12-25 06:23:42.612463   195 MainProcess  MainThread          0        0 WARNING   /22/dls-logformatter/src/dls_logformatter/__main__.py[35] this is a warning message
    2022-12-25 06:23:42.612568   195 MainProcess  MainThread          0        0 INFO      /22/dls-logformatter/src/dls_logformatter/__main__.py[36] this is an info message
    2022-12-25 06:23:42.612609   195 MainProcess  MainThread          0        0 INFO      /22/dls-logformatter/src/dls_logformatter/__main__.py[37] this is a debug message
    2022-12-25 06:23:42.612666   195 MainProcess  MainThread          0        0 ERROR     /22/dls-logformatter/src/dls_logformatter/__main__.py[42] this is an error message
                                                                                 EXCEPTION RuntimeError: error in deep3
                                                                                 TRACEBACK /22/dls-logformatter/src/dls_logformatter/__main__.py[40] deep1()
                                                                                 TRACEBACK /22/dls-logformatter/src/dls_logformatter/__main__.py[18] deep2()
                                                                                 TRACEBACK /22/dls-logformatter/src/dls_logformatter/__main__.py[14] deep3()
                                                                                 TRACEBACK /22/dls-logformatter/src/dls_logformatter/__main__.py[10] raise RuntimeError("error in deep3")

``dls_logformatter --example short``

::

           0        0 WARNING   dls_logformatter.__main__::example[37] this is a warning message
           0        0 INFO      dls_logformatter.__main__::example[38] this is an info message
           0        0 INFO      dls_logformatter.__main__::example[39] this is a debug message
           0        0 ERROR     dls_logformatter.__main__::example[44] this is an error message
                      EXCEPTION RuntimeError: error in deep3
                      TRACEBACK dls_logformatter.__main__::example[42] deep1()
                      TRACEBACK dls_logformatter.__main__::deep1[18] deep2()
                      TRACEBACK dls_logformatter.__main__::deep2[14] deep3()
                      TRACEBACK dls_logformatter.__main__::deep3[10] raise RuntimeError("error in deep3")

``dls_logformatter --example bare``

::

    this is a warning message
    this is an info message
    this is a debug message
    this is an error message
    

Documentation
-----------------------------------------------------------------------

See http://www.cs.diamond.ac.uk/reports/gitlab-ci/dls-logformatter/index.html for more detailed documentation.

Building and viewing the documents locally::

    git clone git+https://gitlab.diamond.ac.uk/scisoft/dls-logformatter.git 
    cd dls-logformatter
    virtualenv /scratch/$USER/venv/dls-logformatter
    source /scratch/$USER/venv/dls-logformatter/bin/activate 
    pip install -e .[dev,docs]
    make -f .dls-logformatter/Makefile validate_docs
    browse to file:///scratch/$USER/venvs/dls-logformatter/build/html/index.html

Topics for further documentation:

- TODO list of improvements
- change log


..
    Anything below this line is used when viewing README.rst and will be replaced
    when included in index.rst

