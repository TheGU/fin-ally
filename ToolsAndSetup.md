Getting the tools you need to be a marginally productive fin-ally developer.

# Introduction #

This section covers the tools required to obtain, develop, and run fin-ally source code.

# Details #

**[Mercurial](http://mercurial.selenic.com/)** (required)

Fin-ally is hosted by Google-code using a Mercurial (Hg) backend. If you don't know anything about Mercurial you can read up on it here. Hg is commonly bundled with TortoiseHg, which provides overlays for file browsers, as well as contextual menu Hg access and some Hg GUI interfaces. Click on the link above, click on the Downloads tab, and then pull down TortoiseHg for 32 or 64-bit Windows. TortoiseHg comes with Hg in one awesome package.

**[Python](http://www.python.org/)** (required)

Fin-ally is written for Python version **2.6.5**. Get it [here](http://www.python.org/ftp/python/2.6.5/python-2.6.5.msi).

**[wxPython](http://www.wxpython.org/index.php)** (required)

wxPython is the GUI framework on which fin-ally runs. It is a port of wxWidgets and can be read about here and found [here](http://downloads.sourceforge.net/wxpython/wxPython2.8-win32-ansi-2.8.11.0-py26.exe). As the link indicates you should install the ansi version of the Python 2.6.5 wxPython.

**[SQLAlchemy](http://www.sqlalchemy.org/)** (required)

SQLAlchemy has replaced Elixir as the Object Relational Mapper and SQL Toolkit. It provides FINally's Python interface to the SQLite database and will be used for all data accesses (read/write/delete/update/etc..). It can be installed using easy\_install as follows:

```
> easy_install SQLAlchemy
```

more instructions can be found [here](http://www.sqlalchemy.org/docs/intro.html).

**[sqlmigratelite](https://bitbucket.org/dls/sqlmigratelite)** (required)

sqlmigratelite is a home-grown Python module that provides a framework for the migration of SQLite data through database schema versions. It can be downloaded [here](https://bitbucket.org/dls/sqlmigratelite/downloads/sqlmigratelite_v1.zip) and should be extracted to this path:

C:/Python26/Lib/site-packages/

**[easy\_install](http://pypi.python.org/pypi/setuptools)**

Easy install is itself a Python package, designed to make installation of other Python packages, well... easier. For Windows development, easy\_install comes in a pre-compiled executable that can be added to your Windows path and executed from the command line. Get it [here](http://pypi.python.org/packages/2.6/s/setuptools/setuptools-0.6c11.win32-py2.6.exe#md5=1509752c3c2e64b5d0f9589aafe053dc). Add C:\Python26\Scripts to your system path as described [here](http://pypi.python.org/pypi/setuptools#windows).

**[Eclipse](http://www.eclipse.org/)**

If you don't already have a Python editor, Eclipse is the way to go. It requires some setup, but once running it provides Python debugging, code-completion, excellent searching features, and access to all of the built in libraries, modules, and packages your script requires. It can be found [here](http://www.eclipse.org/downloads/download.php?file=/eclipse/downloads/drops/R-3.6-201006080911/eclipse-SDK-3.6-win32.zip).

**[PyDev](http://pydev.org/)**

PyDev is an eclipse plug in that allow for all of the great features listed under **Eclipse** above. You can pull it down using the Eclipse update manager by adding this URL: http://pydev.org/updates.