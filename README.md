# MadAnalysis 5 Interpreter For Expert Mode
 MA5 analysis output interpreter for expert mode. Parse the signal collection and construct cutflow (histogram interpreter coming soon). 

## Cutflow Collection

 * Parse all the signal regions and construct an object-base, interactable cutflow.
 * Write combined LaTeX tables for different samples.
 * Compare samples and construct validation tables which allows you to calculate difference of the relative efficiencies for each given sample with respect to a reference sample.
 * Compare signal and background samples and calculate figure of merit.
 * Posibility to include experimentaly available cutflow data and compare it against MadAnalysis 5 cutflow output.

Examples can be found in [examples folder](https://github.com/jackaraz/ma5_expert/tree/master/examples).

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

- [ ] Combine collections with + operator and normalize to a certain luminosity with * operator.
