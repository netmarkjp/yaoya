#!/usr/bin/python
#encoding: utf-8

import sys
import re

class NormalizeFilter(object):

    results=[]
    regexp=None
    mode=None

    def __init__(self,results):
        self.results=results

    def applicate(self):
        delimiter='\n'
        if self.mode == 'excel':
            delimiter='\r'
        # print
        out=sys.stdout
        if self.regexp is not None :
            pattern = re.compile(self.regexp)
        for result in self.results:
            try:
                host_name=result['host_name']
                output=result['output']
                tmp_output=''
                if self.regexp is not None and pattern is not None:
                    for line in re.split(r'\n',output):
                        matched = pattern.search(line)
                        if matched is not None:
                            tmp_output = tmp_output+matched.group()+delimiter
                    output=tmp_output

                output=output.rstrip()
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

    regexp=None
    mode=None

    def __init(**kw):
        super.__init__(**kw)

    def run(self):
        results = self.execute()

        from yaoya.csv import NormalizeFilter
        normalize_filter = NormalizeFilter(results)
        NormalizeFilter.regexp=self.regexp
        NormalizeFilter.mode=self.mode
        normalize_filter.applicate()

