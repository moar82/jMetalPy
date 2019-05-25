
# MoMITPy: Python implementation of MoMIT a multiobjective Miniaturization approach for IoT 

MoMITPy is a tool that allows you to miniaturize (reduce the memory and size footprint) of a JavaScript interpreter to fit on highly constrained IoT devices.  It relies on [Duktape JS engine](https://duktape.org/).  

To perform the miniaturization of a JS interpreter, MoMITPy uses the mandatory code features of JS file that you want to execute, and the list of IoT'devices hardware requirements to select the best combination of code features to execute your JS file without modifying the source code.  Since, MoMITPy is multiobjective, it generates more than one solution, targeting the ones that can be deployed in more devices from the IoT devices list you provide.

MoMITPy relios on [JMetalPy](https://github.com/jMetal/jMetalPy.git) metaheuristic framework.

## Table of Contents
- [Installation](#installation)
- [Input Files](#input Files)
- [Usage](#usage)
- [Output Files](#output Files)
- [Features](#features)
- [Research](#research)
- [Replication package](#replication)
- [License](#license)

## Installation
To download jMetalPy just clone the Git repository hosted in GitHub:
```bash
$ git clone https://github.com/jMetal/jMetalPy.git
$ sudo python3 setup.py install
```
To install Duktape refer to the existing documentation at: [https://duktape.org/guide.html](https://duktape.org/guide.html)

Note that you will need to provide the **path to the installation of duktape later.**

The scripts for running MoMITPy are located on the /iot subfolder
Suppose that you have a javascript file called date-format-tofte.js (located on the iot subfolder), 
and want to execute one run using hybrid random search metaheuristic.

## Input Files

* A javascript file that we want to execute on constrained IoT device.
In this example we use benchmark_date-fromat-tofte.js from [Sunspider testbed](https://webkit.org/perf/sunspider/sunspider.html)

* A CSV file containing the median results measurements of executing the desired javascript program using duktape default measurements.  This is generated using python scripts explained on the [wiki](https://github.com/moar82/jMetalPy/wiki).  For our example, this is the file: 
 median_results_original_default_date-format-tofte.csv
 
* Config.ini.  This file provides the basic configuration parameters of our framework, including the path to the Duktape installation, the file with the test features, name of the harness file, jsfunction to execute (if any), etc.  More information on the [wiki](https://github.com/moar82/jMetalPy/wiki).

* confOpt.csv file.  This file contains the Duktape code features that we want to combine.
These are the columns required for this file.
  * **id**: is a sequential number
  * **property**: is the name according to duktape
  * **default**: the default value of duktape for this property.
  * **activated in**: from which profile we take this configuration 
  * **value in**: the value that we want to experiment with
  * **category**: the category assigned by duktape.
  * **zero-index-base_id**: id -1

* A CSV containing the mandatory features of the javascript file to execute.  for our example, the name is testbed_required_features.csv, which contains the following columns:
  *  **Script**: the name of the javascript(s) to execute
  *  **RequiredFeaturesWithDefaulValue**: the mandatory features
  *  **RequiredFeaturesWithDefaulValueOriginal**: this field is not longer used.
  
* A file with the hardware characteristics of the IoT constrained devices where you want to deploy your js interpreter.  it contains the following columns:
  * device_id
  * device_name:
  * memory_capacity:
  * storage_capacity:
  * wifi_integrated: this field is not used by our approach
  * price: this field is not used by our approach
  * val: preference assigned from the user typically 1 to n.  The higher the value, the most that you want to use it to deploy your javascript file on this device.

## Usage
```bash
$ python3 rs_full_settings.py 1 date-fromat-tofte.js
```
This will generate several files which we are going to explain below.

## Output files

**benchmark_date-fromat-tofte_RS**

This is just a log file in case of errors or execeptions

**/configFiles/optimize**

In this directory we store all the configurations that fail ( for example: optimize.yaml.1540604693.6324103.execution_error)
and overwrite the file that succed in each test (optimize.yaml).
Note that in benchmark_date-fromat-tofte_RS we link the error with the corresponding   optimize.yaml.<identier number>.execution_error.  This is helps for debugging purposes
  
**/iot/duktape-src**

In this folder we stored the files required to benchmark a set of Duktape code features.  It includes the headers of duktape (duk_confgi.h, duktape.h, and duktape.c); our embedded duktape javascript compiler (harness.c), the javascript file to execute (for example, date-fromat-tofte.js).


**FUN.RS.date-fromat-tofte.js.1.Miniaturization** 

This file contains the normalized values obtained for the measurements of file size, memory usage, execution time and DSR metric. The normalization of the values is explained on the paper.

**HV.RS.date-fromat-tofte.js.1.Miniaturization** 

This file is the Hypervolume achieved for this run.  Note that this is not the correct computation, as it assumes that the reference point is (1,1,1,1), as this is a miniaturization problem, but we do not know which is the maximum value that a set of features can achieved beforehand.  Thus, this value has to be computed based on the Nadir point after executing the experiments.

**TIME.RS.date-fromat-tofte.js.1**

Computing times in seconds of the miniaturization process


**VAR.RS.date-fromat-tofte.js.1.Miniaturization** 

This file contains the list of solutions generated by the metaheuristic (that means the list of configurations that matches the mandatory features provided in file xx) separeted by "[]".  You can convert this file to the actual yaml file (the one that compiles a duktape interpreter based on selected features) using var_2_yaml.py script.  More details on the [wiki](https://github.com/moar82/jMetalPy/wiki).

**values_achieved_RS_date-fromat-tofte.js1**

This file contains the real values obtained after miniaturizing the duktape interpreter in the following order:
file size kb, memory usage (kb), execution time (seconds), and DSR metric (more details on the [wiki](https://github.com/moar82/jMetalPy/wiki))


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
