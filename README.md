# MadAnalysis 5 Interpreter For Expert Mode
 MA5 analysis output interpreter for expert mode. Parse the signal collection and construct cutflow (histogram interpreter coming soon). 

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

table.write_signal_comparison_table(open('cms_sus_16_048.tex','w')) 
# to write in to a file give the file obj as input. 
# This will create signal vs bkg comparison table

table.write_comparison_table() 
# this will print the table on the screen. 
# This will create a sample comparison table
```

One can also add a cutflow from another table instead of Ma5 framework. But SR and cut names should match if one wants to write a table
```python
ATLAS = Collection() 
ATLAS.add_SR('MySR',['cut 0','cut 1','cut 2'],[10,5,1])
```

`ATLAS.Print()` will print the following output

```
('Signal Region : ', 'MySR')
============
cut 0
Nentries: -1
Nevents : 10.000
Cut Eff : 1.00000
Rel Eff : 1.00000
============
cut 1
Nentries: -1
Nevents : 5.000
Cut Eff : 0.50000
Rel Eff : 0.50000
============
cut 2
Nentries: -1
Nevents : 1.000
Cut Eff : 0.10000
Rel Eff : 0.20000
```

## Citation 
Developed for [arXiv:2006.09387](http://arxiv.org/abs/2006.09387)
```
@article{1801696,
    author = "Araz, Jack Y. and Fuks, Benjamin and Polykratis, Georgios",
    title = "{Simplified fast detector simulation in MadAnalysis 5}",
    eprint = "2006.09387",
    archivePrefix = "arXiv",
    primaryClass = "hep-ph",
    month = "6",
    year = "2020"
}
```


## TODO

- [ ] Clean cutflow reader needs optimization and clarity

- [x] Generalize table writer and add latex writer

- [ ] Histogram reader

- [ ] Overall Ma5 Analysis parser

- [ ] Some experimental analysis requires MC event comparison table. This needs to be added.
