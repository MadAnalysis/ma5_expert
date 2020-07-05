# MadAnalysis 5 Interpreter For Expert Mode
 MA5 analysis output interpreter for expert mode. Parse the signal collection and construct cutflow (histogram interpreter coming soon). 

# How to get LaTeX output of the cutflow:

```CutFlowReader``` Collects the signal regions under the main CutFlow path and constructs a collection of signal regions. Sample information folder can be inputted to parse cross section value, or it can be overwritten entirely. ```CutFlowTable``` generates two types of cutflow table;
  * Signal vs Background comparison table: The reference sample will be treated as background, and several different statistical variables are calculated with respect to the background. Other samples will be treated as individual signal samples.
  * Sample comparison table: Each sample is compared to the reference sample with respect to their relative cut efficiencies.

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
