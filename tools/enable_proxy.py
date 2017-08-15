#!/usr/bin/python

import sys
import os

import json
from pprint import pprint


#xs env mta_python.web --export-json /tmp/mta_python.web.json

filename = "/tmp/" + sys.argv[1] + ".json"
cmd = "xs env " + sys.argv[1] + " --export-json " + filename + ""
print "cmd: = " + cmd
os.system(cmd)

with open(filename) as data_file:
    data = json.load(data_file)
    in_dests = data["destinations"]
    out_dests = in_dests
    pprint(in_dests)
    idx = 0
    for route in in_dests:
        print "route: " + route["name"] + " : " + route["url"]
        out_dests[idx]["proxyHost"] = "mitm.sfphcp.com"
        out_dests[idx]['proxyPort'] = '8888'
        out_dests[idx]["strictSSL"] = False
        idx += 1

    print "out_dests:" + json.dumps(out_dests)


    cmd = "xs set-env " + sys.argv[1] + " destinations '" + json.dumps(out_dests) + "'"
    print "cmd: = " + cmd
    os.system(cmd)

    cmd = "xs restage " + sys.argv[1]
    print "cmd: = " + cmd
    os.system(cmd)

    cmd = "xs restart " + sys.argv[1]
    print "cmd: = " + cmd
    os.system(cmd)

    cmd = "xs env " + sys.argv[1]
    print "cmd: = " + cmd
    os.system(cmd)

