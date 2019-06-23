# -*-coding:latin-1 -*

import configparser
config = configparser.ConfigParser()
config.read('conf.ini')
if config['DHCP']['DHCP1'] == '0':
    if config['DHCP']['DHCP2'] == '1':
        print("#Iface 1\nauto enp0s3\niface enp0s3 inet static\naddress {}\nnetmask {}\ngateway {}\n\n"
             .format(config['INTERFACES']['IP1'], config['INTERFACES']['NM1'], config['INTERFACES']['GW1']))
