#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 31 10:37:07 2020

@author  : jackaraz
@contact : Jack Y. Araz <jackaraz@gmail.com>
"""

class Cut(object):
    def __init__(self,Name=-1,Nentries=-1,sumw=-1,sumw2=-1, precut=None,cut_0=None, xsec=1.):
        self.Name     = str(Name)
        self.Nentries = Nentries
        self.type     = 'Cut'
        if sumw >= 0:
            self.sumw     = sumw
            self.sumw2    = sumw2
            if cut_0 == None:
                self.eff      = 1.
            else:
                self.eff      = round(sumw/cut_0.sumw,8)
            if precut == None:
                self.rel_eff  = 1.
            else:
                if precut.sumw == 0.:
                    self.rel_eff = 1.
                else:
                    self.rel_eff  = round(sumw/precut.sumw,8)
            self.nevt    = round(self.eff*xsec,8)
            self.Nevents = round(self.eff*xsec,8)
        else:
            self.nevt    = float(xsec)
            self.Nevents = float(xsec)
            if cut_0 == None:
                self.eff      = 1.
            else:
                self.eff      = round(xsec/cut_0.Nevents,8)
            if precut == None:
                self.rel_eff  = 1.
            else:
                if precut.Nevents == 0.:
                    self.rel_eff = 1.
                else:
                    self.rel_eff  = round(xsec/precut.Nevents,8)

    @classmethod
    def __type__(self):
        return __name__

    def set_lumi(self,lumi):
        self.Nevents *= 1000.*lumi
        return self
    
    def set_xsec(self,xsec):
        self.nevt    = round(self.eff*xsec, 8)
        self.Nevents = round(self.eff*xsec, 8)
        return self
    
    def Print(self):
        print('============')
        print(self.Name)
        print('Nentries: {:.0f}'.format(self.Nentries))
        print('Nevents : {:.3f}'.format(self.Nevents))
        print('Cut Eff : {:.5f}'.format(self.eff))
        print('Rel Eff : {:.5f}'.format(self.rel_eff))
        

class SignalRegion(object):
    def __init__(self,name):
        self.name = name
        self.cutlist = []

    def __getitem__(self,cut_num):
        return self.cutlist[cut_num]

    @classmethod
    def __type__(self):
        return __name__

    def __len__(self):
        return len(self.cutlist)

    def items(self):
        return [(i,self.cutlist[i]) for i in range(len(self.cutlist))]

    def add_cut(self,cut):
        self.cutlist.append(cut)
    
    def get_names(self):
        return [x.Name for x in self.cutlist]

    def get_name(self,n):
        return self.cutlist[n].Name

    def get_cut(self,n):
        return self.cutlist[n]

    def get_final_cut(self):
        return self.cutlist[len(self)-1]

    def isAlive(self):
        return self.get_final_cut().Nentries > 0

    def set_lumi(self,lumi):
        self.cutlist = [cut.set_lumi(lumi) for cut in self.cutlist]
        return self

    def set_xsec(self,xsec):
        self.cutlist = [cut.set_xsec(xsec) for cut in self.cutlist]
        return self
    
    def regiondata(self):
        return {self.name : {'Nf' : self.get_final_cut().sumw,
                             'N0' : self.get_cut(0).sumw}}

    def Print(self):
        for cut in self.cutlist:
            cut.Print()