#!/bin/bash



if [ $1 = '--recon' ] && [ $2 ]
    then
        echo '[+] Recon Subdomain'

        echo -e '\e[32;1m[+] Enumeration subfinder'

        subfinder -d $2 -silent -all -o $2_subfinder.txt
        
        echo -e '\e[31;1m[+] Enumeration assetfinder'

        assetfinder -subs-only $2 >> $2_assetfinder.txt

        echo -e '\e[33;1m[+] Enumeration crt.sh'

        curl -s "https://crt.sh/?q=%25.$2&output=json" | jq -r ".[].name_value" | sed 's/\*\.//g' >> $2_crt.sh.txt

        echo -e '\e[34;1m[+] Enumeration findomain'

        findomain -t $2 -q >> $2_findomain.txt

        echo -e '\e[36;1m[+] Enumeration amass'

        amass enum -d $2 -o $2_amass1.txt

        echo -e '\e[31;1m[+] Enumeration Haktrails'

        echo $2 | haktrails $2_haktrails.txt
        
        echo -e '\e[30;1m[+] Enumeração httpx'

        cat $2_subfinder.txt $2_assetfinder.txt $2_crt.sh.txt $2_amass1.txt $2_findomain.txt $2_haktrails.txt >> $2_subdomain.txt ; cat $2_subdomain.txt | anew | httpx -l $2_subdomain.txt -silent -threads 100 >> $2_validados.txt; rm -rf $2_subfinder.txt $2_assetfinder.txt $2_crt.sh.txt $2_findomain.txt $2_amass1.txt $2_haktrails.txt

else

    echo -e "\e[32;1mForma de uso: ./recon.sh --recon ^dominio^"

fi
