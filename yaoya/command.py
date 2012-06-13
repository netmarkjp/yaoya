#!/usr/bin/env python
#coding: utf-8

from ConfigParser import ConfigParser
from pymongo import Connection
from pymongo import ASCENDING
from pymongo import DESCENDING
from copy import deepcopy

class Main(object):

    config = ConfigParser()
    group_name = None

    def __init__(self, config_file, group_name, command_name=None):
        self.config.read(config_file)
        self.group_name = group_name
        self.command_name = command_name

    def run(self):
        results = self.execute()

#        from yaoya.rpm import NormalizeFilter
#        normalize_filter = NormalizeFilter(results)
#        normalize_filter.applicate()

        # print
        for result in results:
            try:
#                print "%s, %s"%(
#                    result['host_name'],
#                    result['output'].rstrip(),
#                    )
                print result
            except:
                pass


    def execute(self):
        mongos={
            'mongo_host':self.config.get('server','mongo_host'),
            'mongo_port':self.config.get('server','mongo_port'),
            'mongo_dbs':self.config.get('server','mongo_dbs'),
            'mongo_collection':self.config.get('server','mongo_collection'),
            }
        connection = Connection(
            mongos['mongo_host'],
            int(mongos['mongo_port']),
            )
        collection = connection[mongos['mongo_dbs']][mongos['mongo_collection']]

        base_find_condition = {
            'group_name' : self.group_name,
            'visible' : 'True',
            }
        if self.command_name is not None:
            base_find_condition.update({'command_name' : self.command_name,})

        # find hosts in group
        condition=deepcopy(base_find_condition)
        host_names = collection.find(condition).distinct('host_name')
        host_names.sort()

        # find latest result on each host
        results=[]
        for host_name in host_names:
            condition=deepcopy(base_find_condition)
            condition.update({'host_name':host_name})
            latests = collection.find(condition).sort('execute_at',DESCENDING).limit(1)
            latest_execute_at=''
            for latest in latests:
                latest_execute_at = latest['execute_at']
                break
            
            condition=deepcopy(base_find_condition)
            condition.update({'host_name':host_name})
            condition.update({'execute_at':latest_execute_at})
            documents = collection.find(condition).sort('command_name',ASCENDING)
            for document in documents:
                results.append(document)

        # finalize
        connection.disconnect()

        return results


