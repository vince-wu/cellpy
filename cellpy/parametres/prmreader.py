# -*- coding: utf-8 -*-

default_prms = """
[Paths]
outdatadir: ..\outdata
resdatadir: ..\indata
hdf5datadir: ..\indata
db_path: ..\databases
filelogdir: ..\databases

[FileNames]
db_filename: cellpy_db.xlsx
dbc_filename: cellpy_dbc.xlsx
"""

import glob
import os
import sys
import ConfigParser


class read:
    """reads prm file for cellpy.

    To simplify usage, it is possible to store some commonly used parameters
    in a _cellpy_prms_some_name.ini file (some_name could be any string).

    Currently, the following options (and defaults) are supported::

        [Paths]
        outdatadir: ..\outdata
        resdatadir: ..\indata
        hdf5datadir: ..\indata
        db_path: ..\databases
        filelogdir: ..\databases

        [FileNames]
        db_filename: cellpy_db.xlsx
        dbc_filename: cellpy_dbc.xlsx

    The prmreader looks for files with file names starting with _cellpy_prms
    and ending with .ini in the following directories:
        curdir, filedir, userdir
    in ascending priority. If it finds several files, the file
    _cellpy_prms_default.ini will have lowest priority.

    The search path can be altered by adjusting the search_order list.

    Args:
        prm_filename (str)(optional) : parameter file name
        search_order (list)(optional): list with paths to search in ascending priority
                             (available options: ["curdir","filedir","userdir"]).
    """

    def __init__(self, prm_filename=None, search_order=None):
        self.script_dir = os.path.abspath(os.path.dirname(__file__))
        self.search_path = dict()
        self.search_path["curdir"] = os.path.abspath(os.path.dirname(sys.argv[0]))
        self.search_path["filedir"] = self.script_dir
        self.search_path["userdir"] = os.path.expanduser("~")
        if search_order is None:
            self.search_order = ["curdir", "filedir", "userdir"]
        self.prm_default = os.path.join(self.script_dir, "_cellpy_prms_default.ini")
        self.outdatadir = "..\outdata"
        self.resdatadir = "..\indata"
        self.hdf5datadir = "..\indata"
        self.db_path = "..\databases"
        self.filelogdir = "..\databases"
        self.db_filename = "cellpy_db.xlsx"
        self.dbc_filename = "cellpy_db.xlsx"
        if prm_filename:
            self._readprms(prm_filename)
        else:
            prm_filenames = list()
            prm_globtxt = "_cellpy_prms*.ini"

            for key in self.search_order:
                prm_directory = self.search_path[key]
                prm_globtxt = os.path.join(prm_directory, prm_globtxt)
                prm_filenames.extend(glob.glob(prm_globtxt))

            for f in prm_filenames:
                if f != self.prm_default:
                    self.prm_default = f
                    break

            if not os.path.isfile(self.prm_default):
                print "could not find ini-file"
                no_file = True
            else:
                no_file = False
            self._readprms(no_file=no_file)

    def __get(self, parser, opt, name, too):
        try:
            too = parser.get(opt, name)

        except ConfigParser.NoOptionError as e:
            print "error",
            print e

    def _readprms(self, no_file=False):
        parser = ConfigParser.SafeConfigParser()
        if no_file:
            import StringIO
            parser.readfp(StringIO.StringIO(default_prms))
        else:
            # print self.prm_default
            parser.read(self.prm_default)

        opt = "Paths"
        try:
            self.outdatadir = parser.get(opt, "outdatadir")
        except ConfigParser.NoOptionError as e:
            print "prmreader.py:",
            print e
        try:
            self.resdatadir = parser.get(opt, "resdatadir")
        except ConfigParser.NoOptionError as e:
            print "prmreader.py:",
            print e
        try:
            self.hdf5datadir = parser.get(opt, "hdf5datadir")
        except ConfigParser.NoOptionError as e:
            print "prmreader.py:",
            print e
        try:
            self.db_path = parser.get(opt, "db_path")
        except ConfigParser.NoOptionError as e:
            print "prmreader.py:",
            print e
        try:
            self.filelogdir = parser.get(opt, "filelogdir")
        except ConfigParser.NoOptionError as e:
            print "prmreader.py:",
            print e

        opt = "FileNames"
        try:
            self.db_filename = parser.get(opt, "db_filename")
        except ConfigParser.NoOptionError as e:
            print "prmreader.py:",
            print e
        try:
            self.dbc_filename = parser.get(opt, "dbc_filename")
        except ConfigParser.NoOptionError as e:
            print "prmreader.py:",
            print e

    def _writeprms(self):
        print "prmreader.py: _writeprms is not implemented yet"

    def __str__(self):
        txt = ""
        txt += "prm-file:    \t%s\n" % self.prm_default
        txt += "------------------------------------------------------------\n"
        txt += "NAME          \tVALUE\n"
        txt += "outdatadir:  \t%s\n" % self.outdatadir
        txt += "resdatadir:  \t%s\n" % self.resdatadir
        txt += "hdf5datadir: \t%s\n" % self.hdf5datadir
        txt += "db_path:     \t%s\n" % self.db_path
        txt += "filelogdir:  \t%s\n" % self.filelogdir

        txt += "db_filename: \t%s\n" % self.db_filename
        txt += "dbc_filename:\t%s\n" % self.dbc_filename

        return txt


if __name__ == "__main__":
    r = read()
    print "\n----------------------Read file-----------------------------"
    print "Search path:"
    for k, d in r.search_path.items():
        print k, d,
        print os.path.isdir(d)

    print "Prms:"
    print "------------------------------------------------------------"
    print r
    print "------------------------------------------------------------"

    errors = False
    if not os.path.isdir(r.db_path):
        print "Error! db_path not found"
        errors = True
    if not os.path.isdir(r.outdatadir):
        print "Error! outdatadir not found"
        errors = True
    if not os.path.isdir(r.resdatadir):
        print "Error! resdatadir not found"
        errors = True
    if not os.path.isdir(r.hdf5datadir):
        print "Error! hdf5datadir not found"
        errors = True
    if not os.path.isdir(r.filelogdir):
        print "Error! filelogdir not found"
        errors = True

    if not os.path.isfile(os.path.join(r.db_path, r.db_filename)):
        print "Error! db_filename not found"
        errors = True
    if not os.path.isfile(os.path.join(r.db_path, r.dbc_filename)):
        print "Error! dbc_filename not found"
        errors = True

    if errors == False:
        print "All ok"
