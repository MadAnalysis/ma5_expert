# MadAnalysis 5 Interpreter For Expert Mode
[![EPJC](https://img.shields.io/static/v1?style=plastic&label=DOI&message=10.1140/epjc/s10052-021-09052-5&color=blue)](https://doi.org/10.1140/epjc/s10052-021-09052-5)
[![arxiv](https://img.shields.io/static/v1?style=plastic&label=arXiv&message=2006.09387&color=brightgreen)](https://arxiv.org/abs/2006.09387)

[![CI](https://github.com/MadAnalysis/ma5_expert/actions/workflows/pytest.yml/badge.svg?style=plastic)](https://github.com/MadAnalysis/ma5_expert/actions/workflows/pytest.yml)

 MadAnalysis 5 output interpreter for expert mode. Parses the cutflow and histogram collections and 
 constructs it with an interactable interface. 

## Installation
`pip install ma5-expert`

## Outline
* [Cutflow Collection](#cutflow-collection)
* [Histogram Collection](#histogram-collection)
* [Integration to Public Analysis Database through MadAnalysis](#integration-to-public-analysis-database-through-madanalysis)
* [Citation](#citation)

Examples can be found in [examples folder](https://github.com/jackaraz/ma5_expert/tree/master/docs/examples).

### Cutflow Collection

 * Parse all the signal regions and construct an object-base, interactable cutflow.
 * Write combined LaTeX tables for different samples.
 * Compare samples and construct validation tables which allow you to calculate the difference of the relative efficiencies for each given sample with respect to a reference sample.
 * Compare signal and background samples and calculate the figure of merit.
 * Possibility to include experimentally available cutflow data and compare it against MadAnalysis 5 cutflow output.
 * Calculate Monte Carlo uncertainty per cut on the fly


* Simple cutflow:

`CutFlowCollection` needs `CutFlows` path of your sample in MadAnalysis 5 Analysis folder.
We provide an ma5 directory in `examples` folder so we will go through and the code using that.
Parsing a cutflow simply requires the path of the `CutFlows` folder and optionally `xsection` [pb], `lumi` [1/fb]
and/or `Nevents`. Note that `xsec` overwrites the number of events option, if provided number of events
are always calculated using the cross section.

```python
import ma5_expert as ma5

sample = ma5.cutflow.Collection(
        "docs/examples/mass1000005_300.0_mass1000022_60.0_mass1000023_250.0_xs_5.689/Output/SAF/defaultset/atlas_susy_2018_31/Cutflows",
        xsection = 5.689, lumi = 139.
)
```
Here the first input is the path of the `CutFlows` folder and the rest are simply cross section and 
luminosity information. One can see the signal regions by simply printing the `keys` of the `CutFlowCollection` object;
```python
print(sample.SRnames)
# Output: 
# ['SRC_28', 'SRA_M', 'SRA_L', 'SRA_H', 'SRA', 'SRC', 'SRB', 'SRC_26', 'SRC_24', 'SRC_22']
```
Each signal region is accessible through `CutFlowCollection` object. For instance one can get the names of 
the cuts applied in one of the signal regions.
```python
print(sample.SRA.CutNames)
# Output: 
# ['Initial', '$N_{lep} = 0$', '$N_{j} \\geq 6$', '$N_{b} \\geq 4$', 
# '$\\slashed{E}_T > 350$ [GeV]', '$min(\\Delta\\phi(j_{1-4},\\slashed{E}_T))>0.4$ [rad]', 
# '$\\tau^h$ veto', '$p^{b_1}_T > 200$ [GeV]', '$\\Delta R_{max}(b,b)>2.5$', 
# '$\\Delta R_{max-min}(b,b)<2.5$', '$m(h_{cand})>80$ [GeV]', '$m_{eff} > 1$ [TeV]']
```
Or simply print the entire cutflow;
```python
print(sample.SRA)
# Output: 
# * SRA :
#  * Initial :
#   - Number of Entries    : 200000
#   - Number of Events     : 790771.000 ± 0.000(ΔMC)
#   - Cut & Rel Efficiency : 1.000, 1.000
#  * $N_{lep} = 0$ :
#   - Number of Entries    : 156651
#   - Number of Events     : 499908.962 ± 609.064(ΔMC)
#   - Cut & Rel Efficiency : 0.632, 0.632
#  * $N_{j} \geq 6$ :
#   - Number of Entries    : 65546
#   - Number of Events     : 209971.179 ± 362.184(ΔMC)
#   - Cut & Rel Efficiency : 0.266, 0.420
#  * $N_{b} \geq 4$ :
#   - Number of Entries    : 19965
#   - Number of Events     : 63883.202 ± 123.205(ΔMC)
#   - Cut & Rel Efficiency : 0.081, 0.304
#  * $\slashed{E}_T > 350$ [GeV] :
#   - Number of Entries    : 191
#   - Number of Events     : 755.117 ± 1.688(ΔMC)
#   - Cut & Rel Efficiency : 0.001, 0.012
#  * $min(\Delta\phi(j_{1-4},\slashed{E}_T))>0.4$ [rad] :
#   - Number of Entries    : 72
#   - Number of Events     : 284.658 ± 0.636(ΔMC)
#   - Cut & Rel Efficiency : 0.000, 0.377
#  * $\tau^h$ veto :
#   - Number of Entries    : 68
#   - Number of Events     : 268.850 ± 0.601(ΔMC)
#   - Cut & Rel Efficiency : 0.000, 0.944
#  * $p^{b_1}_T > 200$ [GeV] :
#   - Number of Entries    : 33
#   - Number of Events     : 130.474 ± 0.292(ΔMC)
#   - Cut & Rel Efficiency : 0.000, 0.485
#  * $\Delta R_{max}(b,b)>2.5$ :
#   - Number of Entries    : 25
#   - Number of Events     : 98.836 ± 0.221(ΔMC)
#   - Cut & Rel Efficiency : 0.000, 0.758
#  * $\Delta R_{max-min}(b,b)<2.5$ :
#   - Number of Entries    : 25
#   - Number of Events     : 98.836 ± 0.221(ΔMC)
#   - Cut & Rel Efficiency : 0.000, 1.000
#  * $m(h_{cand})>80$ [GeV] :
#   - Number of Entries    : 10
#   - Number of Events     : 39.543 ± 0.088(ΔMC)
#   - Cut & Rel Efficiency : 0.000, 0.400
#  * $m_{eff} > 1$ [TeV] :
#   - Number of Entries    : 10
#   - Number of Events     : 39.543 ± 0.088(ΔMC)
#   - Cut & Rel Efficiency : 0.000, 1.000
```
As can be seen, it shows number of entries (MonteCarlo events), number of events (lumi weighted), 
cut efficiency and relative efficiency. The error in number of events is the MonteCarlo uncertainty.

It is also possible to access practical information 
```python
print(sample.SRA.isAlive)
# Output: True
```
which simply checks the number of entries in the final cut. Hence one can remove the SRs which does
not have any statistics;
```python
alive = sample.get_alive()
print(f"Number of cutflows survived : {len(alive)},\nNames of the cutflows : { ', '.join([x.id for x in alive]) }")
# Output: 
# Number of cutflows survived : 8,
# Names of the cutflows : SRA_M, SRA_L, SRA_H, SRA, SRC, SRB, SRC_24, SRC_22
```
Each cut is accessible through the interface;
```python
fifth = sample.SRA[5]
print(f"Efficiency : {fifth.eff:.3f}, Relative MC efficiency {fifth.mc_rel_eff:.3f}, number of events {fifth.Nevents:.1f}, sum of weights {fifth.sumW:.3f}")
# Output: 
# Efficiency : 0.0004, Relative MC efficiency 0.377, number of events 284.7, sum of weights 0.008
```
One can also construct independent signal regions for sake of comparisson with Ma5 results;
```python
SRA_presel = [319.7,230.5,192.3,87.9,45.1,20.9,19.3,18.2,17.6,15.0,13.7]

ATLAS = ma5.cutflow.Collection() 

ATLAS.addSignalRegion('SRA',   ma5.SRA.CutNames,   SRA_presel+[13.7])
ATLAS.addSignalRegion('SRA_L', ma5.SRA_L.CutNames, SRA_presel+[0.4])
ATLAS.addSignalRegion('SRA_M', ma5.SRA_M.CutNames, SRA_presel+[6.4])
ATLAS.addSignalRegion('SRA_H', ma5.SRA_H.CutNames, SRA_presel+[7.0])
```
where all properties shown above applies to this new object as well.

[back to top](#outline)

### Histogram Collection

* Parse all the histograms available in the `Histos.saf` file into interactable histogram object.

```python
import ma5_expert as ma5

collection = ma5.histogram.Collection(
        "docs/examples/mass1000005_300.0_mass1000022_60.0_mass1000023_250.0_xs_5.689/Output/SAF/defaultset/atlas_susy_2018_31/Histograms/histos.saf",
        xsection = 5.689, lumi = 139.
)

print(collection)
# Collection of 6 histograms from `examples/mass1000005_300.0_mass1000022_60.0_mass1000023_250.0_xs_5.689/Output/SAF/defaultset/atlas_susy_2018_31/Histograms/histos.saf`
#    * SRA_Meff: [ nbin: 11, min: 800.00, max: 3000.00 ]
#    * SRA_Mh: [ nbin: 12, min: 0.00, max: 480.00 ]
#    * SRB_PTj1: [ nbin: 9, min: 50.00, max: 950.00 ]
#    * SRB_MhAvg: [ nbin: 16, min: 50.00, max: 450.00 ]
#    * SRC_MET: [ nbin: 13, min: 200.00, max: 1500.00 ]
#    * SRC_Sig: [ nbin: 19, min: 17.00, max: 36.00 ]
```

Extract the plotting information:
```python
xbins, bins, weights = collection.lumi_histogram("SRA_Mh")
plt.hist(xbins, bins=bins, weights=weights)
plt.xlabel("$M_{h}\ {\\rm [GeV]}$")
plt.ylabel("${\\rm Number\ of\ events}$")
plt.xlim([min(bins), max(bins)])
plt.show()
```
<p align="center">
<img src="docs/examples/SRA_Mh.png" alt="SRA_Mh" style="width:400px;"/>
</p>

[back to top](#outline)

### Integration to Public Analysis Database through MadAnalysis 5

`ma5-expert` is capable of running MadAnalysis sub-modules through a backend manager. Desired MadAnalysis 
backend can be set via
```python
import ma5_expert as ma5
ma5.BackendManager.set_madanalysis_backend("/PATH/TO/MADANALYSIS5")
```
This will initiate the MadAnalysis backend to be used. Then one can use the reinterpretation tools such as 
exclusion limit computation, externally. One can initiate PAD interface via
```python
interface = ma5.pad.PADInterface(
    sample_path="ma5_expert/docs/examples/mass1000005_300.0_mass1000022_60.0_mass1000023_250.0_xs_5.689",
    dataset_name="defaultset"
)
```
where `sample_path` is the main location of the analysis which has been held, and `dataset_name` is the name
of the dataset which corresponds to the particular folder name under `sample_path + /Outputs/SAF/`. Then results
can be computed via
```python
results = interface.compute_exclusion("atlas_susy_2018_31", 5.689, ma5.backend.PADType.PADForSFS)
```
Note that the given example only computes for `atlas_susy_2018_31` and this analysis has been held under `PADForSFS`
which is indicated via `PADType`. This simply tells function where to look to find corresponding info file, which 
assumes that `PADForSFS` has been installed. The value `5.689` sets the cross section in pb. 

[back to top](#outline)

### Citation 
Developed for [arXiv:2006.09387](http://arxiv.org/abs/2006.09387)

```bibtex
@article{Araz:2020lnp,
    author = "Araz, Jack Y. and Fuks, Benjamin and Polykratis, Georgios",
    title = "{Simplified fast detector simulation in MADANALYSIS 5}",
    eprint = "2006.09387",
    archivePrefix = "arXiv",
    primaryClass = "hep-ph",
    doi = "10.1140/epjc/s10052-021-09052-5",
    journal = "Eur. Phys. J. C",
    volume = "81",
    number = "4",
    pages = "329",
    year = "2021"
}
```

[back to top](#outline)
## TODO

- [ ] Overall Ma5 Analysis parser

- [ ] Add theoretical uncertainties
