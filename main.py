# fileencoding: utf-8
# read content from gfwlist url and generate a foxproxy configuation file with it

import urllib2
import base64
import re

def parse():
    url = "https://raw.githubusercontent.com/gfwlist/gfwlist/master/gfwlist.txt"
    rules = base64.b64decode(
        urllib2.urlopen(
            urllib2.Request(url)
        ).read()
    ).decode()
    for line in re.findall("([^\n]+)", rules):
        if line.find("[") >= 0:
            continue
        if line.find("\\") >= 0:
            continue
        if line.find("!") >= 0:
            if line.find("General List End") >= 0:
                break
            else:
                continue

        obj = re.search("([^|@]+)", line)
        if obj:
            yield str(obj.group())

def ruleHandler(rule):
    return re.sub(r"\/*", '', re.sub(r"https?://", "", rule))
            
def join():
    text = None
    with open("foxyproxy-tpl.json", "r") as f:
        text = f.read()
        f.close()
    rules = []
    [ rules.append(ruleHandler(rule))
     for rule in parse()
     if ruleHandler(rule) not in rules ]

    buff = [str("""{
            "title": "%s",
            "active": true,
            "pattern": "%s",
            "type": 1,
            "protocols": 1
        }""") % (rule, rule)
        for rule in rules
    ]
    with open("foxyproxy.new.json", "w") as f:
        f.write(re.sub('"fuckmylife"', ",\n    ".join(buff), text))

join()
