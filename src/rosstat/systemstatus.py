#! /usr/bin/env python2

import rosnode
import rosgraph
import xmlrpclib
import psutil
import time

default_delay = 0.1

class SystemStatus:
    def __init__(self):
        self.master = rosgraph.Master("")

    def fullReport(self, delay=default_delay):
        mem = psutil.virtual_memory()
        return {
            "cpu_percent": psutil.cpu_percent(delay),
            "mem_percent": 100. * mem.used / mem.total,
            "nodes": self.allNodesStat()
        }

    def allNodesStat(self, **kw):
        return {name: self.pidStat(pid) for name, pid in self.nodePids().items()}

    def nodeStat(self, node_name, **kw):
        return self.pidStat(self.getPid(node_name), **kw)

    def pidStat(self, pid, delay=default_delay):
        p = psutil.Process(pid)
        return {
            "cpu_percent": p.cpu_percent(delay) / psutil.cpu_count(),
            "mem_percent": p.memory_percent()
        }

    def nodePids(self):
        names = self.nodeNames()
        return dict(zip(names, map(self.getPid, names)))

    def nodeNames(self):
        return rosnode.get_node_names()

    def getPid(self, node_name):
        return rosnode._succeed(xmlrpclib.ServerProxy(self.master.lookupNode(node_name)).getPid())

if __name__ == "__main__":
    print(SystemStatus().fullReport())
