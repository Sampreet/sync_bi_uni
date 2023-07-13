# Switching of Quantum Synchronization in Coupled Optomechanical Oscillators

[![Manuscript Version](https://img.shields.io/badge/version-3.0-red?style=for-the-badge)](https://doi.org/10.1088/2399-6528/ac3204)
[![Toolbox Version](https://img.shields.io/badge/qom-v1.0.0-red?style=for-the-badge)](https://sampreet.github.io/qom-docs)

> A collection of all data and scripts for the work.

Author | Affiliation
------------ | -------------
[Sampreet Kalita](https://www.iitg.ac.in/stud/sampreet/) | Indian Institute of Technology Guwahati, Guwahati-781039, India
[Subhadeep Chakraborty](https://scholar.google.co.in/citations?user=o5n-rDUAAAAJ&hl=en) | Indian Institute of Science Education and Research Kolkata, Nadia-741246, India
[Amarendra Kumar Sarma](https://www.iitg.ac.in/aksarma/) | Indian Institute of Technology Guwahati, Guwahati-781039, India

## About the Work

We explore the phenomenon of quantum phase synchronization in two optomechanical oscillators, coupled either bidirectionally or unidirectionally to each other.
We first show that irrespective of the configuration of the optomechanical oscillators, synchronization can be achieved, with a finite degree of quantum correlation.
However, while looking at the variation of the synchronization against the frequency detuning of the two oscillators, we observe a profound effect of the directionality of the optical coupling.
For instance, we find that when the two optomechanical cavities exchange photons bidirectionally, synchronization traces the classic Arnold tongue.
Whereas, for the unidirectional configuration, synchronization exhibits a novel blockade-like behavior where finite detuning favors synchronization.
We also observe a strong connection between synchronization blockade and
synchronization phase transition.

## Notebooks

* [Adiabatic Elimination in the Bidirectional Configuration](notebooks/bidirectional_adiabatic_elimination.ipynb)
* [Adiabatic Elimination in the Unidirectional Configuration](notebooks/unidirectional_adiabatic_elimination.ipynb)
* [Plots in the Manuscript](notebooks/v3.0_qom-v1.0.0/plots.ipynb)

## Structure of the Repository

```
ROOT_DIR/
|
├───data/
│   ├───bar/
│   │   ├───baz_xyz.npz
│   │   └───...
│   └───...
|
├───notebooks/
│   ├───bar/
│   │   ├───baz.ipynb
│   │   └───...
│   │
│   ├───foo_baz.ipynb
│   └───...
|
│───scripts/
│   ├───bar/
│   │   ├───baz.py
│   │   └───...
│   └───...
|
├───systems/
│   ├───__init__.py
│   ├───Foo.py
│   └───...
│
├───.gitignore
├───CHANGELOG.md
└───README.md
```

Here, `foo` represents the module or system and `bar` represents the version.

## Execution

### Installing Dependencies

[The Quantum Optomechanics Toolbox](https://github.com/Sampreet/qom) requires `Python 3.8+` installed, preferably via the [Anaconda distribution](https://www.anaconda.com/download).
Once `Anaconda` is set up, create and activate a new `conda` environment using:

```bash
conda create -n qom python
conda activate qom
```

The toolbox relies primarily on `numpy` (for fast numerical algebra), `scipy` (for numerical methods), `sympy` (for symbolic algebra), `seaborn` (for color palettes) and `matplotlib` (for plotting results).
These libraries can be installed using:

```bash
conda install matplotlib numpy scipy sympy seaborn
```

***Note: To run the GUI modules, `pyqt` should be installed separately.***

Once the dependencies are installed, download the [repository of the toolbox](https://github.com/Sampreet/qom) as `.zip` and extract the contents.
Now, execute the following from *outside* the top-level directory, `ROOT_DIR`, inside which `setup.py` is located (refer to the file structure of the repository [here](https://github.com/sampreet/qom/blob/master/CONTRIBUTING.md)):

```bash
pip install -e ROOT_DIR
```

The corresponding documentation is available [here](https://sampreet.github.io/qom-docs).

### Running the Scripts

To run the scripts, navigate *inside* the top-level directory, `ROOT_DIR`, and execute:

```bash
python scripts/bar/baz.py
```

Here, `bar` is the name of the folder inside `scripts` and `baz.py` is the name of the script (refer to the repository structure).