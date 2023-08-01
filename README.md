# PT to AT
## Attack Tree Generation via Process Mining: From Process Trees to Attack Trees

This work provides a method for the semi-automatic generation of Attack Trees using process mining. The main concept is applying Process Mining to attack logs and deriving a Process Tree from them. Then we define rules for translating a Process Tree to an Attack Tree.
## Features

- Derive a Process Tree directly from an event log which describes the behavior of an attacker
- Translate the Process Tree into an Attack Tree, in the RisQFLan format
## Implementation

PTtoAT is implemented as a [Python](https://www.python.org/) application.
The main script Translator.py is composed by the following steps:
- Import the log file and derive a Process Tree using the Inductive Miner
- Translate the Process Tree into an Attack Tree
- Convert the AttackTree into RISQFlan code

## Usage/Example

The implemented script directly derives an Attack Tree from the input log (in xes format). The following is the format of the execution, where:
- LogFile is the filename of the xes file (withouth extension)
- OutputFile is the filename of the output Attack Tree (withouth extension) 
```python
python Translator.py LogFile OutputFile
```
A sample xes file is provided, which can be used to run the script using the following command:
```python
python Translator.py Example ATree
```
