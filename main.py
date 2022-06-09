import os.path
import time
from multiprocessing import Process, Manager, Semaphore
from yaml.loader import SafeLoader
from clash import push
from tqdm import tqdm
import json
import yaml
import requests
import shutil
import subprocess


def check(alive, proxy, apiurl,sema,timeout):
    r = requests.get(url=apiurl + '/proxies/'+str(proxy['name'])+'/delay?url=http://gstatic.com/generate_204&timeout='+str(timeout))
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
            source = str(config['source'])
            timeout = config['timeout']
            outfile = config['outfile']
        alive = manager.list()
        if source.startswith('https://'):
            proxyconfig = yaml.load(requests.get(source).text,Loader=SafeLoader)
        else:
            with open (source,'r') as reader:
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
        for i in tqdm(range(int(len(config['proxies']))), desc="Testing"):
            sema.acquire()
            p = Process(target=check, args=(alive,config['proxies'][i],apiurl,sema,timeout))
            p.start()
            processes.append(p)
        for p in processes:
            p.join
        time.sleep(10)
        alive=list(alive)
        push(alive,outfile)
        shutil.rmtree('./temp')
        clash.terminate()

