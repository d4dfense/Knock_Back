# Knock Back
Knock Back is a simple defensive countermeasure tool designed to detect inbound
Network Map (Nmap) probes. While running as a (minimal) decoy web server on the 
host system, the tool monitors for incoming HTTP requests typical of a Nmap scan.
If detected, the user can degrade the scan with excessive slow-downs and launch 
their own probe to gather information on where an incoming Nmap scan originated.

## Features
<p>Here are some features</p>
- bullet 1
- bullet 2
- bullet 3

## Requirements
<p>In order to run Knock Back, ensure you have the following dependencies:</p>
- Nmap installed on the host system (Tested with 7.92 on Linux)
- python 3.10
- python3-nmap 1.6.0
- flask 2.0.1

### Usage
To run the tool at the command line:
```
  $ python knock_back.py
```
To degrade the performance of an incoming Nmap scan, set an interval (seconds). This delays the responses to the originator:
```
  $ python knock_back.py -i 30
```
Note: To attempt attribution against the originating scanner machine, you must run as root:
```
  $ sudo python knock_back.py
```
Optionally, specify custom parameters to change the default app port and output files:
```
  $ sudo python knock_back.py -p 8888 -i 7 -o myScanResults.json
```
Once the script is up and running, use a browser to verify the application is up:
- http://localhost:9999/hello

To reset the server state back to defaults after a known NMAP scan, navigate to:
- http://localhost:9999/reset
## Limitations
Knock Back monitors against a few known Nmap commands. However, advanced Nmap users may create more stealthy, less noisy scans. 
Knock Back is not guaranteed to detect all possible Nmap scans. See alternative tools, such as oschameleon, for good examples of
further ways to detect reconnaissance tools such as Nmap at the network packet layer.
