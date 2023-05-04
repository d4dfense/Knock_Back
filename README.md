# Knock Back
<p>Knock Back is a simple defensive countermeasure tool designed to detect inbound  
Network Map (Nmap) probes. While running as a (minimal) decoy web server on the   
host system, the tool monitors for incoming HTTP requests typical of a Nmap scan.  
If detected, the user can degrade the scan with excessive slow-downs and launch   
their own probe to gather information on where an incoming Nmap scan originated.</p>
<br>

## Features
<p>At a glance, Knock Knock provides the following capabilities:</p>

 - Monitor a host against incoming Nmap scans and launch a counter-scan.
 - Degrade peformance of an incoming Nmap scan, throughout the lifetime of our counter-scan or until instructed to stop.
 - Run on either Linux or Windows* based host machine.
<p></p>
 *Windows Machines can detect Nmap scans and downgrade performance, yet have a known issue for attacker OS identification.
<p></p><br>

## Requirements
<p>In order to run Knock Back, ensure you have the following dependencies:</p>

 * Nmap installed on the host system (Tested with versions 7.92 on Linux, 7.93 on Windows)
 * python 3.10
 * python3-nmap 1.6.0
 * flask 2.0.1
<p></p><br>

## Usage
To run the tool at the command line and view help regarding input arguments:
```
  $ python knock_back.py -h
```
To adjust the performance of an incoming Nmap scan, set an interval (seconds). This delays the responses to the originator:
```
  $ python knock_back.py -i 15
```
Note: To attempt attribution against the originating scanner machine, you must run as root:
```
  $ sudo python knock_back.py
```
Once the script is up and running, use a browser to verify the application is up:
- http[]()://localhost:9999/hello

To persistently delay an Nmap scan, even after a counter-scan, set the annoyance flag (-a or --annoy):
```
  $ sudo python knock_back.py -i 15 --annoy
```
This will delay all further HTTP responses to the server on the host machine. To reset the server state, navigate to:
- http[]()://localhost:9999/reset

Optionally, specify custom parameters to change the default app port and output files:
```
  $ sudo python knock_back.py -p 8888 -a -i 7 -o myScanResults.json
```

At any time, close the Knock Back tool with a CTRL-C command input to the terminal:
```
  $ ^C
```
<p></p><br>

## Limitations
- Knock Back monitors against certain known Nmap commands. However, advanced Nmap users may create more stealthy, less noisy scans. 
Knock Back is not guaranteed to detect all possible Nmap scans. See alternative tools, such as OsChameleon, for good examples of
further ways to detect reconnaissance tools such as Nmap at the network packet layer.
- Attribution is not always straightforward. Improvements to the tool might include a traceroute capability to complement Nmap.
