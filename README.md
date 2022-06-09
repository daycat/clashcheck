# clashcheck
A fast clash proxy checker, built from clash-core.

## Installation:
1. Clone to local
```sh
git clone https://github.com/daycat/clashcheck.git && cd clashcheck
```
2. Install python and Pip3 (Search for guides for your OS)
3. Install python prerequisites
```sh
pip3 install -r requirements.txt
```
4. MacOS / Linux : Increase your max open file count
5. Get Country.mmdb into ~/.config/clash/
```sh
wget https://github.com/Dreamacro/maxmind-geoip/releases/latest/download/Country.mmdb -O ~/.config/clash/Country.mmdb
```

## Run:
```sh
python3 main.py
```

## Configuration:
``` yaml
http-port: 23940 #port to run http proxy on
api-port: 23941 #api port
threads: 100 #thread number
source: https://ghproxy.com/https://raw.githubusercontent.com/daycat/freeray/main/output.yaml # can be local file or internet address
outfile: optimized.yaml # must be local file
timeout: 3000 #timeout in miliseconds
```

