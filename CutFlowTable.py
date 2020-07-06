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
            make : BOOL
                Write the Makefile -> (default, True)
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
            file.write(r'\documentclass[12pt]{article}'+'\n'+\
                       r'\usepackage{pdflscape,slashed}'+'\n'+\
                       r'\begin{document}'+'\n'+\
                       r'\begin{landscape}'+'\n\n\n\n'+\
                       '%%%%%% \\delta := |Ref. smp - smp_i| / ref_smp\n\n\n\n')
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
                txt += 'Events & $\\varepsilon$ & $\\delta$ [\%]'
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
                        rel_eff =abs(1-(smp[cutID].rel_eff/cut.rel_eff))
                        txt += '{:.1f} & {:.3f} & {:.1f} '.format(smp[cutID].Nevents,smp[cutID].rel_eff,rel_eff*100.)
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
            else:
                print(txt)
        if file != None:
            file.write('\n\n\n\n'+r'\end{landscape}'+'\n'+r'\end{document}'+'\n')
            if kwargs.get('make',True):
                self.WriteMake(file,make=kwargs.get('make',True))


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
            sys_sig : BOOL
                Calculate S/sqrt(B+(B*sys)^2) -> (default False)
            ZA : BOOL
                Calculate Assimov significance -> (default False)
            make : BOOL
                Write the Makefile -> (default, True)
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
            file.write(r'\documentclass[12pt]{article}'+'\n'+\
                       r'\usepackage{pdflscape,slashed}'+'\n'+\
                       r'\begin{document}'+'\n'+\
                       r'\begin{landscape}'+'\n\n\n\n')
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
                    txt += '{:.1f} & - &'.format(cut.Nevents)
                else:
                    txt += '{:.1f} & {:.3f} &'.format(cut.Nevents,cut.rel_eff)
                
                for sample in self.samples:
                    smp = sample[SR]
                    if cutID == 0:
                        txt += '{:.1f} & - '.format(smp[cutID].Nevents)
                    elif cutID > 0 and cut.rel_eff == 0:
                        txt += '{:.1f} & {:.3f} '.format(smp[cutID].Nevents,smp[cutID].rel_eff)
                    else:
                        txt += '{:.1f} & {:.3f} '.format(smp[cutID].Nevents,smp[cutID].rel_eff)
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

                    if kwargs.get('sig_sys',False):
                        txt += '\n     \\multicolumn{3}{c}{$S/\sqrt{B+(B\Delta_{sys})^2}$}  &'
                        for sample in self.samples:
                            smp = sample[SR]
                            txt += '\\multicolumn{2}{c}{'+\
                                    '{:.3f}'.format(fom.sig_sys)+'}'
                            if smp != self.samples[-1][SR]:
                                txt += ' & ' 
                            else:
                                txt += r'\\'

                    if kwargs.get('ZA',False):
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
        if file != None:
            file.write('\n\n\n\n'+r'\end{landscape}'+'\n'+r'\end{document}'+'\n')
            if kwargs.get('make',True):
                self.WriteMake(file,make=kwargs.get('make',True))


    def WriteMake(self,file,make=True):
        if not file.name.endswith('.tex'):
            raise ValueError('Input does not have .tex extention.')
        if os.path.isfile(file.name):
            make = open('Makefile','w')
            make.write('all:\n')
            make.write('\tpdflatex '+file.name[:-4]+'\n'+\
                       '\tpdflatex '+file.name[:-4]+'\n'+\
                       '\trm -f *.aux *.log *.out *.toc *.blg *.dvi *.t1 *.1 *.mp *spl\n'+\
                       'clean:\n'+\
                       '\trm -f *.aux *.log *.out *.toc *.blg *.dvi *.t1 *.1 *.mp *spl *.lol *Notes.bib\n')
            if make:
                try:
                    file.close()
                    os.system('make')
                except:
                    print 'Compilation failed.'
        else:
            raise ValueError('Can not find '+file.name)
