FROM kalilinux/kali-rolling:latest

WORKDIR /data

RUN mkdir -p /root/.config/haktools

RUN mkdir -p /root/.config/subfinder

COPY provider-config.yaml /root/.config/subfinder/

COPY haktrails-config.yml /root/.config/haktools/

RUN apt-get update

RUN apt-get upgrade -y

RUN apt-get dist-upgrade -y

RUN apt-get install locate -y

RUN apt-get install wget -y

RUN apt-get install git -y

RUN apt-get install jq -y 

RUN apt-get install vim -y

RUN apt-get install golang -y

RUN apt-get install python3 -y

RUN apt-get install python3-pip -y

RUN go env -w GO111MODULE=auto

RUN go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest
RUN mv /root/go/bin/subfinder /usr/bin/

RUN apt-get install sublist3r -y

RUN apt-get install nmap -y

RUN apt-get install nikto -y

RUN apt-get install hydra -y

RUN go install -v github.com/tomnomnom/assetfinder@latest
RUN mv /root/go/bin/assetfinder /usr/bin/

RUN go install -v github.com/projectdiscovery/httpx/cmd/httpx@latest
RUN mv /root/go/bin/httpx /usr/bin/

RUN go install -v github.com/tomnomnom/anew@latest
RUN mv /root/go/bin/anew /usr/bin/

RUN go install -v github.com/hakluke/haktrails@latest
RUN mv /root/go/bin/haktrails /usr/bin/

RUN go install -v github.com/OWASP/Amass/v3/...@master
RUN mv /root/go/bin/amass /usr/bin/
