# MadAnalysis 5 Interpreter For Expert Mode
 MA5 analysis output interpreter for expert mode. Parse the signal collection and construct cutflow (histogram interpreter coming soon). 

## Cutflow Collection

 * Parse all the signal regions and construct an object-base, interactable cutflow.
 * Write combined LaTeX tables for different samples.
 * Compare samples and construct validation tables which allow you to calculate the difference of the relative efficiencies for each given sample with respect to a reference sample.
 * Compare signal and background samples and calculate the figure of merit.
 * Possibility to include experimentally available cutflow data and compare it against MadAnalysis 5 cutflow output.
 * Calculate Monte Carlo uncertainty per cut on the fly
 
Examples can be found in [examples folder](https://github.com/jackaraz/ma5_expert/tree/master/examples).

Simple cutflow:
```python
from ma5_expert.CutFlowReader import Collection
Vec = Collection(collection_path='DMsimp_recast/Output/SAF/vec/sfs_atlas_conf_2019_040_0/Cutflows',
                 xsection=7.8e-02, lumi = 139.)
print Vec
#Output:
   * Signal Region : SR6j_1000
   0.    Initial
      Nentries: 200000
      Nevents : 10842.000
      Cut Eff : 1.00000
      Rel Eff : 1.00000
   1.    Preselection
      Nentries: 24595
      Nevents : 2979.391 ± 16.178
      Cut Eff : 0.27480
      Rel Eff : 0.27480
   2.    njets>=2
      Nentries: 24595
      Nevents : 2979.391 ± 16.178
      Cut Eff : 0.27480
      Rel Eff : 1.00000
   3.    njets>=6
      Nentries: 240
      Nevents : 24.207 ± 1.561
      Cut Eff : 0.00223
      Rel Eff : 0.00812
...
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

- [x] Some experimental analysis requires MC event comparison table. This needs to be added.

- [x] Combine collections with + operator and normalize to a certain luminosity with * operator.

- [x] Add MC uncertainties

- [ ] Add theoretical uncertainties
