
# MoMITPy: Python implementation of MoMIT a multiobjective Miniaturization approach for IoT 

MoMITPy is a tool that allows you to miniaturize (reduce the memory and size footprint) of a JavaScript interpreter to fit on highly constrained IoT devices.  It relies on [Duktape JS embedded engine]().  

To perform the miniaturization of a JS interpreter, MoMITPy uses the mandatory code features of JS file that you want to execute, and the list of IoT'devices hardware requirements to select the best combination of code features to execute your JS file without modifying the source code.  Since, MoMITPy is multiobjective, it generates more than one solution, targeting the ones that can be deployed in more devices from the IoT devices list you provide.

MoMITPy relios on [JMetalPy](https://github.com/jMetal/jMetalPy.git) metaheuristic framework.

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)
- [License](#license)

## Installation
To download jMetalPy just clone the Git repository hosted in GitHub:
```bash
$ git clone https://github.com/jMetal/jMetalPy.git
$ sudo python3 setup.py install
```
The scripts for running MoMITPy are located on the /iot subfolder

## Usage
TODO

## Features
The current release of MoMITPy  contains the following components:

* Algorithms: random search, NSGA-II, SWAY, and Hybrid random search.
* Benchmark problems: [Sunspider](https://webkit.org/perf/sunspider/sunspider.html) JS benchmark 
* Quality indicators: hypervolume.
* Density estimator: crowding distance.

## Research
MoMITPy is the product of research at Concordia University in Montreal Canada in the Ptidej Lab.
If you want to use out tool, please cite the following paper:

[RePOR: Mimicking humans on refactoring tasks. Are we there yet?](https://arxiv.org/abs/1808.04352)

For a complete list of works please visit my [personal web site](https://moar82.github.io/#portfolio)


### Replication package
There is a replication package of the experiments associated with the research paper where MoMIT approach was introduced:
[Replication package website](https://moar82.github.io/momit_data/)

## License
This project is licensed under the terms of the MIT - see the [LICENSE](LICENSE) file for details.
* This software is made available AS IS, and THE AUTHOR DISCLAIMS
 * ALL WARRANTIES, EXPRESS OR IMPLIED, INCLUDING WITHOUT LIMITATION THE
 * IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
 * PURPOSE, AND NOT WITHSTANDING ANY OTHER PROVISION CONTAINED HEREIN, ANY
 * LIABILITY FOR DAMAGES RESULTING FROM THE SOFTWARE OR ITS USE IS
 * EXPRESSLY DISCLAIMED, WHETHER ARISING IN CONTRACT, TORT (INCLUDING
 * NEGLIGENCE) OR STRICT LIABILITY, EVEN IF Rodrigo Morales Alvarado IS ADVISED
 * OF THE POSSIBILITY OF SUCH DAMAGES.
