#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 30 17:50:43 2020

@author: jackaraz
contact: jackaraz@gmail.com
"""
from CutFlowReader import *
from FoM import FoM
import os


class CutFlowTable:
    def __init__(self, *args,**kwargs):
        """
        Parameters
        ----------
        *args : list of SR Collection
            This list contains SR collections i.e. background and signal. It can 
            have multiple collections but all collections has to have same cutflow.
        **kwargs : 
            ref_sample : INT
                The index of the reference sample in the SR collection.
            sample_names : LIST
                Names of the samples.
        Returns
        -------
        None.
        """
        samples = list(args)
        sample_names = kwargs.get('sample_names',[])
        if len(sample_names) == len(samples):
            self.sample_names = sample_names
        else:
            self.sample_names = ['Sample '+str(x) for x in range(len(samples))]
        
        ref_sample = kwargs.get('ref_sample',0)
        self.ref_name = self.sample_names[ref_sample]
        self.ref_sample = samples[ref_sample]
        samples.remove(self.ref_sample)
        self.sample_names.remove(self.ref_name)
        self.samples = samples
    
    def _sorter(self,x):
        return self.ref_sample[x].get_final_cut().Nentries
    
    def write_comparison_table(self,*args,**kwargs):
        """
        Parameters
        ----------
        *args : FILE
            Optional, if there is a file input, tables will be written in the 
            file otherwise all will be printed on the screen.
        **kwargs : 
            only_alive : BOOLEAN (default True)
                only write the SRs which has more than zero yield for reference
                collection.
        Returns
        -------
        LaTeX tables of signal regions.
        """
        SR_list = self.ref_sample.keys()
        if kwargs.get('only_alive',True): 
            SR_list = [x for x in SR_list if self.ref_sample[x].isAlive()]
        SR_list.sort(key=self._sorter, reverse=True)
        file = None
        if len(args) > 0:
            file = args[0]
            file.write(r'\documentclass[11pt]{article}'+'\n'+\
                       r'\usepackage{pdflscape}'+'\n'+\
                       r'\begin{document}'+'\n'+\
                       r'\begin{landscape}'+'\n\n\n\n')
        for SR in SR_list:
            txt = '\n\n%% '+SR+'\n\n'
            txt+='\\begin{table}[h]\n'
            txt+='  \\begin{center}\n'
            txt+='  \\renewcommand{\\arraystretch}{1.}\n'
            n_rows = len(self.samples)
            txt+='    \\begin{tabular}{c||cc|'+'|'.join(['ccc']*(n_rows))+'}\n'
            txt+='      & '

            # Write header of the table
            txt += '\\multicolumn{2}{c|}{'+self.ref_name+'} &'
            for smp in self.sample_names:
                txt += '\\multicolumn{3}{c'+(self.sample_names.index(smp) != len(self.sample_names)-1)*'|'+'}{'+smp+'} '
                if not self.sample_names.index(smp) == len(self.sample_names)-1:
                    txt += '&'
                else:
                    txt += '\\\ \\hline\\hline\n'
            txt +='      & Events & $\\varepsilon$ &'
            for smp in self.sample_names:
                txt += 'Events & $\\varepsilon$ & Ratio [\%]'
                if not self.sample_names.index(smp) == len(self.sample_names)-1:
                    txt += ' & '
                else:
                    txt += '\\\ \\hline\n'
            # write cutflow
            for cutID, cut in self.ref_sample[SR].items():
                name = cut.Name
                if '$' not in name:
                    name = name.replace('_',' ')
                txt += '      '+name.ljust(40,' ') + '& '
                if cutID == 0:
                    txt += '{:.1f} & - & '.format(cut.Nevents)
                else:
                    txt += '{:.1f} & {:.3f} & '.format(cut.Nevents,cut.rel_eff)
                
                for sample in self.samples:
                    smp = sample[SR]
                    if cutID == 0:
                        txt += '{:.1f} & - & - '.format(smp[cutID].Nevents)
                    elif cutID > 0 and cut.rel_eff == 0:
                        txt += '{:.1f} & {:.3f} & - '.format(smp[cutID].Nevents,smp[cutID].rel_eff)
                    else:
                        rel_eff =1-(smp[cutID].rel_eff/cut.rel_eff)
                        txt += '{:.1f} & {:.3f} & {:.1f}\\% '.format(smp[cutID].Nevents,smp[cutID].rel_eff,rel_eff*100.)
                    if smp != self.samples[-1][SR]:
                        txt += ' & '  
                    else:
                        txt += r'\\'
                txt += '\n'
            entries = [x.Nentries for x in [self.ref_sample[SR].get_final_cut()]+\
                                           [sample[SR].get_final_cut() for sample in self.samples]]
            txt+='    \\end{tabular}\n'
            txt+='    \\caption{'+SR.replace('_',' ')+\
            (any([x<100 for x in entries]))*(' (This SR needs more event:: MC event count = '+\
                                             ', '.join([str(x) for x in entries])+')')+'}\n'
            txt+='  \\end{center}\n'
            txt+='\\end{table}\n'
            if file != None:
                file.write(txt)
                file.write('\n\n\n\n'+r'\end{landscape}'+'\n'+r'\end{document}'+'\n')
                self.WriteMake(file,make=kwargs.get('make',True))
            else:
                print(txt)
    
    def write_signal_comparison_table(self,*args,**kwargs):
        """

        Parameters
        ----------
        *args : FILE
            Optional, if there is a file input, tables will be written in the 
            file otherwise all will be printed on the screen.
        **kwargs : 
            sys : FLOAT ]0,1]
                Systematic uncertainty, default 20%
            only_alive : BOOLEAN (default True)
                only write the SRs which has more than zero yield for reference
                collection.
        Returns
        -------
        Signal over Background comparison table.

        """
        sys = kwargs.get('sys',0.2)
        SR_list = self.ref_sample.keys()
        if kwargs.get('only_alive',True): 
            SR_list = [x for x in SR_list if self.ref_sample[x].isAlive()]
        SR_list.sort(key=self._sorter, reverse=True)
        file = None
        if len(args) > 0:
            file = args[0]
        for SR in SR_list:
            txt = '\n\n%% '+SR+'\n\n'
            txt+='\\begin{table}[h]\n'
            txt+='  \\begin{center}\n'
            txt+='  \\renewcommand{\\arraystretch}{1.}\n'
            n_rows = len(self.samples)
            txt+='    \\begin{tabular}{c||cc|'+'|'.join(['cc']*(n_rows))+'}\n'
            txt+='      & '

            # Write header of the table
            txt += '\\multicolumn{2}{c|}{'+self.ref_name+'} &'
            for smp in self.sample_names:
                txt += '\\multicolumn{2}{c'+(self.sample_names.index(smp) != len(self.sample_names)-1)*'|'+'}{'+smp+'} '
                if not self.sample_names.index(smp) == len(self.sample_names)-1:
                    txt += '&'
                else:
                    txt += '\\\ \\hline\\hline\n'
            txt +='      & Events & $\\varepsilon$ &'
            for smp in self.sample_names:
                txt += 'Events & $\\varepsilon$ '
                if not self.sample_names.index(smp) == len(self.sample_names)-1:
                    txt += ' & '
                else:
                    txt += '\\\ \\hline\n'
            # write cutflow
            for cutID, cut in self.ref_sample[SR].items():
                name = cut.Name
                if '$' not in name:
                    name = name.replace('_',' ')
                txt += '      '+name.ljust(40,' ') + '& '
                if cutID == 0:
                    txt += '{:.1f} & - &'.format(cut.Nevents,cut.rel_eff*100.)
                else:
                    txt += '{:.1f} & {:.1f}\\% &'.format(cut.Nevents,cut.rel_eff*100.)
                
                for sample in self.samples:
                    smp = sample[SR]
                    if cutID == 0:
                        txt += '{:.1f} & - '.format(smp[cutID].Nevents,smp[cutID].rel_eff*100.)
                    elif cutID > 0 and cut.rel_eff == 0:
                        txt += '{:.1f} & {:.1f}\\% '.format(smp[cutID].Nevents,smp[cutID].rel_eff*100.)
                    else:
                        txt += '{:.1f} & {:.1f}\\% '.format(smp[cutID].Nevents,smp[cutID].rel_eff*100.)
                    if smp != self.samples[-1][SR]:
                        txt += ' & '  
                    else:
                        txt += r'\\'

                if cut == self.ref_sample[SR].get_final_cut():
                    txt += r'\hline\hline'
                    fom = FoM(smp[cutID].Nevents,cut.Nevents,sys=sys)
                    txt += '\n     \\multicolumn{3}{c}{$S/B$} &'
                    for sample in self.samples:
                        smp = sample[SR]
                        txt += '\\multicolumn{2}{c}{'+'{:.3f}\\%'.format(100.*fom.S_B)+'}'
                        if smp != self.samples[-1][SR]:
                            txt += ' & ' 
                        else:
                            txt += r'\\'
 
                    txt += '\n     \\multicolumn{3}{c}{$S/S+B$} &'
                    for sample in self.samples:
                        smp = sample[SR]
                        txt += '\\multicolumn{2}{c}{'+'{:.3f}\\%'.format(100.*fom.S_SB)+'}'
                        if smp != self.samples[-1][SR]:
                            txt += ' & ' 
                        else:
                            txt += r'\\'

                               
                    txt += '\n     \\multicolumn{3}{c}{$S/\sqrt{B}$}  &'
                    for sample in self.samples:
                        smp = sample[SR]
                        txt += '\\multicolumn{2}{c}{'+\
                                '{:.3f}'.format(fom.sig)+'}'
                        if smp != self.samples[-1][SR]:
                            txt += ' & ' 
                        else:
                            txt += r'\\'
                    
                    txt += '\n     \\multicolumn{3}{c}{$S/\sqrt{B+(B\Delta_{sys})^2}$}  &'
                    for sample in self.samples:
                        smp = sample[SR]
                        txt += '\\multicolumn{2}{c}{'+\
                                '{:.3f}'.format(fom.sig_sys)+'}'
                        if smp != self.samples[-1][SR]:
                            txt += ' & ' 
                        else:
                            txt += r'\\'
                            
                    txt += '\n     \\multicolumn{3}{c}{$Z_A$} &'
                    for sample in self.samples:
                        smp = sample[SR]
                        txt += '\\multicolumn{2}{c}{'+\
                                '${:.3f} \\pm {:.3f} $'.format(fom.ZA,fom.ZA_err)+'}'
                        if smp != self.samples[-1][SR]:
                            txt += ' & ' 
                        else:
                            txt += r'\\'
                    
                txt += '\n'

            txt+='    \\end{tabular}\n'
            txt+='    \\caption{'+SR.replace('_',' ')+\
            (cut.Nentries<100)*'(This SR needs more event:: MC event count = {:.0f})'.format(cut.Nentries)+'}\n' 
            txt+='  \\end{center}\n'
            txt+='\\end{table}\n'
            if file != None:
                file.write(txt)
            else:
                print(txt)

    def WriteMake(self,file,make=True):
        if os.path.isfile(file.name):
            make = open('Makefile','w')
            make.write('all:\n')
            make.write('\tpdflatex '+file.name[:4]+'\n'+\
                       '\tpdflatex '+file.name[:4]+'\n'+\
                       '\trm -f *.aux *.log *.out *.toc *.blg *.dvi *.t1 *.1 *.mp *spl\n'+\
                       'clean:\n'+\
                       '\trm -f *.aux *.log *.out *.toc *.blg *.dvi *.t1 *.1 *.mp *spl *.lol *Notes.bib\n')
            if make:
                try:
                    file.close()
                    os.system('make')
                except:
                    print 'Compilation failed.'




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
    size = len(sr_list[0])
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
            if sr>0 and sr_list[0][cut].Nevents>0:
                txt += str(round(sr_list[1][cut].Nevents/\
                                 sr_list[0][cut].Nevents,3)).ljust(9, ' ') + ' | '
            #else:
                #txt += ' '.ljust(9, ' ') + ' | '
        if cut % 2 == 0 and colored:
            txt += u' \u001b[0m' 
        print txt
    print 
