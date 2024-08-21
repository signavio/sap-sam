[![REUSE status](https://api.reuse.software/badge/github.com/signavio/sap-sam)](https://api.reuse.software/info/github.com/signavio/sap-sam)

# SAP Signavio Academic Models (SAP-SAM)

This repository contains the source code for the paper `SAP Signavio Academic Models: A Large Process Model Dataset` by Diana Sola, Christian Warmuth, Bernhard Schäfer, Peyman Badakhshan, Jana-Rebecca Rehse, and Timotheus Kampik.

Link to the paper: https://arxiv.org/abs/2208.12223 (pre-print)

Link to the dataset: https://zenodo.org/record/7012043 

## License

The example code in this repository is licensed as follows. **Note that a different license applies to the dataset itself!**

```
Copyright (c) 2022 by SAP.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
```

The following license applies to the SAP-SAM dataset.

```
Copyright (c) 2022 by SAP.

SAP grants to Recipient a non-exclusive copyright license to the Model Collection to use the Model Collection for Non-Commercial Research purposes of evaluating Recipient’s algorithms or other academic research artefacts against the Model Collection. Any rights not explicitly granted herein are reserved to SAP. For the avoidance of doubt, no rights to make derivative works of the Model Collection is granted and the license granted hereunder is for Non-Commercial Research purposes only.

"Model Collection" shall mean all files in the archive (which are JSON, XML, or other representation of business process models or other models).

"Recipient" means any natural person receiving the Model Collection.

"Non-Commercial Research" means research solely for the advancement of knowledge whether by a university or other learning institution and does not include any commercial or other sales objectives.
```

## Citing SAP-SAM

```BibTeX
@misc{SAP-SAM-paper,
  doi = {10.48550/ARXIV.2208.12223},
  url = {https://arxiv.org/abs/2208.12223},
  author = {Sola, Diana and Warmuth, Christian and Schäfer, Bernhard and Badakhshan, Peyman and Rehse, Jana-Rebecca and Kampik, Timotheus},
  keywords = {Other Computer Science (cs.OH), Software Engineering (cs.SE), FOS: Computer and information sciences, FOS: Computer and information sciences},
  title = {SAP Signavio Academic Models: A Large Process Model Dataset},
  publisher = {arXiv},
  year = {2022},
  copyright = {arXiv.org perpetual, non-exclusive license}
}
```
or 
```BibTeX
@dataset{SAP-SAM-dataset,
  author       = {Kampik, Timotheus and Warmuth, Christian and Sola, Diana and Schäfer, Bernhard and Axworthy, Liz and Ivarsson, Erica and
                  Ouda, Karim and Eickhoff, David},
  title        = {SAP Signavio Academic Models},
  month        = aug,
  year         = 2022,
  publisher    = {Zenodo},
  version      = {0.5.1},
  doi          = {10.5281/zenodo.6964944},
  url          = {https://doi.org/10.5281/zenodo.6964944}
}
```
## Setup

You need to download the [dataset](https://zenodo.org/record/7012043#.Y9jQV3bMKPo) and place it into the folder `./data/raw` such that the models are in `./data/raw/sap_sam_2022/models`.

> It is also possible to run the analysis on any `.sgx` files (Signavio workspace exports). Place the files in `./data/raw/sap_sam_2022/models` and the conversion will be performed automatically.

To get started on Mac or Windows, we provide a dependency setup with `poetry`.
Make sure poetry is installed on your system with `poetry --version`. If not, run `pip poetry install`.

To install the dependencies,  do  to the root of the cloned repository, type this line in the terminal, and press enter:
```shell
poetry install
```

> It is important to note that you should have the latest stable version of `python` or `python3` installed on your machine, and not a pre-release one (try `python --version`). The current latest stable version is `3.12.5` (as of August 2024).

After executing the script, you should be able to setup the kernel:
```shell
poetry run python -m ipykernel install --user --name=sap-sam-kernel
```
Then, to open the project, simply type:
```shell
poetry run jupyter notebook
```

Alternatively, a **conda** setup is possible.

We provide two [conda](https://docs.conda.io/projects/conda/en/latest/user-guide/index.html) environment.yml files that can be used to create a new environment and install the required dependencies:
- `environment.yml`: contains the abstract dependencies (pandas, numpy, ...).
- `environment-lock.yml`: contains versions for all dependencies and the transitive dependencies to ensure reproducible results.

You can use the following conda command to create the environment:
```shell
conda env create -f environment.yml  
```
or
```shell
conda env create -f environment-lock.yml  
```

## Getting started

We provide a [tutorial Jupyter Notebook](https://github.com/signavio/sap-sam/blob/main/notebooks/1_tutorial.ipynb) that illustrates the dataset format in more detail and shows how to use the csv parsers developed in `./src`.

The [properties Jupyter Notebook](https://github.com/signavio/sap-sam/blob/main/notebooks/2_properties.ipynb) gives an overview of selected properties of the dataset.

## Dataset Format

The SAP-SAM dataset contains 103 csv files with a rough size of 38 GB of process models (see modeling notations of the models below).

### CSV Format

1. csv columns: 
    - Revision ID: Unique identifier for model revision
    - Model ID: Unique identifier for model
    - Organization ID: Unique identifier for organization this model originates from
    - Datetime: Date and time of creation
    - Model JSON: JSON containing model information
    - Description: Description of model (typically empty)
    - Name: Model name
    - Type: Model type (duplicate and less specific than namespace)
    - Namespace: Stencilset/modeling notation (e.g. BPMN, DMN, UML,...)
2. Number of models: 1,021,471
3. Number of models by modeling notation:

| Modeling notation     | Frequency |
|------                 |------     |
| BPMN 2.0              | 618,807   |
| Value Chain           | 194,078   |
| DMN 1.0               | 98,286    |
| EPC                   | 32,369    |
| BPMN 1.0              | 15,643    |
| UML 2.2 Class         | 14,953    |
| Petri Net             | 11,207    |
| ArchiMate 2.1         | 10,956    |
| UML Use Case          | 10,228    |
| Organigram            | 4,568     |
| BPMN 2.0 Choreography | 4,096     |
| BPMN 2.0 Conversation | 2,788     |
| FMC Block Diagram     | 1,398     |
| CMMN 1.0              | 999       |
| CPN                   | 385       |
| Journey Map           | 287       |
| YAWL 2.2              | 238       |
| Process Documentation Template | 86 |
| jBPM 4                | 76       |
| XForms                | 20       |
| Chen Notation         | 3        |

## Dummy Data

In order to remove personal first and last names, emails or in some cases matriculations numbers (which users have added in non-compliance with the T&Cs), we have applied a simple replacement script. In particular, we have replaced - to the extent possible - emails, names, and (matriculation) numbers with the following dummy values:

| Context                   | Dummy             |
|------                     |--------           |
|Email Dummy               | jane.doe@dummy.com|
|Name Dummy                | Jane Doe          |
|Matriculation/Number Dummy| 12345678          |


## Project Organization

    ├── data
    │   ├── interim           <- Intermediate data that has been transformed.
    │   └── raw               <- The raw dataset should be placed in this folder.
    ├── notebooks             <- Jupyter notebooks.
    ├── reports            
    │   └── figures           <- Generated graphics and figures used in the paper.
    ├── src               
    │   └── sapsam            <- Source code and dictionaries for use in this project.
    ├── LICENSE               <- License that applies to the example code in this repository.
    ├── README.md             <- The top-level README for developers using this project.
    ├── environment-lock.yml  <- Contains versions for all dependencies and the transitive dependencies to ensure reproducible results.
    ├── environment.yml       <- Contains the abstract dependencies (pandas, numpy, ...).
    └── setup.py              <- Makes project pip installable (pip install -e .) such that src can be imported.
    
    
    
