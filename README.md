# Spy4CastManual

Spy4Cast is an open-source python implementation of a 
maximum convariance analysis (MCA) statistical model.

In this manual we explain the steps to take to install 
and run for the first time this model.

Full documentation is available at https://spy4cast-docs.netlify.app

Link to GitHub repository with the latest code: https://github.com/pabloduran016/Spy4CastManual

## Installation

You have to have installed git (Install Git https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)

You have to have installed anaconda (Install Anaconda https://docs.anaconda.com/anaconda/install/index.html)

```bash
    $ conda create -n <your-env-name> python=3.9
    $ conda activate <your-env-name>
    (<your-env-name>) $ conda install pip
    (<your-env-name>) $ conda install cartopy
    (<your-env-name>) $ pip install git+https://github.com/pabloduran016/Spy4Cast
```

Cartopy has to be installed with conda because pip version does not work

## Usage

For usage example look at file [EquatorialAtlantic_Impact_Nino.py](EquatorialAtlantic_Impact_Nino.py) in this repository.

## How to cite this material

DOI: https://10.5281/zenodo.8162066

BibTex:
```
@software{Spy4CastManual,
  doi = {10.5281/ZENODO.13619197},
  url = {https://zenodo.org/doi/10.5281/zenodo.13619197},
  author = {Duran-Fonseca,  Pablo and Rodriguez-Fonseca,  Belen},
  keywords = {python,  open-source,  statistical-model,  physics,  spy4cast},
  title = {Spy4CastManual},
  publisher = {Zenodo},
  year = {2024},
  copyright = {Creative Commons Attribution 4.0 International}
}
```
