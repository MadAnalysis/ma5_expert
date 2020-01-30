import numpy as np
import os

"""
ma5_path = '/home/jack/packages/dev_ma5/v1.8.28/madanalysis5/'
analysis = 'atlas_susy_2018_031'
sample   = '_onestepN2hN1_1100_330_200'
atlas_susy_2018_031 = SR_collection(SR_collection_path = ma5_path+analysis+'/Output/'+\
                                                         sample+'/'+analysis+'_0/Cutflows/',
                                    collection_name = 'MA5').readCollection()
"""                                   


class cut(object):
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
                self.eff      = np.float32(sumw/cut_0.sumw)
            if precut == None:
                self.rel_eff  = 1.
            else:
                if precut.sumw == 0.:
                    self.rel_eff = 1.
                else:
                    self.rel_eff  = np.float32(sumw/precut.sumw)
            self.nevt    = np.float32(self.eff*xsec)
            self.Nevents = np.float32(self.eff*xsec)
        else:
            self.nevt    = np.float32(xsec)
            self.Nevents = np.float32(xsec)
            if cut_0 == None:
                self.eff      = 1.
            else:
                self.eff      = np.float32(xsec/cut_0.Nevents)
            if precut == None:
                self.rel_eff  = 1.
            else:
                if precut.Nevents == 0.:
                    self.rel_eff = 1.
                else:
                    self.rel_eff  = np.float32(xsec/precut.Nevents)
            
    def set_lumi(self,lumi):
        self.Nevents *= 1000.*lumi
    
    def set_xsec(self,xsec):
        self.nevt    = np.float32(self.eff*xsec)
        self.Nevents = np.float32(self.eff*xsec)
        return self
    
    def Print(self):
        print '============'
        print self.Name 
        print 'Nentries: ', self.Nentries
        print 'Nevents : ', round(self.Nevents,3)
        print 'Cut Eff : ', round(self.eff,5)
        print 'Rel Eff : ', round(self.rel_eff,5)
        

class SR(object):
    def __init__(self,name):
        self.name = name
        self.cutlist = []
        self.type = 'SignalRegion'
    
    def __getitem__(self,cut_num):
        return self.cutlist[cut_num]
    
    def size(self):
        return len(self.cutlist)
    
    def items(self):
        return [(i,self.cutlist[i]) for i in range(self.size())]

    def add_cut(self,cut):
        self.cutlist.append(cut)
    
    def get_names(self):
        return [x.Name for x in self.cutlist]
    
    def get_name(self,n):
        return self.cutlist[n].Name
    
    def get_cut(self,n):
        return self.cutlist[n]
    
    def get_final_cut(self):
        return self.cutlist[self.size()-1]
    
    def isAlive(self):
        return self.get_final_cut().Nentries > 0
    
    def set_lumi(self,lumi):
        self.cutlist = [cut.set_lumi(lumi) for cut in self.cutlist]
    
    def set_xsec(self,xsec):
        self.cutlist = [cut.set_xsec(xsec) for cut in self.cutlist]
        return self
    
    def Print(self):
        for cut in self.cutlist:
            cut.Print()
        
        
class SR_collection(object):
    def __init__(self, SR_collection_path='', sample_file=False, xsection=1, dataset=False, collection_name=''):
        self.SR_collection_path = os.path.normpath(SR_collection_path+'/')
        self.type               = 'SR_collection'
        self.sample_file        = sample_file
        self.xsec               = xsection
        self.dataset_info       = dataset
        self.collection_name    = collection_name
        if os.path.isdir(SR_collection_path):
            self.SRlist             = [x.split('.')[0] for x in os.listdir(SR_collection_path)]
        else:
            self.SRlist = []
        self.SRdict             = {}
        self.readCollection()
    
    def __getattr__(self, name):
        if name in self.__dict__['SRdict'].keys():
            return self.__dict__['SRdict'][name]
        else:
            return False
    
    def __getitem__(self,name):
        return self.SRdict[name]
    
    def keys(self):
        return self.SRdict.keys()
    
    def items(self):
        return self.SRdict.items()
    
    def add_SR(self,SR):
        if SR.size() == 0:
            print SR.name, ' has no cut'
        else:
            self.SRdict[SR.name] = SR
        return self
    
    def Print(self,*args):
        for key, item in self.items():
            print 'Signal Region : ', key
            item.Print()
    
    def get_xsec(self):
        if self.dataset_info == False:
            return False
        with open(self.dataset_info, 'r') as f:
            sample = f.readlines()
        j = 0
        while j < len(sample):
            if sample[j].startswith('<SampleGlobalInfo>'):
                j+=2
                xsec = np.float64(sample[j].split()[0])
                break
            j+=1
        self.xsec = xsec

    def get_alive(self):
        temp = {}
        for key, item in self.SRdict.items():
            if item.isAlive():
                temp[key] = item
            else:
                pass
        self.SRdict = temp
    
    def readCollection(self):
        if not os.path.isdir(self.SR_collection_path):
            return False
        for sr in os.listdir(self.SR_collection_path):
            fl = os.path.join(self.SR_collection_path,sr)
            with open(fl, 'r') as f:
                cutflow = f.readlines()

            if self.xsec == 1 and self.dataset_info != False:
                self.get_xsec()
            
            currentSR = SR(sr.split('.')[0])
            
            i = 0
            while i < len(cutflow):
                if cutflow[i].startswith('<InitialCounter>'):
                    i+=2
                    current_cut = cut(Name='Presel.',
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
                    current_cut = cut(Name=cutflow[i].split('"')[1],
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
        return self
            
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