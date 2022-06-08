import os.path
import time
from multiprocessing import Process, Manager, Semaphore
from yaml.loader import SafeLoader
import json
import yaml
import requests
import subprocess


def check(alive, proxy, apiurl,sema):
    r = requests.get(url=apiurl + '/proxies/'+str(proxy['name'])+'/delay?url=http://gstatic.com/generate_204&timeout=3000')
    response = json.loads(r.text)
    try:
        if response['delay'] > 0:
            alive.append(proxy)
    except:
        pass

    sema.release()



if __name__ == '__main__':
    with Manager() as manager:
        if not os.path.exists('./temp'):
            os.mkdir('temp')
        with open ('config.yaml','r') as reader:
            config = yaml.load(reader,Loader=SafeLoader)
            http_port = config['http-port']
            api_port = config['api-port']
            threads = config['threads']
        alive = manager.list()
        with open ('output.yaml','r') as reader:
            proxyconfig = yaml.load(reader,Loader=SafeLoader)
        baseurl = '127.0.0.1:' + str(api_port)
        config = {'port': http_port, 'external-controller': baseurl, 'mode': 'global',
                      'log-level': 'silent', 'proxies': proxyconfig['proxies']}
        with open('./temp/working.yaml', 'w') as file:
            file = yaml.dump(config, file)
        clash = subprocess.Popen(['./clash', '-f', './temp/working.yaml'])
        processes =[]
        apiurl='http://'+baseurl
        sema = Semaphore(threads)
        time.sleep(5)
        for i in config['proxies']:
            sema.acquire()
            p = Process(target=check, args=(alive,i,apiurl,sema))
            p.start()
            processes.append(p)
        for p in processes:
            p.join
        time.sleep(10)
        alive=list(alive)
        print(alive)

        clash.terminate()

