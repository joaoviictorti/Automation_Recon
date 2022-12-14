import pymongo
from time import strftime
import subprocess
import json
import argparse
from argparse import BooleanOptionalAction


class Subdominios():

    def __init__(self:object,dominio:str):
        self.__dominio = dominio
    
    def subfinder(self:object):
        ferramenta = "subfinder"
        subprocess.check_output(f"docker run --rm --name {ferramenta} -v {self.__dominio}:/data kali:4.0 /bin/bash -c \"subfinder -d {self.__dominio} -silent >> subfinder.txt\"",shell=True)

    def assetfinder(self:object):
        ferramenta = "assetfinder"
        subprocess.check_output(f"docker run --rm --name {ferramenta} -v {self.__dominio}:/data kali:4.0 /bin/bash -c \"assetfinder -subs-only {self.__dominio} >> assetfinder.txt\"",shell=True)

    def crt(self:object):
        ferramenta = "crt"
        subprocess.check_output(f"docker run --rm --name {ferramenta} -v {self.__dominio}:/data kali:4.0 /bin/bash -c \"curl -s \"https://crt.sh/?q={self.__dominio}&output=json\"| jq -r \".[].name_value\" | sed 's/\*\.//g' >> crt.txt\" ",shell=True)

    def amass(self:object):
        ferramenta = "amass"
        subprocess.check_output(f"docker run --rm --name {ferramenta} -v {self.__dominio}:/data kali:4.0 /bin/bash -c \"amass enum -d {self.__dominio} -o amass.txt\"",shell=True)

    def haktrails(self:object):
        ferramenta = "haktrails"
        subprocess.check_output(f"docker run --rm --name {ferramenta} -v {self.__dominio}:/data kali:4.0 /bin/bash -c \"echo {self.__dominio} | haktrails haktrails.txt\"",shell=True)

    def createvolume(self:object):
        subprocess.check_output(f"docker volume create {self.__dominio}",shell=True)

class Validacao():

    def __init__(self:object,dominio:str):
        self.__dominio = dominio

    def httpx(self:object):
        ferramenta = "httpx"
        subprocess.check_output(f"docker run --rm --name {ferramenta} -v {self.__dominio}:/data kali:3.0 /bin/bash -c \"cat * | anew | httpx -silent -json -o {self.__dominio}.json\"",shell=True)

class Enviar():

    def __init__(self:object,dominio:str):
        self.__dominio = dominio
        
    def enviar(self:object):
        hora = strftime("%Y-%m-%dT%H:%M:%S%Z")
        domain = self.__dominio.split(".")[0]
        collection ="subdominios"
        myclient = pymongo.MongoClient("")
        mydb = myclient[domain]
        mycol = mydb[collection]
        with open(f"/var/lib/docker/volumes/{self.__dominio}/_data/{self.__dominio}.json") as json_file:
            dic_subdomain = {}
            for line in json_file:
                json_line = line.rstrip('\n')
                jsondata = json.loads(json_line)
                try:
                    dic_subdomain['url'] = jsondata['url']
                except:
                    dic_subdomain['url'] = ""
                try:
                    dic_subdomain['porta'] = jsondata['port']
                except:
                    dic_subdomain['porta'] = ""
                try:
                    dic_subdomain['scheme'] = jsondata['scheme']  
                except:
                    dic_subdomain['scheme'] = ""
                try:
                    dic_subdomain['webserver'] = jsondata['webserver']
                except:
                    dic_subdomain['webserver'] = ""
                try:
                    dic_subdomain['host'] = jsondata['host']
                except:
                    dic_subdomain['host'] = '0.0.0.0'
                try:
                    dic_subdomain['status-code'] = jsondata['status_code']
                except:                
                    dic_subdomain['status-code'] = ""
                
                dic_subdomain['timestamp'] = hora

                data = {
                    "Data": dic_subdomain['timestamp'],
                    "url": dic_subdomain['url'],
                    "porta": dic_subdomain['porta'],
                    "scheme":dic_subdomain['scheme'],
                    "webserver":dic_subdomain['webserver'],
                    "host":dic_subdomain['host'],
                    "status-code": dic_subdomain['status-code']
                }
                mycol.insert_one(data)
            subprocess.check_output(f"docker volume rm -f {self.__dominio}",shell=True)
            subprocess.check_output(f"rm -rf /var/lib/docker/volumes/{self.__dominio}",shell=True)


parser = argparse.ArgumentParser(usage="Recon Completo")
parser.add_argument("-f",dest="ferramenta",choices=['assetfinder','subfinder','crt','findomain','amass','haktrails'],action="store",help="Ferramenta")
parser.add_argument("-v",dest="volume",action=argparse.BooleanOptionalAction,type=bool,help="Volume",default=True)
parser.add_argument("-d",dest="dominio",action="store",help="Dominio")
parser.add_argument("-httpx",dest="httpx",action=argparse.BooleanOptionalAction,help="Ferramenta",default=True)
parser.add_argument("-enviar",dest="enviar",action=argparse.BooleanOptionalAction,help="Ferramenta",default=True)

args = parser.parse_args()

match args.volume:
    case True:
        Subdominios(args.dominio).createvolume()
    case _:
        pass

match args.ferramenta:
    case "assetfinder":
        Subdominios(args.dominio).assetfinder()
    case "subfinder":
        Subdominios(args.dominio).subfinder()
    case "crt":
        Subdominios(args.dominio).crt()
    case "amass":
        Subdominios(args.dominio).amass()
    case "haktrails":
        Subdominios(args.dominio).haktrails()
    case _:
        pass

match args.httpx:
    case True:
        Validacao(args.dominio).httpx()

match args.enviar:
    case True:
        Enviar(args.dominio).enviar()
    case _:
        pass