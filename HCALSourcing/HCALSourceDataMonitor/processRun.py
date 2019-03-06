#!/usr/bin/env python
"""
A script to process a single sourcing run
# -*- coding: UTF-8 -*-

"""
import string
import os
import sys
import subprocess

inputFileLocal = 'file:///data/sourcing/USC1702/USC___XXX__.root'
inputFileEos = 'root://eoscms//eos/cms/store/group/dpg_hcal/comm_hcal/USC/run__XXX__/USC___XXX__.root'
outFile = '/data/sourcing/Ntuples1903/ntuple_da___XXX__.root'

cfgTemplate = 'hcalsourcedatamonitor_template_cfg.py'
cfgFile = 'hcalsourcedatamonitor_cfg.py'

anaPath = '/wwwlocal/p5s/Ana/Scripts/'
script = './histoMakerHB.py'
link = 'http://cmskam06.cern.ch/p5sourcing2019/profs.php'

rawDataFile = ''
ntupleFile = ''


def makeCfgFile(rawDataFile, ntupleFile):
    
    f = open(cfgTemplate,'r')
    tmpl = f.read()
    f.close()
    
    tmpl = tmpl.replace('__XXX__', rawDataFile)
    tmpl = tmpl.replace('__YYY__', ntupleFile)
    
    f = open(cfgFile, 'w')
    f.write(tmpl)
    f.close()

def processRun():
    if len(sys.argv) < 2:
        print "Usage", sys.argv[0], "runNo [local]"
        exit(1) 
        
    cwd = os.getcwd()
    
    runNo = str(sys.argv[1]).zfill(6)
    if len(sys.argv) == 3 and sys.argv[2] == 'local':
        #Check if file has been copied
        rawDataFile = inputFileLocal.replace('__XXX__', runNo)
        if not  os.path.isfile(rawDataFile.replace('file://', '')):
            print rawDataFile,  'not found. Make sure that it\'s been copied from hcalutca01' 
            exit(1)
        print "Processing run", runNo, 'from local storage'
    else:
        #File from eos
        rawDataFile = inputFileEos.replace('__XXX__', runNo)
        print "Processing run", runNo, 'from eos'
    
    ntupleFile = outFile.replace('__XXX__', runNo)
    makeCfgFile(rawDataFile, ntupleFile)

    print "Running CMSSW for run", runNo, "..."
    #proc = subprocess.Popen(['cmsRun', cfgFile], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    #out,err = proc.communicate()
    #print out
    #print err
    command = 'cmsRun ' + cfgFile
    os.system(command)
    
    
    #print "Running ngHistoMaker for run", runNo, "..."
    #os.chdir(anaPath)
    #proc = subprocess.Popen([script, runNo], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    #out,err = proc.communicate()
    #print out
    #print err
    
    os.chdir(cwd)
    
    print "=================================\n"
    print "You can examine output at ", link, '\n'
    
#===========================================================
if __name__ == "__main__":
    processRun()





