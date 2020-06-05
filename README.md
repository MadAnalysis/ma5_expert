# MA5lib
 MA5 analysis output reader for expert mode. Parse the signal collection and construct cutflow.

* CutFlowReader:

Collects the signal regions under the main CutFlow path and constructs a collection of signal regions.

```python
from MA5lib.CutFlowReader import Collection
from MA5lib.CutFlowTable import CutFlowTable

# overwrite lumi to 1/1000 to set xsec as initial number of events.
# by default first sample is the refference sample (or bkg) 
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
# This will create sample comparison table
```

## TODO

* Clean cutflow reader needs optimization and clarity

* Generalize table writer and add latex writer

* Histogram reader
