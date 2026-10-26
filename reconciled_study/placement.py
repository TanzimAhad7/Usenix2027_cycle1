#!/usr/bin/env python3
"""Observe socket ownership and descendant NVIDIA workers before using a server."""
import argparse
import csv
import io
import json
import re
import subprocess

def command(argv):
    return subprocess.run(argv,check=True,capture_output=True,text=True,timeout=15).stdout

def evaluate(gpu, port, devices, applications, processes, sockets):
    if gpu not in (2,3):
        raise ValueError('Only physical GPU 2 or 3 is authorized')
    mapping={int(row[0].strip()):row[1].strip() for row in csv.reader(io.StringIO(devices)) if len(row)==2}
    expected=mapping.get(gpu)
    if not expected:raise ValueError('Requested physical GPU absent')
    listeners=set()
    for line in sockets.splitlines():
        fields=line.split()
        if len(fields)>3 and re.search(r':'+str(port)+r'$',fields[3]):
            listeners.update(int(x) for x in re.findall(r'pid=(\d+)',line))
    if not listeners:raise ValueError('Cannot establish local server socket owner')
    parents={}
    for line in processes.splitlines():
        fields=line.split()
        if len(fields)==2 and all(x.isdigit() for x in fields):parents[int(fields[0])]=int(fields[1])
    def belongs(pid):
        seen=set()
        while pid and pid not in seen:
            if pid in listeners:return True
            seen.add(pid);pid=parents.get(pid,0)
        return False
    workers=[]
    for row in csv.reader(io.StringIO(applications)):
        if len(row)!=2 or not row[0].strip().isdigit():continue
        pid=int(row[0]);uuid=row[1].strip()
        if belongs(pid):workers.append({'pid':pid,'gpu_uuid':uuid})
    if not workers:raise ValueError('No GPU workers attributable to server; cannot qualify GPU ownership')
    if any(w['gpu_uuid']!=expected for w in workers):raise ValueError('Server uses a GPU outside the selected physical device')
    return {'qualified':True,'physical_gpu':gpu,'gpu_uuid':expected,'port':port,'socket_owner_pids':sorted(listeners),'gpu_workers':workers,'scope':'Observed process ownership at preflight; no permanent deployment guarantee'}

def qualify(gpu,port):
    return evaluate(gpu,port,
        command(['nvidia-smi','--query-gpu=index,uuid','--format=csv,noheader,nounits']),
        command(['nvidia-smi','--query-compute-apps=pid,gpu_uuid','--format=csv,noheader,nounits']),
        command(['ps','-eo','pid=,ppid=']),command(['ss','-ltnp']))

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--gpu',type=int,choices=[2,3],required=True)
    p.add_argument('--port',type=int,required=True)
    a=p.parse_args()
    try:print(json.dumps(qualify(a.gpu,a.port),indent=2))
    except Exception as exc:
        print(json.dumps({'qualified':False,'error':str(exc)}))
        raise SystemExit(2)
