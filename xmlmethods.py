"""
(Intern Project West Pod Summer 2019)
Authors: Thomas McLaughlin               |    Spencer DeRecat                   |    Benjamin Rice
Email : thomas.mclaughlin@tanium.com    |    Spencer.derecat@tanium.com        |    benjamin.rice@tanium.com
Date  : June 12 2019
Description:
A class containing various methods for pulling useful information out of manifest content xml
"""

import xml.etree.ElementTree as ET
import urllib.request as urllib2
from collections import Counter
class Xmlmethods():
    def __init__(self, xmlfile):  #input - xml file to be parsed, in our case: manifest.xml
        self.tree = ET.parse(xmlfile)
        self.root = self.tree.getroot()
        self.headers = []
        self.founddelims = {}
        self.foundossupport = {}
        self.founddescriptions = {}
        self.foundresulttypes = {}
        self.foundsensorlengths = {}
        self.foundhashes = {}
        self.foundsensortypes = {}
        for elem in self.root:
            #go into each content link to find sensors
            contentstore = urllib2.urlopen(elem.find('content_url').text)
            contenttree = ET.parse(contentstore)
            header = contenttree.getroot()
            self.headers.append(header)
    def getdelimeters(self):
        # populates self.founddelims
        for header in self.headers:
            # #go into each content link to find sensors
            # contentstore = urllib2.urlopen(elem.find('content_url').text)
            # contenttree = ET.parse(contentstore)
            # header = contenttree.getroot()
            for elem in header.iter('sensor'):
                name = elem.find('name').text
                if name not in self.founddelims.keys():
                    self.founddelims[name] = []
                #if there is a delimiter put it in found delims, if not put 'none' in found delims
                if elem.find('delimiter') != None:
                    delim = elem.find('delimiter').text
                    if delim not in self.founddelims[name]:
                        self.founddelims[name].append(delim)
                else:
                    if 'none' not in self.founddelims[name]:
                        self.founddelims[name].append('none')


    def getossupport(self):
        # foundossupport gets 5 index list with information about supported OS for all sensors: 0 - WINDOWS, 1 - LINUX, 2 - MAC, 3 - SOLARIS, 4 - AIX
        # index marked 1 if sensor supported, 0 if not
        # example: [1, 0, 0, 1, 1] - supports OS (0, 3, 4) does not support OS (1, 2)
        # same index based scheme used for getsensorlength and getsensortype
        for header in self.headers:
            # # go into each content link to find sensors
            # contentstore = urllib2.urlopen(elem.find('content_url').text)
            # contenttree = ET.parse(contentstore)
            # header = contenttree.getroot()
            for elem in header.iter('sensor'):
                name = elem.find('name').text
                if name not in self.foundossupport.keys():
                    self.foundossupport[name] = []
                supported = [0] * 5
                for osname in elem.iter('os'):
                    supported[int(osname.text)] = 1  #if os supported mark 1 in corresponding index
                if supported not in self.foundossupport[name]:
                    self.foundossupport[name].append(supported)



    def getnames(self):
        #gets names of all sensors and how often they occur in the xml doc, returned as a dictionary
        names = []
        for header in self.headers:
            # # go into each content link to find sensors
            # contentstore = urllib2.urlopen(elem.find('content_url').text)
            # contenttree = ET.parse(contentstore)
            # header = contenttree.getroot()
            for elem in header.iter('sensor'):  #make list of all names, including repeats
                names.append(elem.find('name').text)
        return Counter(names)  #consolidate into dictionary with counts of each name and return


    def getdescriptions(self):
        # adds descriptions of sensors to founddescriptions if no description, adds none
        for header in self.headers:
            # # go into each content link to find sensors
            # contentstore = urllib2.urlopen(elem.find('content_url').text)
            # contenttree = ET.parse(contentstore)
            # header = contenttree.getroot()
            for elem in header.iter('sensor'):
                name = elem.find('name').text
                if name not in self.founddescriptions.keys():
                    self.founddescriptions[name] = []
                if elem.find('description') != None:
                    description = elem.find('description').text
                    if description not in self.founddescriptions[name]:
                        self.founddescriptions[name].append(description)
                else:
                    if 'none' not in self.founddescriptions[name]:
                        self.founddescriptions[name].append('none')


    def getresulttype(self):
        #adds result type for each sensor to foundresult tupe
        for header in self.headers:
            # # go into each content link to find sensors
            # contentstore = urllib2.urlopen(elem.find('content_url').text)
            # contenttree = ET.parse(contentstore)
            # header = contenttree.getroot()
            for elem in header.iter('sensor'):
                name = elem.find('name').text
                if name not in self.foundresulttypes.keys():
                    self.foundresulttypes[name] = []
                rtype = elem.find('result_type').text  #get result type
                if rtype not in self.foundresulttypes[name]:
                    self.foundresulttypes[name].append(rtype)


    def getsensorlength(self):
        #adds code length by character for each operating system supported by sensors in corresponding index of 5 elem list,
        #put in foundsensorlengths
        for header in self.headers:
            # # go into each content link to find sensors
            # contentstore = urllib2.urlopen(elem.find('content_url').text)
            # contenttree = ET.parse(contentstore)
            # header = contenttree.getroot()
            for elem in header.iter('sensor'):
                name = elem.find('name').text
                if name not in self.foundsensorlengths.keys():
                    self.foundsensorlengths[name] = []
                oslens = ['stub'] * 5
                for codechunk in elem.iter('sensor_query'):  #for each sensor query get code length + operating system
                    if "THIS IS A STUB" in codechunk.find('query').text:
                        continue
                    else:
                        oslens[int(codechunk.find('os').text)] = len(codechunk.find('query').text) #length of each os at corresponding os index in list (first elem = WINDOWS)
                if oslens not in self.foundsensorlengths[name]:
                    self.foundsensorlengths[name].append(oslens)


    def gethash(self):
        #put hash for each sensor in foundhashes
        for header in self.headers:
            # # go into each content link to find sensors
            # contentstore = urllib2.urlopen(elem.find('content_url').text)
            # contenttree = ET.parse(contentstore)
            # header = contenttree.getroot()
            for elem in header.iter('sensor'):
                name = elem.find('name').text
                if name not in self.foundhashes.keys():
                    self.foundhashes[name] = []
                htype = elem.find('what_hash').text  # get hash
                if htype not in self.foundhashes[name]:
                    self.foundhashes[name].append(htype)


    def getsensortypes(self):
        #add list of sensor types per os to foundsensortypes
        for header in self.headers:
            # # go into each content link to find sensors
            # contentstore = urllib2.urlopen(elem.find('content_url').text)
            # contenttree = ET.parse(contentstore)
            # header = contenttree.getroot()
            for elem in header.iter('sensor'):
                name = elem.find('name').text
                if name not in self.foundsensortypes.keys():
                    self.foundsensortypes[name] = []
                sensor_supported = ['N/A'] * 5
                for codechunk in elem.iter('sensor_query'):
                    sensor_supported[int(codechunk.find('os').text)] = codechunk.find('sensor_type').text  #sensor type per os index in sensor_supported
                if sensor_supported not in self.foundsensortypes[name]:
                    self.foundsensortypes[name].append(sensor_supported)
