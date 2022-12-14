#!/bin/bash


if [ $1 = '--recon' ] && [ $2 ]
    then
        echo '[+] RECON SUBDOMINIO'

        echo -e '\e[32;1m[!] Enumeração subfinder'

        subfinder -d $2 -silent -all -o $2_subfinder.txt
        
        echo -e '\e[31;1m[!] Enumeração assetfinder'

        assetfinder -subs-only $2 >> $2_assetfinder.txt

        echo -e '\e[33;1m[!] Enumeração crt.sh'

        curl -s "https://crt.sh/?q=%25.$2&output=json" | jq -r ".[].name_value" | sed 's/\*\.//g' >> $2_crt.sh.txt

        echo -e '\e[34;1m[!] Enumeração findomain'

        findomain -t $2 -q >> $2_findomain.txt

        echo -e '\e[36;1m[!] Enumeração amass'  

        amass enum -d $2 -o $2_amass1.txt

        echo -e '\e[31;1m[!] Enumeração Haktrails'

        echo $2 | haktrails $2_haktrails.txt
        
        echo -e '\e[30;1m[!] Enumeração httpx'

        cat $2_subfinder.txt $2_assetfinder.txt $2_crt.sh.txt $2_amass1.txt $2_findomain.txt $2_haktrails.txt >> $2_subdomain.txt ; cat $2_subdomain.txt | anew | httpx -l $2_subdomain.txt -silent -threads 100 -o $2_validados.txt; rm -rf $2_subfinder.txt $2_assetfinder.txt $2_crt.sh.txt $2_findomain.txt $2_amass1.txt $2_haktrails.txt

        echo '[+] RECON CRAWLER'

        cat $2_validados.txt | waybackurls  
else

    echo -e "\e[32;1mForma de uso: ./recon.sh --recon ^dominio^"

fi
