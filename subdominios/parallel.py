import sys
import os

domain = sys.argv[1]

def parallel():
    os.system('rm -rf /home/victor/Recon/subdominios/arquivo.log')
    with open ('/home/victor/Recon/subdominios/arquivo.log','a') as file:
        file.write('python3 /home/victor/Github/Github/Reconhecimento/subdominio.py -v -d '+domain+'\n')
        file.write('python3 /home/victor/Github/Github/Reconhecimento/subdominio.py -f assetfinder -d '+domain+'\n')
        file.write('python3 /home/victor/Github/Github/Reconhecimento/subdominio.py -f subfinder -d '+domain+'\n')
        file.write('python3 /home/victor/Github/Github/Reconhecimento/subdominio.py -f crt -d '+domain+'\n')
        file.write('python3 /home/victor/Github/Github/Reconhecimento/subdominio.py -f amass -d '+domain+'\n')
        file.write('python3 /home/victor/Github/Github/Reconhecimento/subdominio.py -f haktrails -d '+domain+'\n')
        file.write('python3 /home/victor/Github/Github/Reconhecimento/subdominio.py -httpx -d '+domain+'\n')
        file.write('python3 /home/victor/Github/Github/Reconhecimento/subdominio.py -enviar -d '+domain+'\n')
    print("[+] PROCESSANDO SUBDOMAIN \n")
    os.system(f'cat /home/victor/Recon/subdominios/arquivo.log | parallel -u -j 2 ')
def main():
   parallel()
if __name__ == '__main__':
    main()