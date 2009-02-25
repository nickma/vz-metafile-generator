#!/usr/bin/env python

#===============================================================================
# Based on code for Nick by Gal - creating VZ meta files from template
#===============================================================================

### Imports
import sys
import os

### Defines
key_order = ['osname', 'osver', 'osarch', 
             'appname', 'version', 'release', 
             'summary', 'license', 
             'packages', 'package_manager',
             'distribution', 'repositories', 'description']
# ^ this is the order keys appear in the input file? change as necessary

#the signal to end of field (ex. end of the list of packages or repositories)
field_end_line = '\n'

#default template file name
default_template = 'my_tmpl'
###default_os_template = 'my_os_tmpl'

### Functions

def get_distro_name(distro_dict):
    osname = distro_dict['osname']
    osname = osname.split('\n')[0]
    osver = distro_dict['osver']
    osver = osver.split('\n')[0]
    osarch = distro_dict['osarch']
    osarch = osarch.split('\n')[0]
    return osname+'-'+osver+'-'+osarch

def input_to_list_of_dict(input_file):
    """ read input, convert to list of dictionaries """
    
    #load data from input file
    f_i = open(input_file, 'r')
    data = f_i.readlines()         
    f_i.close()
    
    #main loop
    ln = 0
    dict_lst = list()
    
    while ln < len(data):
        print '.',
        #init dictionary for the distro loop
        cur_dist = dict()
        #per distro loop
        for k in key_order:
            #create a dict
            cur_dist[k] = ''
            while data[ln] != field_end_line:
                cur_dist[k] += data[ln]
                ln += 1
            #end while data
            ln+=1
        #end for k in key_order
        dict_lst.append(cur_dist)
    #end while loop
    print '.'
    return dict_lst
    
def dict_to_file(mydict, template, outfile):
    """ write a distro dictionary mydict to outfile according to template (tempalte is a string)"""
    f = open(outfile, 'w')
    f.write(template % mydict)
    f.close()
    
def load_template(template_file):
    """ load a template from the file template_file, returns the template as a long string """
    f = open(template_file, 'r')
    data = f.readlines()
    f.close()
    tmpl = ''.join(data)
    return tmpl

def main(input_file, template_file):
    #load template
    print 'loading template' 
    tmpl = load_template(template_file)
    
    #load data from input file
    print 'reading input file',      #"," at end of a print command aborts the new line
    distro_list = input_to_list_of_dict(input_file)
   
    #loop over distro list and output to files 
    print 'writing files', 
    for distro in distro_list:
        print '.',
        dict_to_file(distro, tmpl, 'metafile-vz-'+get_distro_name(distro))
    print 'Done!'
    print 'Convert Metafiles to VZ rpm using vzmktmpl'
    
    
### main
if __name__ == '__main__':
    if len(sys.argv) == 2:
        main(sys.argv[1], default_template)
    elif len(sys.argv) == 3:
        main(sys.argv[1], sys.argv[2])
    else:
        print 'invalid number of arguments'
        print 'usage: %s input_file [template_file]' % sys.argv[0]

