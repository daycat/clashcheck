import os.path
from multiprocessing import Process, Manager
from check import check
from yaml.loader import SafeLoader
import os.path
import yaml

if __name__ == '__main__':
    with Manager() as manager:
        if not os.path.exists('./temp'):
            os.mkdir('temp')
        with open ('config.yaml','r') as reader:
            config = yaml.load(reader,Loader=SafeLoader)
            start_port = config['start_port']
        alive = manager.list()
        with open ('in.yaml','r') as reader:
            config = yaml.load(reader,Loader=SafeLoader)
        config = config['proxies']
        processes =[]
        for i in config:
            p = Process(target=check, args=(alive,i,start_port))
            p.start()
            processes.append(p)
            start_port = start_port+1
        for p in processes:
            p.join