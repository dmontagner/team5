#!/usr/bin/python

# This script is responsible for update the following files in OpenNTI
#
#    - data/hosts.yaml
#
# hosts.yaml format
#
#  <IP>:<TAG>
#
# where <TAG> can be vmx or qfx
#
# team 5

import yaml
import sys, getopt, inspect


#
# print trace messages in the code
#
def trace(sev, msg):
    global SEV
    funcName = inspect.stack()[1][3]
    if (sev <= SEV):
        print 'TRACE[' + `sev` + ']: ' + funcName + '() : ' + msg

def printHelp():
    print ''
    print './provisionOpenNTI.py -d <severity> -o <operation> -h <host IP> -t <tag>'
    print ''
    print 'operation (o):'
    print ''
    print '    add: add host'
    print '    del: delete host'
    print ''
    print 'host (h):'
    print ''
    print '    host IP: the IP address of the host'
    print ''
    print 'tag (t):'
    print ''
    print '    tag: the host tag (vmx or qfx)'
    print ''
    print 'severity (d):'
    print ''
    print '    0: no traces enabled (default)'
    print '    1: traces level 1 enabled'
    print '    2: traces level 2 enabled'
    print '    <...>'
    print '    9: traces level 9 enabled (maximum verbosity)'
    print ''

def Success():
    print '1'
    sys.exit(0)

def Failure():
    print '0'
    sys.exit(1)

#
# Main loop of the code
#
def main(argv):

    global SEV

    try:
        opts, args = getopt.getopt(sys.argv[1:],"h:o:t:d:", ["host=", "operation=", "tag=", "debug="])
    except getopt.GetoptError:
        printHelp()
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-d", "--debug"):
            SEV = int(arg)
        elif opt in ("-o", "--operation"):
            operationArg = arg
        elif opt in ("-h", "--host"):
            hostArg = arg
        elif opt in ("-t", "--tag"):
            tagArg = arg
        else:
            printHelp()

    trace(2, 'operationArg = ' + operationArg)
    trace(2, 'hostArg = ' + hostArg)
    trace(2, 'tagArg = ' + tagArg)
    trace(2, 'severity = ' + `SEV`)

    # continue here
    # get the path for the host file from the yaml files provisionOpenNTI.yaml
    try:
        stream = open('provisionOpenNTI.yaml','r')
        configFile = yaml.load(stream)
        stream.close()
        trace(1,'loaded yaml config file')
        #print configFile
    except:
        trace(1,'ERROR: could not load provisionOpenNTI.yaml')

    try:
        streamHostsFile = open(configFile['hosts'],'r')
    except:
        trace(1,'ERROR: could not read the configuration file ' + configFile['hosts'])

    trace(1,'configFile = ' + configFile['hosts'])

    HostsFile = yaml.load(streamHostsFile) or {}
    streamHostsFile.close()

    #print HostsFile

    if 'add' in operationArg:
        # add a host
        trace(2, "adding a host")
        #try:
        HostsFile[hostArg] = tagArg
        #except:
            # the file is empty
        #    trace(1,'WARNING: the hosts file is empty')
        #print HostsFile
        # open file for write
        try:
            streamHostsFile = open(configFile['hosts'],'w')
            yaml.dump(HostsFile, streamHostsFile, default_flow_style=False)
            streamHostsFile.close()
            Success()

        except Exception, err:
            trace(1, 'ERROR: could not update ' + configFile['hosts'])
            print Exception, err
            Failure()

    elif 'del' in operationArg:
        # delete a host
        trace(2, "removing a host")
        try:
            del HostsFile[hostArg]
            streamHostsFile = open(configFile['hosts'],'w')
            yaml.dump(HostsFile, streamHostsFile, default_flow_style=False)
            streamHostsFile.close()
            Success()

        except KeyError:
            trace(1, 'ERROR: host does not exist')
            Failure()

    else:
        trace(1, 'ERROR: operation not supported')
        Failure()

SEV = 0

if __name__ == '__main__':
    main(sys.argv[1:])
