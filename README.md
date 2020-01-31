# MA5lib
 MA5 analysis output reader for expert mode. Parse the signal collection and construct cutflow.

* CutFlowReader:

Collects the signal regions under the main CutFlow path and constructs a collection of signal regions.

```python
from MA5lib.CutFlowReader import Collection
SRcollection = Collection(collection_path='CutFlow',saf_file='_dataset.saf', lumi=139.0)
```

## TODO

* Clean cutflow reader needs optimization and clarity

* Generalize table writer and add latex writer

* Histogram reader