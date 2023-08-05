# pyPhases

A toolobx for configuration based data generation.

The main concepts are:
- Phases: A phase is a python based process that can generate data that depends on configuration values. Phases can also access data from different phases using `self.getData("myDataId", MyDataType)`.
- Config: A config is saved in a `dict`-like manner and is connected to the project. The configuration can be loaded from phases with `getConfig("myConfigField")`.
- Exporter: An exporter can save data persitently to a storage. A Storage has specific python types it can handle. You can populate your data to a exporter using `self.registerData("myDataId", myData)` if any exporter can handle the data type.
- Project: A project is the composition of all the concepts its stores the config values, knows about the phases and can execute phases. For a automatic config based composition, the connected tool [phases](https://pypi.org/project/phases/) can be used.

![arch](assets/achitektur.svg)


## Install

Python `>= 3.6` is required.

`pip install phases pyPhases`

## Hello World Example

The project is using two phases, one to generate the sentence to be said and the other one to actually say it.

First we need a data directory where where the data will be stored (default `data`): `mkdir data`

### `poject.yaml`

 ```yaml
name: example
namespace: myNamespace

exporter:
    # exporter that can handle primitive types
  - PickleExporter

phases:
    - name: GenerateIt
      exports:
        - sentence
    - name: SayIt

data:
  - name: world
    dependsOn:
      - who

config:
  who: whole world
 ````

### `example/phases/GenerateIt.py`

```python
from pyPhases import Phase

class GenerateIt(Phase):
    """This phase generates the sentence to be said."""
    def main(self):
        self.log("Generating the sentence")
        greetWho = self.getConfig("who")
        self.registerData("sentence", "Hello %s!" % greetWho)

```

### `example/phases/SayIt.py`

 ```python
from pyPhases import Phase

class SayIt(Phase):
    """This phase says the sentence."""
    def main(self):
        sentence = self.getData("sentence")
        self.logSuccess(sentence)

```

Run the Example: `python -m phases run SayIt`

First Output will generate the sentence in phase `GenerateIt`:
```console
[phases] Phases 1.0.0 with pyPhases 1.0.3 (Log level: LogLevel.INFO)
[Project] Data sentence--current was not found, try to find phase to generate it
[GenerateIt] RUN phase GenerateIt
[GenerateIt] Generating the sentence
[SayIt] Hello world!
```
The data is now stored in the file: `data/sentence--current`

If your run it again (`python -m phases run SayIt`) the data is loaded using the Pickleexporter:

```console
[phases] Phases 1.0.0 with pyPhases 1.0.3 (Log level: LogLevel.INFO)
[SayIt] RUN phase SayIt
[Project] Data sentence--current was not found, try to find phase to generate it
[GenerateIt] RUN phase GenerateIt
[GenerateIt] Generating the sentence
[SayIt] Hello world!
```

If you change the config value `who` in the project to `whole world`. The data is generated again:

```console
[phases] Phases 1.0.0 with pyPhases 1.0.3 (Log level: LogLevel.INFO)
[SayIt] RUN phase SayIt
[Project] Data sentence--current was not found, try to find phase to generate it
[GenerateIt] RUN phase GenerateIt
[GenerateIt] Generating the sentence
```

if you want to explicit generate the data you can just run the first phase: `python -m phases run GenerateIt`

## Example projects

- https://gitlab.com/tud.ibmt.public/pyphases/pyphasesml-example-bumpdetector
- https://gitlab.com/tud.ibmt.public/pyphases/arousaldetector


## Development

## build

`python setup.py sdist bdist_wheel`

## publish

`twine upload dist/*`

## documentation

`sphinx-apidoc -o docs/source pyPhases`
`sphinx-build -b html docs/source docs/build`


# test
`python -m unittest discover -v`
