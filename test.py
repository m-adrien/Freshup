
import argparse  # Importation argparse pour les options
import os  # Importation commandes bash de l'os
import threading  # Importation du module pour faire du thread
import sys  # Importation des commandes sys essentiels
import subprocess  # Importation du module subprocess
import json  # Importation de la configuration
import time
import re

# Création du dictionnaire de config :
data = open('conf.json', 'r')
config = json.load(data)
data.close()

# Création des argument :
parser = argparse.ArgumentParser()
parser.add_argument("-d", "--dhcp", help="DHCP : will not ne installed", action="store_false")
parser.add_argument("-f", "--firewall", help="FIREWALL : will not be installed", action="store_false")
parser.add_argument("-i", "--interfaces", help="INTERFACES : will not be configured", action="store_false")
parser.add_argument("-n", "--nat", help="NAT : will not be configured", action="store_false")
parser.add_argument("-r", "--route", help="Forwarding will not be enable", action="store_false")
parser.add_argument("-t", "--tools", help="Net-tools dnsUtils tcp-dump and SSH: will be not installed",
                    action="store_false")
parser.add_argument("-F", "--force", help="Force the installation on other distribution BE CAREFUL",
                    action="store_false")
args = parser.parse_args()

# ------------------------------------ Verification de conf.json ------------------------ #
# Encodage du regex pour determiner ip dans la variable regip
regip = re.compile("^([0-9]{1,3}\.){3}[0-9]{1,3}?$")

# Création des dictionnaires de conf.json
a1 = config['FireWall']['Server']
a2 = config['FireWall']['eth0']['INPUT']
a3 = config['FireWall']['eth0']['OUTPUT']
a4 = config['FireWall']['eth1']['INPUT']
a5 = config['FireWall']['eth1']['OUTPUT']
a6 = config['FireWall']['eth2']['INPUT']
a7 = config['FireWall']['eth2']['OUTPUT']
b1 = config['DHCP']['eth0']
b2 = config['DHCP']['eth1']
b3 = config['DHCP']['eth2']


def verifdico(dico):
    """Vérifie le contenue d'un dictionnaire les valeurs des clé doivent corrrespondre à regip défini ailleurs en regex
    les clé devront alors être une adress ip si non le script quittera avec un code erreur 3"""
    for key, values in dico.items():
        if not regip.match(values):
            print('There is an error in conf.json > DHCP.')
            sys.exit(3)


verifdico(b1)
verifdico(b2)
verifdico(b3)


def verifkey(key):
    """Vérifie le contenue d'une clé la valeurs da la clé devra corrrespondre à regip défini ailleurs en regex
    la clé doit  alors être une adress ip si non le script quittera avec un code erreur 3"""
    if not regip.match(key):
        print('There is an error in conf.json > Interfaces')
        sys.exit(3)


verifkey(config['Interfaces']['eth0']['IP'])
verifkey(config['Interfaces']['eth0']['NetMask'])
verifkey(config['Interfaces']['eth0']['GateWay'])
verifkey(config['Interfaces']['eth1']['IP'])
verifkey(config['Interfaces']['eth1']['NetMask'])
verifkey(config['Interfaces']['eth1']['GateWay'])
verifkey(config['Interfaces']['eth2']['IP'])
verifkey(config['Interfaces']['eth2']['NetMask'])
verifkey(config['Interfaces']['eth2']['GateWay'])


def verifkey2(key):
    """Vérifie le contenue d'une clé pour que sa valeur soit binaire, si non --> exit status = 3"""
    if (key != 0 and key != 1):
        print('There is an error in conf.json > Interfaces')
        sys.exit(3)


verifkey2(config['Interfaces']['eth0']['Activated'])
verifkey2(config['Interfaces']['eth0']['Firewall'])
verifkey2(config['Interfaces']['eth1']['Activated'])
verifkey2(config['Interfaces']['eth1']['Firewall'])
verifkey2(config['Interfaces']['eth2']['Activated'])
verifkey2(config['Interfaces']['eth2']['Firewall'])


def verifkey3(key):
    """Vérifie le contenue d'une clé pour que sa valeur soit égale à DMZ, LAN ou NET si non --> exit status = 3"""
    if (key != 'DMZ' and key != 'LAN' and key != 'NET'):
        print('There is an error in conf.json > Interfaces > Type ')
        sys.exit(3)


verifkey3(config['Interfaces']['eth0']['Type'])
verifkey3(config['Interfaces']['eth1']['Type'])
verifkey3(config['Interfaces']['eth2']['Type'])

if all(value in {0, 1,} for value in a1.values()):
    pass
else:
    print('There is an error in conf.json : FireWall > Server.')
    sys.exit(3)

if all(value in {0, 1, 2} for value in a2.values()):
    pass
else:
    print('There is an error in conf.json : FireWall > eth0 > INTPUT.')
    sys.exit(3)

if all(value in {0, 1, 2} for value in a3.values()):
    pass
else:
    print('There is an error in conf.json : FireWall > eth0 > OUTPUT.')
    sys.exit(3)

if all(value in {0, 1, 2} for value in a4.values()):
    pass
else:
    print('There is an error in conf.json : FireWall > eth1 > INTPUT.')
    sys.exit(3)

if all(value in {0, 1, 2} for value in a5.values()):
    pass
else:
    print('There is an error in conf.json : FireWall > eth1 > OUTPUT.')
    sys.exit(3)

if all(value in {0, 1, 2} for value in a6.values()):
    pass
else:
    print('There is an error in conf.json : FireWall > eth2 > INTPUT.')
    sys.exit(3)

if all(value in {0, 1, 2} for value in a7.values()):
    pass
else:
    print('There is an error in conf.json : FireWall > eth2 > OUTPUT.')
    sys.exit(3)

