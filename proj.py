#!/usr/bin/python3

import sys
import re

def checkip(input1):
    exist = False 
    reg = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'
    ip = re.search(reg,input1)
    if ip == None:
        return False
    else:
        ip_split= input1.split(".")
        for x in ip_split:
            if eval(x) > 255:
                return False
            else:
                exist = True
    return exist
            
def parse(fname):
    output = []
    file = open(fname, "r")
    listr = file.readlines()
    reg = re.compile(r"\d{2}:\d{2}:\d{2}.\d{6} IP (?P<ip>(?:\d{1,3}\.){3}\d{1,3}).\d{1,5} > (?P<ip2>(?:\d{1,3}\.){3}\d{1,3})")
    for line in listr:
      m = reg.match(line)
      if m:
        length = re.search('length (\d+)', line)
        if output == []:
            output.append([m.group("ip"),m.group("ip2"),int(length.group(1))])
        else:
          exists = False
          for x in output:
            if m.group("ip") == x[0]:
              if m.group("ip2") == x[1]:
                if length:
                  x[2] =  x[2] + int(length.group(1))
                  exists = True
                  break
          if exists == False:
            if length:
              output.append([m.group("ip"),m.group("ip2"),int(length.group(1))])
    file.close()
    return output

def filter_results(pfile,sip,dip):
    exists = False
    output = []
    if dip == None or dip == "":
        for x in pfile:
            if x[0] == sip:
                output.append(x)
                exists = True
    else:
        for x in pfile:
            if x[1] == dip and x[0] == sip:
                output.append(x)
                exists = True
    if exists == False:
        output.extend(pfile)  
    return output

def sort_list(flist):
    for x in flist:
        flist = sorted(flist, reverse=True, key=lambda x: x[2])
    return flist

def print_list(slist):
    for x in slist:
        print("source:", x[0], "\t dest:", x[1], "\t total:" ,x[2])
 
if len(sys.argv) == 3:
    filename = sys.argv[1]
    sourceip = sys.argv[2]
    destip = ""
elif len(sys.argv) == 4:
    filename = sys.argv[1]
    sourceip = sys.argv[2]
    destip= sys.argv[3]
elif len(sys.argv) == 2:
    filename = sys.argv[1]
    sourceip = ""
    destip = ""
    print_list(sort_list(parse(filename)))

if checkip(sourceip) == True:
    if len(sys.argv) == 4:
        print_list((sort_list(filter_results(parse(filename),sourceip,destip))))
    elif len(sys.argv) == 3:
        print_list((sort_list(filter_results(parse(filename),sourceip,destip))))

    














