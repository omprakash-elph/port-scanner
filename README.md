# 🔍 Multithreaded Port Scanner

A fast, multithreaded Python port scanner with service detection and banner grabbing.

## Features
- Multithreaded scanning (configurable threads)
- Service name detection
- Banner grabbing
- Results saved to output file
- Color coded terminal output

## Requirements
- Python 3
- colorama

## Installation
git clone https://github.com/YOURUSERNAME/port-scanner.git
cd port-scanner
pip install -r requirements.txt

## Usage
python3 Scanner1.py -t 192.168.1.1 -p 1-1000 -T 100 -o results.txt

## Arguments
| Argument | Description | Example |
|---|---|---|
| -t | Target IP address | -t 192.168.1.1 |
| -p | Port range | -p 1-1000 |
| -T | Number of threads | -T 100 |
| -o | Output file | -o results.txt |

## Legal Disclaimer
This tool is for educational purposes and authorized testing only.
Never scan systems without permission.

## Author
Om Prakash Kumar -https://github.com/omprakash-elph
