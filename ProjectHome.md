# Fin-ally #
## Project Overview ##
Fin-ally (Financial Ally) is a financial analysis and expense tracking tool written in Python using a wxWidgets GUI framework and a SQLite database layer. This tool is intended to address and answer a number of simple financial questions, such as:

  * What do I spend my money on?
  * What types of expenses should I target for reduction to increase savings?
  * What percentage of my weekly/monthly/annual pay am I saving?

Additionally, Fin-ally is designed to provide a certain amount of graphical and numerical feedback about your expenses. This feedback will eventually be provided in three forms:

  * A list of expenses in simple grid format.
  * Graphical expense tracking over time (ie: bar graphs).
  * Basic numerical analysis.

## Project Components ##
As described above, Fin-ally is designed to interpret and dislay financial data. In order to achieve this, Fin-ally needs to be able to collect financial information, turn them into persistent records, and display them to a human user. The major technical components are:

### Data Collection ###
Currently, data collection is handled via either a finance entry control or an import control. The finance entry control allows the user to input data for a single transaction, while the import control allows the user to load a financial data file similar to a Quicken file format.
### SQLite database ###
Record persistence is handled via a SQLite interface, responsible for reading, writing, seraching, and maintaining a SQLite database (.db) file.
### GUI Interface ###
The User Interface portion of Fin-ally is written using the wxPython framework, and handles the majority of the interaction between the database and the user. WxPython becomes the run-time "master" for Fin-ally, and it handles all program flow.

## Project Prerequisites ##
In order to run the Fin-ally application, the following software packages are required:

  * Python 2.5.1 or higher (when available). Beginning with verion 2.5.1, most Python distributions contain the sqlite3 module, which is required for Fin-ally. To get a Python distribution, check out the [Python.org downloads](http://www.python.org/download/).
  * wxPython module for Python 2.5. This provides the required GUI modules and is typically **not** part of a standard Python installation. It can be found with the [wxPython binary downloads](http://www.wxpython.org/download.php#binaries).
  * (optional) The Sqlite3 executable. This will allow you to open SQLite version 3 files and inspect them independent of Fin-ally. Extremely useful for debugging. It can be found with the [SQLite downloads](http://www.sqlite.org/download.html).

## Running Fin-ally ##
Executing the Fin-ally program can be done from a command line environment using:

`>> python FINally.py`

and it can also be executed by double-clicking on the FINally.py file.

**NOTE:** If no database (.db) file is present in the root Fin-ally directory, the Fin-ally tool will prompt the user to input a file name (ending in .db), which it will then populate with sample data and use as the default database.