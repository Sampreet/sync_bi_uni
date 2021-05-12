# Quantum Synchronzation Transition in Optically Coupled Optomechanical Oscillators

Author | Affiliation
------------ | -------------
[Subhadeep Chakraborty](https://scholar.google.co.in/citations?user=o5n-rDUAAAAJ&hl=en) | ICFAI University Tripura, Tripura-799210, India
[Sampreet Kalita](https://www.iitg.ac.in/stud/sampreet/) | Indian Institute of Technology Guwahati, Guwahati-781039, India
[Amarendra Kumar Sarma](https://www.iitg.ac.in/aksarma/) | Indian Institute of Technology Guwahati, Guwahati-781039, India

## About the Work

We investigate the phenomenon of quantum synchronization of mechanical oscillators in two optomechanical cavities coupled optically through two configurations.

* ***Bidirectional configuration:*** The cavities exchange photons in a reversible manner and synchronization traces the classic Arnold tongue.
* ***Unidirectional configuration:*** The cavities are arranged in a forward-fed manner and synchronization exhibits a novel blockade-like phenomenon associated with in-phase and anti-phase transitions.

We further investigate the stability of the collective modes of the two mechanical oscillators to understand the synchronization phase transitions.

## Structure of the Repository
```
ROOT_DIR/
|
├───notebooks/
│   ├───foo_bar.ipynb
│   └───...
|
│───scripts/
│   ├───foo_bar.py
│   └───...
|
├───systems/
│   ├───__init__.py
│   ├───FooBar.py
│   └───...
|
│───utils/
│   ├───__init__.py
│   ├───foo_bar.py
│   └───...
│
├───.gitignore
├───GUI.py
└───README.md
```

## Running the Scripts

To run the scripts, navigate *inside* the top-level directory, `ROOT_DIR`, and execute:

```bash
python scripts/foo_bar.py
```

Here, `foo_bar.py` is the name of the script.

To run in GUI mode, from `ROOT_DIR`, execute:

```bash
python -c 'from qom.ui import run; run()'
```

Alternatively, run `GUI.py`.

