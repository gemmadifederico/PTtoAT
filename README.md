# PT to AT
## Attack Tree Generation via Process Mining: From Process Trees to Attack Trees

This work provides a method for the semi-automatic generation of Attack Trees using process mining. The main concept is applying Process Mining to attack logs and deriving a Process Tree from them. Then we define rules for translating a Process Tree to an Attack Tree.
## Features

- Derive a Process Tree directly from an event log which describes the behavior of an attacker
- Translate the Process Tree into an Attack Tree, in the RisQFLan format
## Implementation

PTtoAT is implemented as a [Python](https://www.python.org/) application.
The main script PTtoAT.py is composed by the following steps:
- Import the log file and derive a Process Tree using the Inductive Miner, or import directly a Process Tree file
- Translate the Process Tree into an Attack Tree
- Convert the AttackTree into RISQFlan code

## Usage/Example

The implemented script can derive an Attack Tree directly from the input event log (in xes format), or translate a Process Tree into an Attack Tree. The following is the format of the execution, where:
- filename is the filename of the log file (withouth extension, in xes format), or the filename of the Process Tree file (withouth extension, in xml format)
- code [1,2], where 1 indicates the translation from an event log, 2 indicates the translation from a Process Tree
```python
python PTtoAT.py filename code
```
A sample log (.xes) file is provided, which can be used to run the script using the following command:
```python
python PTtoAT.py Example 1
```
The script will save the Process Tree file in .xml, the Attack Tree file in .xml and the RISQFlan file in .bbt