import json
import template_config as config
from collections import OrderedDict
import argparse
parser = argparse.ArgumentParser(description='Template Generator')
parser.add_argument('--name','-n',default="logstash*",help='template name' )
parser.add_argument('--ty','-t',default="logs",help='type of the data' )
parser.add_argument('--disableall','-da',action='store_true',help='disable all' )
parser.add_argument('--disablesource','-ds',action='store_true',help='disable source' )
parser.add_argument('--refresh','-r',default="30s",help='refresh interval' )
parser.add_argument('--numrepli','-nr',default=0,type=int,help='number of replicas' )
args = parser.parse_args()
template_name = args.name
_type = args.ty
if args.disableall:
    to_enable_all = False
else:
    to_enable_all = True
if args.disablesource:
    to_enable_source = False
else:
    to_enable_source = True
refresh_interval = args.refresh
number_replicas = args.numrepli

template = OrderedDict()
template["template"] = template_name
template["settings"] = { "index.refresh_interval": refresh_interval,"number_of_replicas": number_replicas}
template["mappings"] = {}
template["mappings"][_type] = OrderedDict()
template["mappings"][_type]["_all"] = {}
template["mappings"][_type]["_all"]["enabled"] = to_enable_all
template["mappings"][_type]["_source"] = {}
template["mappings"][_type]["_source"]["enabled"] = to_enable_source
template["mappings"][_type]["properties"] = {}
for strs in config.not_analyzed_strings:
    template["mappings"][_type]["properties"][strs] = {"index" : "not_analyzed","doc_values" : True,"type": "string"}

for strs in config.not_indexed_strings:
    template["mappings"][_type]["properties"][strs] = {"index" : "no","type": "string"}

for times in config.timefields:
    template["mappings"][_type]["properties"][times] = {
                                                        "type" : "date",
                                                        "format" : "dateOptionalTime",
                                                        "doc_values" : True
                                                       }

for dbls in config.double_types:
    template["mappings"][_type]["properties"][dbls] = { "type" : "double","doc_values" : True,"index": "not_analyzed"}
for ints in config.integer_types:
    template["mappings"][_type]["properties"][ints] = { "type" : "integer","doc_values" : True,"index": "not_analyzed"}
for longs in config.long_types:
    template["mappings"][_type]["properties"][longs] = { "type" : "long","doc_values" : True,"index": "not_analyzed"}
for ips in config.ip_fields:
    template["mappings"][_type]["properties"][ips] = { "type" : "ip","doc_values" : True,"index": "not_analyzed"}

with open("templates.json","w") as json_file:
    json_file.write(json.dumps(template,indent=4))
