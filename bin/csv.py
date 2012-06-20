#!/usr/bin/env python
#coding: utf-8

from os import sys
from os import path

parent_dir, bin_dir = path.split(path.dirname(path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from optparse import OptionParser
from yaoya.csv import Main

if __name__ == '__main__':
    p = OptionParser()
    p.add_option('-c','--config',dest="config",help="configuration file. default is <YAOYA_HOME>/conf/yaoya.cfg")
    p.add_option('-g','--group',dest="group",help="group name")
    p.add_option('-n','--name',dest="command",help="command name")
    p.add_option('-r','--regexp',dest="regexp",help="regexp pattern")
    p.add_option('-m','--mode',dest="mode",help="if --mode=excel , line delimiter set to \\r.")
    p.set_defaults(
	config=parent_dir+'/conf/yaoya.conf',
        group = None,
        command = None,
	)
    opts,args = p.parse_args()
    if opts.group is None:
        sys.stderr.write(u'ERROR: -g or --group required.')
        sys.stderr.write(u'\n')
        sys.exit(1)
    if opts.command is None:
        sys.stderr.write(u'ERROR: -n or --command required.')
        sys.stderr.write(u'\n')
        sys.exit(1)
    m=Main(
            opts.config,
            group_name=opts.group,
            command_name=opts.command,
            )
    m.regexp=opts.regexp
    m.mode=opts.mode
    sys.exit(
        m.run()
        )

# :vim: filetype=python :
