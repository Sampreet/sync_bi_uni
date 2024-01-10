# Switching of Quantum Synchronization in Coupled Optomechanical Oscillators

[![Manuscript Version](https://img.shields.io/badge/manuscript-v3.0-red?style=for-the-badge)](https://doi.org/10.1088/2399-6528/ac3204)
[![Toolbox Version](https://img.shields.io/badge/qom-v1.0.1-red?style=for-the-badge)](https://sampreet.github.io/qom-docs/v1.0.1)
[![Last Updated](https://img.shields.io/github/last-commit/sampreet/sync_bi_uni?style=for-the-badge)](https://github.com/sampreet/sync_bi_uni/blob/master/CHANGELOG.md)

> J. Phys. Commun 5, 115006 (2021)

Author | Affiliation
------------ | -------------
[Sampreet Kalita](https://www.iitg.ac.in/stud/sampreet/) | Indian Institute of Technology Guwahati, Guwahati-781039, India
[Subhadeep Chakraborty](https://scholar.google.co.in/citations?user=o5n-rDUAAAAJ&hl=en) | Indian Institute of Science Education and Research Kolkata, Nadia-741246, India
[Amarendra Kumar Sarma](https://www.iitg.ac.in/aksarma/) | Indian Institute of Technology Guwahati, Guwahati-781039, India

Contributing Part | SK | SC
------------ | ------------ | -------------
Literature review | 40% | 60%
Idea and formulation | 20% | 80%
Derivations of expressions | 70% | 30%
Parameter sweeping | 40% | 60%
Illustrations and plots | 80% | 20%
Results and discussion | 60% | 40%
Manuscript preparation | 40% | 60%

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
* [Plots in the Latest Version of the Manuscript](notebooks/v3.0_qom-v1.0.1/plots.ipynb)

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

## Installing Dependencies

All numerical data and plots are obtained using the [Quantum Optomechanics Toolbox](https://github.com/sampreet/qom), an open-source Python framework to simulate optomechanical systems.
Refer to the [QOM toolbox documentation](https://sampreet.github.io/qom-docs/v1.0.1) for the steps to install this libary.

## Running the Scripts

To run the scripts, navigate *inside* the top-level directory, and execute:

```bash
python scripts/bar/baz.py
```

Here, `bar` is the name of the folder (containing the version information) inside `scripts` and `baz.py` is the name of the script (refer to the repository structure).