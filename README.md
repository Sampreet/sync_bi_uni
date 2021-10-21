# Switching of Quantum Synchronization in Coupled Optomechanical Oscillators

Author | Affiliation
------------ | -------------
[Sampreet Kalita](https://www.iitg.ac.in/stud/sampreet/) | Indian Institute of Technology Guwahati, Guwahati-781039, India
[Subhadeep Chakraborty](https://scholar.google.co.in/citations?user=o5n-rDUAAAAJ&hl=en) | ICFAI University Tripura, Tripura-799210, India
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
├───CHANGELOG.md
├───GUI.py
└───README.md
```

## Execution

### Installing Dependencies

The project requires `Python 3.8+` installed via the [Anaconda distribution](https://www.anaconda.com/products/individual). 
An extensive guide to set up your python environment same can be found [here](https://sampreet.github.io/python-for-physicists/modules/m01-getting-started/m01t01-setting-up-python.html).

Once the installation is complete and `conda` is configured, it is preferable to create a new conda environment (say `qom`) and activate it using:

```bash
conda create -n qom python=3
conda activate qom
```

This project uses [The Quantum Optomechanics Toolbox](https://github.com/Sampreet/qom) which can be installed from the Python Package Index via `pip` using:

```bash
pip install -i https://test.pypi.org/simple/ qom
```

Alternatively, [clone](https://github.com/Sampreet/qom) or [download](https://github.com/Sampreet/qom/archive/refs/heads/master.zip) as `.zip` and extract the contents.
Now, execute the following from *outside* the top-level directory, `ROOT_DIR`, inside which `setup.py` is located:

```bash
pip install -e ROOT_DIR
```

### Running the Scripts

To run the scripts, navigate *inside* the top-level directory, `ROOT_DIR`, and execute:

```bash
python scripts/foo_bar.py
```

Here, `foo_bar.py` is the name of the script.

To run in GUI mode using `PowerShell` or `bash`, navigate to `ROOT_DIR` and execute:

```bash
python -c 'from qom.ui.gui import run; run()'
```

Alternatively, run `GUI.py` from within the directory.