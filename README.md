# MadAnalysis 5 Interpreter For Expert Mode
 MA5 analysis output reader for expert mode. Parse the signal collection and construct cutflow.

# How to get LaTeX output of the cutflow:

```CutFlowReader``` Collects the signal regions under the main CutFlow path and constructs a collection of signal regions. Sample information folder can be inputted to parse cross section value, or it can be overwritten entirely. ```CutFlowTable``` generates two types of cutflow table;
  * Signal vs Background comparison table: The reference sample will be treated as background, and several different statistical variables are calculated with respect to the background. Other samples will be treated as individual signal samples.
  * Sample comparison table: Each sample is compared to the reference sample with respect to their relative cut efficiencies.

```python
from ma5_expert.CutFlowReader import Collection
from ma5_expert.CutFlowTable  import CutFlowTable

# overwrite lumi to 1/1000 to set xsec as the initial number of events.
# by default first sample is the reference sample (or bkg) 
# set reference sample by using ref_sample = INT, default 0
# Each sample must have the same cutflow!

Delphes = Collection(collection_path=ma5_path+'cms_sus_16_048_delphes/Output/SAF/defaultset/cms_sus_16_048/Cutflows',
                     saf_file=ma5_path+'cms_sus_16_048_delphes/Output/SAF/defaultset/defaultset.saf', 
                     lumi=1./1000.,xsection=172004.)
Jets    = Collection(collection_path=ma5_path+'cms_sus_16_048_jets/Output/SAF/defaultset/cms_sus_16_048/Cutflows',
                     saf_file=ma5_path+'cms_sus_16_048_jets/Output/SAF/defaultset/defaultset.saf', 
                     lumi=1./1000.,xsection=172004.)
Const   = Collection(collection_path=ma5_path+'cms_sus_16_048_const/Output/SAF/defaultset/cms_sus_16_048/Cutflows',
                     saf_file=ma5_path+'cms_sus_16_048_const/Output/SAF/defaultset/defaultset.saf', 
                     lumi=1./1000.,xsection=172004.)

table = CutFlowTable(Delphes,Jets,Const,sample_names=['Delphes','SFS [Jets]','SFS [Constituents]'])

file = open('cms_sus_16_048.tex','w')
file.write(r'\documentclass[11pt]{article}'+'\n'+\
           r'\usepackage{pdflscape}'+'\n'+\
           r'\begin{document}'+'\n'+\
           r'\begin{landscape}'+'\n\n\n\n')

table.write_signal_comparison_table(file) 
# to write in to a file give the file obj as input. 
# This will create signal vs bkg comparison table

file.write('\n\n\n\n'+r'\end{landscape}'+'\n'+r'\end{document}'+'\n')
file.close()

table.write_comparison_table() 
# this will print the table on the screen. 
# This will create a sample comparison table
```

## TODO

- [ ] Clean cutflow reader needs optimization and clarity

- [x] Generalize table writer and add latex writer

- [ ] Histogram reader

- [ ] Overall Ma5 Analysis parser

- [ ] Some experimental analysis requires MC event comparison table. This needs to be added.
