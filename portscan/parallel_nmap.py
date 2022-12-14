import sys
import socket
import subprocess
import os
import json
from time import strftime
import pymongo

dominio = sys.argv[1]
myclient = pymongo.MongoClient("")

def consulta():
    list_ap = []
    mydb = myclient['businesscorp']
    mycol = mydb["subdominios"]
    for x in mycol.find():
        if x['host'] in list_ap:
            pass
        else:
            list_ap.append((x['host']))
    return list_ap

def parallel():
	os.system('rm -rf /home/victor/Recon/portscan/nmap_parallel.log')
	for ip in consulta():
		with open ('/home/victor/Recon/portscan/nmap_parallel.log','a') as file:
			file.write(f'python3 /home/victor/Recon/portscan/nmap.py {dominio} {ip}'+'\n')
	print("[+] PROCESSANDO NMAP \n")
	os.system('cat /home/victor/Recon/portscan/nmap_parallel.log | parallel -u -j 2')
def main():
	consulta()
	parallel()
if __name__ == '__main__':
    main()
