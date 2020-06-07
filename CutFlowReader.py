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


class Collection:
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
        if os.path.isdir(collection_path):
            self.collection_path = os.path.normpath(collection_path+'/')
        else:
            raise ValueError("Can't find the collection path! "+ collection_path)
        if saf_file != False:
            self.saf            = SAF(saf_file=saf_file, 
                                      xsection=kwargs.get('xsection',-1))
            self.xsec           = self.saf.xsec
        else:
            self.xsec = kwargs.get('xsection',-1)
        self.collection_name    = kwargs.get('ID','SR-Collection')
        self.SRdict             = {}
        self.regiondata         = {}
        self.readCollection()
        # If lumi is not given just set it to xsec [pb]
        self.SRdict             = self.set_lumi(kwargs.get('lumi',1.0e-3))

    
    def __getattr__(self, name):
        if name in self.__dict__['SRdict'].keys():
            return self.__dict__['SRdict'][name]
        else:
            return False

    @classmethod
    def __type__(self):
        return __name__

    def __getitem__(self,name):
        return self.SRdict[name]
    
    def keys(self):
        return self.SRdict.keys()
    
    def items(self):
        return self.SRdict.items()
    
    def add_SR(self,SR):
        if SR.size() == 0:
            print(SR.name, ' has no cut')
        else:
            self.SRdict[SR.name] = SR
        return self
    
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
