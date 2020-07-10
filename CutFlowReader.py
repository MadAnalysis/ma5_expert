#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 31 10:37:07 2020

@author  : jackaraz
@contact : Jack Y. Araz <jackaraz@gmail.com>
"""

import os
from SafReader import SAF
from CutFlowObjects import Cut, SignalRegion


class Collection(object):
    def __init__(self, collection_path='', saf_file=False, **kwargs):
        """

        Parameters
        ----------
        collection_path : STR
            The path where all the cutflow saf files exist. The default is ''.
        saf_file : STR, optional
            Sample information file. The default is False.
        **kwargs : 
            xsection : FLOAT
                Cross section value overwrite. The default is -1
            ID : STR 
                Name of the collection. The default is SR-Collection
            lumi : FLOAT
                Luminosity overwrite. The Default is 1e-3

        Raises
        ------
        ValueError
            Raised if can't find collection path.

        Returns
        -------
        Cut flow collection.

        """
        self.SR_collection_path = ''
        xsec    = kwargs.get('xsection',-1)
        nevents = kwargs.get('nevents', -1)
        lumi    = kwargs.get('lumi',1.0e-3)
        if nevents > 0:
            xsec = nevents
            lumi = 1e-3
        
        if saf_file != False:
            self.saf            = SAF(saf_file=saf_file, 
                                      xsection=xsec)
            self.xsec           = self.saf.xsec
        else:
            self.xsec = xsec
        self.collection_name    = kwargs.get('ID','SR-Collection')
        self.SRdict             = {}
        self.regiondata         = {}

        if collection_path != '':
            if os.path.isdir(collection_path):
                self.collection_path = os.path.normpath(collection_path+'/')
                self.readCollection()
            else:
                raise ValueError("Can't find the collection path! "+ collection_path)
        # If lumi is not given just set it to xsec [pb]
        self.SRdict             = self.set_lumi(lumi)

    @classmethod
    def __type__(self):
        return __name__

    def __getitem__(self,name):
        return self.SRdict[name]
    
    def keys(self):
        return self.SRdict.keys()

    def items(self):
        return self.SRdict.items()

    def add_SR(self,SR_name,cut_names,cut_values,raw=[]):
        if len(cut_names) != len(cut_values):
            raise ValueError("Cut names does not match with the values: {:.0f} != {:.0f}".format(len(cut_names),len(cut_values)))
        if raw == []:
            raw = [1e99]*len(cut_names)
        else:
            if len(raw) != len(cut_values):
                raise ValueError("Cut values does not match with the raw number of events: {:.0f} != {:.0f}".format(len(raw),len(cut_values)))
        SR = SignalRegion(SR_name)
        for ix, (name, val, entries) in enumerate(zip(cut_names,cut_values,raw)):
            if ix == 0:
                current_cut = Cut(Name=name, xsec=val, Nentries=entries)
                cut_0       = current_cut
                precut      = current_cut
            else:
                current_cut = Cut(Name=name, precut=precut,cut_0=cut_0, xsec=val, Nentries=entries)
                precut      = current_cut
            SR.add_cut(current_cut)
        self.SRdict[SR_name] = SR


    def Print(self,*args):
        for key, item in self.items():
            print('Signal Region : ', key)
            item.Print()

    def get_alive(self):
        temp = {}
        for key, item in self.SRdict.items():
            if item.isAlive():
                temp[key] = item
            else:
                pass
        self.SRdict = temp
    
    def set_lumi(self,lumi):
        if lumi <= 0:
            return self.SRdict
        new_SRdict = {}
        for key, item in self.SRdict.items():
            new_SRdict[key] = item.set_lumi(lumi)
        return new_SRdict
    
    def readCollection(self):
        if not os.path.isdir(self.collection_path):
            return False
        for sr in os.listdir(self.collection_path):
            fl = os.path.join(self.collection_path,sr)
            with open(fl, 'r') as f:
                cutflow = f.readlines()

            currentSR = SignalRegion(sr.split('.')[0])
            
            i = 0
            while i < len(cutflow):
                if cutflow[i].startswith('<InitialCounter>'):
                    i+=2
                    current_cut = Cut(Name='Presel.',
                                      Nentries=int(cutflow[i].split()[0])+\
                                               int(cutflow[i].split()[1]),
                                      sumw=float(cutflow[i+1].split()[0])+\
                                           float(cutflow[i+1].split()[1]),
                                      sumw2=float(cutflow[i+2].split()[0])+\
                                            float(cutflow[i+2].split()[1]), 
                                      xsec=self.xsec)
                    currentSR.add_cut(current_cut)
                    cut_0  = current_cut
                    precut = current_cut
                elif cutflow[i].startswith('<Counter>'):
                    i+=1
                    current_cut = Cut(Name=cutflow[i].split('"')[1],
                                      Nentries=int(cutflow[i+1].split()[0])+\
                                               int(cutflow[i+1].split()[1]),
                                      sumw=float(cutflow[i+2].split()[0])+\
                                           float(cutflow[i+2].split()[1]),
                                      sumw2=float(cutflow[i+3].split()[0])+\
                                            float(cutflow[i+3].split()[1]), 
                                      xsec   = self.xsec,
                                      precut = precut,
                                      cut_0  = cut_0)
                    currentSR.add_cut(current_cut)
                    precut = current_cut
                i+=1
            self.SRdict[currentSR.name] = currentSR
            self.regiondata[currentSR.name] = currentSR.regiondata()
