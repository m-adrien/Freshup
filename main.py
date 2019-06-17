#!/usr/bin/python3.5
# -*-coding:utf-8 -*

#Création des argument options :
import argparse
parser = argparse.ArgumentParser()
parser.parse_args()

####Vérifions que nous sommes sur Debian####

##Création -> variable verif -> présence du mot debian dans la version de la distribution##
#Import commandes bash de l'os#
import os
os.system('uname -a | grep Debian')
verif = os.system('echo $?')
#Si Verif = 1 = pas sur Debian = On arrête le programme
if verif == 1:
   sys.exit([0])

#On importe la configuration et on recupère nos variables
import configparser
config = configparser.ConfigParser()
config.read('conf.ini')
IP1 = config.get('INTERFACES', 'IP1')
IP2 = config.get('INTERFACES', 'IP2')
IP3 = config.get('INTERFACES', 'IP3')
NM1 = config.get('INTERFACES', 'NM1')
NM2 = config.get('INTERFACES', 'NM2')
NM3 = config.get('INTERFACES', 'NM3')
GW1 = config.get('INTERFACES', 'GW1')
GW2 = config.get('INTERFACES', 'GW2')
GW3 = config.get('INTERFACES', 'GW3')
NAT1 = config.get('NAT', 'NAT1')
NAT2 = config.get('NAT', 'NAT2')
NAT3 = config.get('NAT', 'NAT3')
DHCP1 = config.get('DHCP', 'DHCP1')
DHCP2 = config.get('DHCP', 'DHCP2')
DHCP3 = config.get('DHCP', 'DHCP3')
START1 = config.get('DHCP', 'START1')
START2 = config.get('DHCP', 'START2')
START3 = config.get('DHCP', 'START3')
END1 = config.get('DHCP', 'END1')
END2 = config.get('DHCP', 'END2')
END3 = config.get('DHCP', 'END3')
DGATE1 = config.get('DHCP', 'DGATE1')
DGATE2 = config.get('DHCP', 'DGATE2')
DGATE3 = config.get('DHCP', 'DGATE3')

##Verifications et la conf OK --> C'est parti ! ##
#Configuration des interfaces

interfaces = open("/etc/network/interfaces", "w")
#Importation du module pickle
import pickle
#Création du pickle de conf de base
iface0 = "source /etc/network/interfaces.d/*\n\n#loopback iface\nauto lo\niface lo inet loopback\n\n"
with open('iface0', 'wb') as fichier:
    mon_pickler = pickle.Pickler(fichier)
    mon_pickler.dump(score)

#Création du pickle "iface1" de conf d'interfaces 1
iface1 = "#Iface 1\nauto enp0s3\niface enp0s3 inet static\naddress {}\nnetmask {}\ngateway {}\n\n".format(IP1, NM1, GW1)
with open('iface1', 'wb') as fichier:
    mon_pickler = pickle.Pickler(fichier)
    mon_pickler.dump(score)

#Création du pickle "iface2" de conf d'interfaces 2
iface2 = "#Iface 2\nauto enp0s3\niface enp0s3 inet static\naddress {}\nnetmask {}\ngateway {}\n\n".format(IP2, NM2, GW2)
with open('iface2', 'wb') as fichier:
    mon_pickler = pickle.Pickler(fichier)
    mon_pickler.dump(score)

#Création du pickle "iface3" de conf d'interfaces 3
iface3 = "#Iface 3\nauto enp0s3\niface enp0s3 inet static\naddress {}\nnetmask {}\ngateway {}\n\n".format(IP3, NM3, GW3)
with open('iface3', 'wb') as fichier:
    mon_pickler = pickle.Pickler(fichier)
    mon_pickler.dump(score)

#Ramplacer le fichier interface par nos valeurs