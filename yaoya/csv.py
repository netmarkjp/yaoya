#!/usr/bin/python
#encoding: utf-8

import sys
import re

class NormalizeFilter(object):

    results=[]

    def __init__(self,results):
        self.results=results

    def applicate(self):
        # print
        out=sys.stdout
        for result in self.results:
            try:
                host_name=result['host_name']
                output=result['output'].rstrip()
                output=re.sub(r'"','',output)
                line='"%s","%s"'%(
                    host_name,
                    output,
                    )
                out.write(line.encode('utf-8')) 
                out.write('\n')
            except:
                pass

from yaoya.command import Main
class Main(Main):

    def __init(**kw):
        super.__init__(**kw)

    def run(self):
        results = self.execute()

        from yaoya.csv import NormalizeFilter
        normalize_filter = NormalizeFilter(results)
        normalize_filter.applicate()
