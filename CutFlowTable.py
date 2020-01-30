#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 30 17:50:43 2020

@author: jackaraz
"""
from MA5_CutReader import *

def Experimental_CutFlow(SR,SR_name,cut_flow):
    if len(SR_name) != len(cut_flow):
        print 'Size does not match: ', len(SR_name) , len(cut_flow)
        return False
    for i in range(len(cut_flow)):
        if i == 0:
            current_cut = cut(Name=SR_name[i], xsec=cut_flow[i])
            cut_0       = current_cut
            precut      = current_cut
        else:
            current_cut = cut(Name=SR_name[i], precut=precut,cut_0=cut_0, xsec=cut_flow[i])
            precut      = current_cut
        SR.add_cut(current_cut)
    return SR

def compare(*args,**kwargs):
    SR_coll = []
    for item in args:
        if 'type' in item.__dict__.keys():
            if item.type == 'SR_collection':
                SR_coll.append(item)

    colored = True
    SR      = None
    if 'colored' in kwargs.keys():
        colored = kwargs['colored']
    if 'SR' in kwargs.keys():
        SR = kwargs['SR']
    
    #sr_name_size = {}
    #for SR in SR_coll[0].keys():
    #    sr_name_size[SR] = max([len(x.Name)+2 for x in SR_coll[0][SR].get_names()])
    #    print ''.ljust(sr_name_size[SR], '='),SR_coll[0][SR].name
    #    for inpt in SR_coll:
    #    print ''.ljust(sr_name_size[SR], ' ')+
    
    
    sr_list = list(args)
    print ''.ljust(54, '='),sr_list[0].name
    size = sr_list[0].size()
    print ''.ljust(55, ' ') + 'ATLAS'.ljust(15, ' ') + ' | '+'MA5'.ljust(15, ' ') + ' | '+'MA5/ATLAS'.ljust(8, ' ') + ' | '
    #print ''.ljust(55, ' ') + '------'.ljust(6, ' ') + ' | '+'------'.ljust(6, ' ') + ' | '+'--------'.ljust(8, ' ') + ' | '

    for cut in range(size):
        txt = ''
        if cut%2 == 0 and colored:
            txt += u'\u001b[31m'
        txt += sr_list[0].get_cut(cut).Name.ljust(55, ' ')
        for sr in range(len(sr_list)):
            txt += str(round(sr_list[sr][cut].Nevents,1)).ljust(6, ' ') + ' | '
            txt += str(round(sr_list[sr][cut].rel_eff,3)).ljust(6, ' ') + ' | '
            if sr>0:
                txt += str(round(sr_list[1][cut].Nevents/\
                                 sr_list[0][cut].Nevents,3)).ljust(9, ' ') + ' | '
        if cut % 2 == 0 and colored:
            txt += u' \u001b[0m' 
        print txt
    print 