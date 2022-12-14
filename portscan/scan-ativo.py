import xml.etree.ElementTree as ET
import sys
import socket
import os
import json
import uuid
import pymongo
from time import strftime
import subprocess

dominio = sys.argv[1]
dominio2 = dominio.split(".")[0]
myclient = pymongo.MongoClient("")
hora = strftime("%Y-%m-%dT%H:%M:%S")
collection = "portscan"
mydb = myclient[dominio2]
mycol = mydb[collection]
x = str(uuid.uuid1()).split('-')[0]
scanner = 'nmap' + x
dic_ports = {}
ip = sys.argv[2]

def executa(dominio):
    subprocess.check_output(f"docker volume create {scanner}",shell=True)
    subprocess.check_output(f'docker run --rm --name {scanner} -v {scanner}:/data kali:3.0 nmap -sSV -Pn {ip} -oX {scanner}.xml', shell=True)

def parse():
    tree = ET.parse(f'/var/lib/docker/volumes/{scanner}/_data/{scanner}.xml')
    root = tree.getroot()
    for i in root.iter('nmaprun'):
        for nmaprun in i:
            if(nmaprun.tag == 'host'):
                for host in nmaprun:
                    if(host.tag == 'address'):
                        if(':' not in host.attrib['addr']):
                            dic_ports['ip_v4'] = host.attrib['addr']
                            dic_ports['network.type'] = host.attrib['addrtype']
                    if(host.tag == 'ports'):
                        for port in host:
                            if(port.tag == 'port'):
                                dic_ports['network.transport'] = port.attrib['protocol']
                                dic_ports['server.port'] = port.attrib['portid']
                                for itens in port:
                                    if(itens.tag == 'state'):
                                        dic_ports['service.state'] = itens.attrib['state']
                                    if(itens.tag == 'service'):
                                        try:
                                            dic_ports['network.protocol'] = itens.attrib['name']
                                        except:
                                            dic_ports['network.protocol'] = ''
                                        try:
                                            dic_ports['application.version.number'] = itens.attrib['version']
                                        except:
                                            dic_ports['application.version.number'] = ''
                                        try:
                                            dic_ports['service.name'] = itens.attrib['product']
                                        except:
                                            dic_ports['service.name'] = ''
                                        dic_ports['server.ipblock'] = ip
                                        data = {
                    				            '@timestamp':hora,
                    				            'server.address':ip,
                    				            'network.protocol':dic_ports['network.protocol'],
                    				            'server.ip':ip,
                    				            'server.port':dic_ports['server.port'],
                    				            'server.ipblock':dic_ports['server.ipblock'],
                    				            'server.name':dic_ports['service.name'],
                    				            'server.state':dic_ports['service.state'],
                    				            'network.transport':dic_ports['network.transport'],
                    				            'network.type':dic_ports['network.type'],
                    				            'application.version.number':dic_ports['application.version.number'],
                    				            'vulnerability.scanner.vendor':'nmap'
            				                    }
                                        mycol.insert_one(data)
        subprocess.check_output(f"docker volume rm -f {scanner}",shell=True)
        subprocess.check_output(f"rm -rf /var/lib/docker/volumes/{scanner}",shell=True)
                                        
def main():
    executa(dominio)
    parse()
    
if __name__== '__main__':
    main()
