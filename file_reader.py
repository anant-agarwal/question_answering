#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 31 20:40:50 2016

"""
import re
import xml.etree.ElementTree as ET
import os

def read_xml_file( path_to_file ):
    read_handle = open( path_to_file,"rb")
    #
    # Get rid of the first line before parsing as xml
    # If we are planning to use the first line for ranking answers, we can
    #store the first line and return first line along with the sentence
    #
    read_handle.readline()
    try :
        tree = ET.parse(read_handle)
        root = tree.getroot()
        for child in root.iter('TEXT') :
            sentence = child.text
        return sentence
    except:
        print path_to_file
        return ''

def read_file_text(path_to_file):
    read_handle = open( path_to_file,"r")
    read_handle.readline()
    text = read_handle.read()
    text = re.sub('<[^>]*>', '', text)
    return text

def list_all_files( path ):
    all_files = os.listdir(path);
    all_text_files = [];
    for file_name in all_files:
        if (file_name.isdigit()):
            all_text_files.append(int(file_name));
    return (all_text_files)
