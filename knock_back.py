
#python3
import os
import json
import nmap3
import argparse
from time import sleep
from urllib.parse import urlparse
from threading import Lock
from tkinter import messagebox
from flask import Flask, request, render_template, abort, g


#Flask App must be declared globally, for @app Routing
app = Flask('Knock Back', static_url_path='/static', static_folder='static')
#app.config['DEBUG'] = True

# Suspicious markers from Nmap GET/POST requests to a target machine
NMAP_NIX_FLAG = 'nmaplowercheck'    # Appears before randomized numerical sequence.
NMAP_WIN_FLAG = 'nice%20ports'      # Appears static with Trinity. A Matrix Nod?!?
NMAP_URL_FLAGS = ['jobtracker.jsp','flumemaster.jsp','evox.about','nmaplowercheck',
                  'nice%20ports','Trinity.txt.bak']

# State Variables. The 'g' Construct from Flask may be more elegant.
STATE_LOCK = Lock()
BEING_SCANNED = False
FIRST_HIT = False
STARTED_SCAN = False
FINISHED_SCAN = False

# Can be set by User Arguments or defaults.
OUTPUT_PATH = None
INTERVAL = None
PERSIST_DELAYS = None


def Main(args):
    global INTERVAL
    global OUTPUT_PATH
    global PERSIST_DELAYS

    #handle args
    fp = os.path.join(os.getcwd(),args.output)
    with STATE_LOCK:
        OUTPUT_PATH = fp
        INTERVAL = args.interval
        PERSIST_DELAYS = args.annoy
    
    app.run(host='0.0.0.0', port=args.port)
    


@app.route("/hello",methods=['GET'])
def home():
    global PERSIST_DELAYS
    global INTERVAL

    with STATE_LOCK:
        mode = PERSIST_DELAYS
        timeout = INTERVAL
    
    page_html = '<h1>Welcome to Knock Back!</h1></p>Persistent Delays are: <b>{0}</b>'.format(mode)
    page_html += '<p>Delays during Nmap scans are: <b>{0}s</b><p>'.format(timeout)
    return(page_html)


@app.route("/reset",methods=['GET'])
def reset():
    global BEING_SCANNED
    global FIRST_HIT
    global STARTED_SCAN
    global FINISHED_SCAN
    
    with STATE_LOCK:
        BEING_SCANNED = False
        FIRST_HIT = False
        STARTED_SCAN = False
        FINISHED_SCAN = False

    return('Scanning State Reset.')

@app.route('/',methods=['GET','POST'])
def index():
    return('/..')


@app.before_request
def inspectRequest():
    global BEING_SCANNED
    global FIRST_HIT
    global STARTED_SCAN
    global FINISHED_SCAN
    global PERSIST_DELAYS
    global OUTPUT_PATH
    global INTERVAL

    path = request.url
    remote_ip = request.remote_addr
    remote_user = request.remote_user
    
    with STATE_LOCK:
        resetFlags = FINISHED_SCAN
        persisting = PERSIST_DELAYS

    if resetFlags and not persisting:
        with STATE_LOCK:
            BEING_SCANNED = False
            STARTED_SCAN = False
            FINISHED_SCAN = False
            FIRST_HIT = False 

    # Check a variety of potential markers across Linux and Windows scans.
    for flag in NMAP_URL_FLAGS:
        if flag in path:
            msg = 'Detected Nmap Scan from: {0} - user: {1}!'.format(remote_ip,remote_user)
            terminal_msg = paintRed(msg)
            print(terminal_msg)

            with STATE_LOCK:
                #setattr(g, '_BEING_SCANNED', True)
                BEING_SCANNED = True
                alreadyHit = FIRST_HIT
            
            if not alreadyHit:
                messagebox.showwarning('Detected Nmap!',msg)
            with STATE_LOCK:
                FIRST_HIT = True

    with STATE_LOCK:
        counterScanning = STARTED_SCAN
        beingScanned = BEING_SCANNED
        print('Detected Scan is {0}'.format(beingScanned))
        print('Counter Scan is {0}'.format(counterScanning))

    if beingScanned and not counterScanning:    
        
        with STATE_LOCK:
            #setattr(g,'_SCAN_STARTED',True)
            STARTED_SCAN = True
        
        mapper = nmap3.Nmap()
        print(paintYel('Started Nmap() Counterscan...'))
        results = mapper.nmap_os_detection(remote_ip, args='-A -sV')

        with STATE_LOCK:   
            fp = OUTPUT_PATH
            writeToJSON(fp,results) 
            FINISHED_SCAN = True 
        
        msg = 'Counter scan results against IP:{0} saved to: {1}'.format(remote_ip,fp)
        messagebox.showinfo('Counter-Scan Complete.',msg)

    #Degrade performance between subsequent attacking Nmap scan attempts.
    with STATE_LOCK:
        shouldSleep = BEING_SCANNED
        interval = INTERVAL
        print('Should sleep is: {0}'.format(shouldSleep))

    if shouldSleep:
        print('going to sleep for {0}s...'.format(interval))
        sleep(interval)

    return


def paintRed(str):
    RED = '\033[91m'
    END = '\033[0m' #terminates colored text
    return RED + str + END
 
def paintYel(str):
    YELLOW = '\033[93m'
    END = '\033[0m' #terminates colored text
    return YELLOW + str + END


def writeToJSON(output_fp, obj):
    
    with open(output_fp, 'w', encoding='utf-8') as file:
        #json.dump(obj, f, ensure_ascii=False, indent=4)
        json.dump(obj, file, indent=4)


if __name__ == "__main__":
    
    desc = '''A Decoy Web Application that monitors for Nmap Probes and 
            performs a counter-scan against the attacking machine.'''
    arg_psr = argparse.ArgumentParser(description=desc)
    arg_psr.add_argument('-a','--annoy',default=False, action='store_true',
        help='Once Nmap is detected, persist all future HTTP delays until the server state is reset.')
    arg_psr.add_argument('-p','--port',default=9999,
        help='The port to run the application on. Defaults to 9999.')
    arg_psr.add_argument('-i','--interval',default=5, type=int,
        help='The interval, in seconds, to sleep between attacker Nmap HTTP calls.')
    arg_psr.add_argument('-o','--output',default='counter_scan.json',
        help='What to name the JSON output file. Example: myScanLog.json')
    args = arg_psr.parse_args()

    Main(args)
#Fin