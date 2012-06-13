#!/usr/bin/python
#encoding: utf-8

import sys
import re

class ManagedHost:
    name=""        # ホスト名
    daemon_names=[] # Onのデーモン名

def filterDaemons(output):
    for line in output.split('\n'):
        line = re.sub(r'\.(el|fc)[0-9]+(\..*|)','',line)
#        line = re.sub(r'-[\-\._0-9a-zA-Z]+','',line)
        yield line

class NormalizeFilter(object):

    results=[]

    def __init__(self,results):
        self.results=results

    def applicate(self):
        hosts=[]
        for result in self.results:
            host=ManagedHost()
            host.name=result['host_name']
            host.daemon_names=[daemon for daemon in filterDaemons(result['output'])]
            hosts.append(host)

        daemon_names=[]
        for host in hosts:
            for daemonName in host.daemon_names:
                if daemonName not in daemon_names:
                    daemon_names.append(daemonName)
        daemon_names.sort()
        
        separator=","
        markOn=u"○"
        markOff=u""
        
        # print header
        out=sys.stdout
        for host in hosts:
            out.write("%s%s"%(separator,host.name))
        out.write('\n')
        # print body
        for daemonName in daemon_names:
            print daemonName,
            for host in hosts:
                result=markOn if daemonName in host.daemon_names else markOff
                line="%s%s"%(separator,result)
                out.write(line.encode('utf-8'))
            out.write('\n')

from yaoya.command import Main
class Main(Main):

    def __init(**kw):
        super.__init__(**kw)

    def run(self):
        results = self.execute()

        from yaoya.rpm import NormalizeFilter
        normalize_filter = NormalizeFilter(results)
        normalize_filter.applicate()
