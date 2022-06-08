import string
import yaml
import random
def check(alive, proxy, port):
    config = {'port': port, 'mode': 'global', 'log-level': 'silent', 'proxies': [proxy]}
    fn = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(3))
    with open ('./temp/'+fn+'.yaml','w') as file:
        file = yaml.dump(config, file)
