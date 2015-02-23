#!/usr/bin/python
# Copyright 2014 Pawel Daniluk
#
# This file is part of WeBIAS.
#
# WeBIAS is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of
# the License, or (at your option) any later version.
#
# WeBIAS is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public
# License along with WeBIAS. If not, see
# <http://www.gnu.org/licenses/>.

import os
import pkg_resources

def put_file(dest, src, opt_dict=None):
    fh = open(dest, 'w')
    if opt_dict is not None:
        fh.write(pkg_resources.resource_string('webias', src) % opt_dict)
    else:
        fh.write(pkg_resources.resource_string('webias', src))
    fh.close()

def create_dir():
    from optparse import OptionParser
    parser = OptionParser(usage="usage: %prog [options] server_dir")
    parser.add_option("--withexamples", action="store_true", dest="examples", help="Populate server directory with sample files.")
    (options, args)=parser.parse_args()

    if len(args) != 1:
        parser.error("incorrect number of arguments")

    server_dir = args[0]

    try:
        os.mkdir(server_dir)
    except OSError:
        print "Cannot create directory %s. Aborting." % server_dir
        exit(-1)

    opt_dict = {'server_dir': os.path.abspath(server_dir)}

    os.chdir(server_dir)

    os.mkdir('conf')
    os.mkdir('dbcache')
    os.mkdir('templates')
    os.mkdir('media')
    os.mkdir('apps')
    os.mkdir('modules')
    os.mkdir('validation')

    put_file('conf/config.ini', 'data/conf/config.ini.sample', opt_dict)
    put_file('runner.py', 'data/runner.py')

    if options.examples:
        example_files = [('apps/groups.xml', 'data/examples/apps/groups.xml'),
                         ('apps/server_map.xml', 'data/examples/apps/server_map.xml'),
                         ('apps/test.xml', 'data/examples/apps/test.xml'),
                         ('apps/vargroups.xml', 'data/examples/apps/vargroups.xml'),
                         ('templates/examples/Test/param_table.genshi', 'data/examples/templates/examples/Test/param_table.genshi'),
                         ('templates/page/Test/help.genshi', 'data/examples/templates/page/Test/help.genshi'),
                         ('templates/page/example.genshi', 'data/examples/templates/page/example.genshi')
                         ]

        verbatim_files = [('examples/test.py', 'data/examples/programs/test.py')]

        os.mkdir('examples')
        os.mkdir('templates/examples')
        os.mkdir('templates/examples/Test')
        os.mkdir('templates/page')
        os.mkdir('templates/page/Test')

        for (dst, src) in example_files:
            put_file(dst, src, opt_dict)

        for (dst, src) in verbatim_files:
            put_file(dst, src)
