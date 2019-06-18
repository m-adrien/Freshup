#!/usr/bin/python3.5
# -*-coding:utf-8 -*

# ---------- Module | Conf.ini | Options ---------- #

# Import argparse pour les options
import argparse
# Import commandes bash de l'os
import os
# On importe la configuration
import configparser
# On recupère nos variables du fichier .ini
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

# Création des argument options :
parser = argparse.ArgumentParser()
parser.parse_args()

# -----------Vérifions que nous sommes sur Debian----------- #

# Création -> variable verif -> présence du mot debian dans la version de la distribution

os.system('uname -a | grep Debian')
verif = os.system('echo $?')
# Si Verif = 1 = pas sur Debian = On arrête le programme
if verif == 1:
   sys.exit([0])
# ---Verification OK + Conf Chargé --> C'est parti !--- #

# -----------Configuration des interfaces-----------#

# Ouverture et ecriture (erase) du fichier de conf
interfaces = open("/etc/network/interfaces", "w")
# Insertion de la conf de base
interfaces.write("source /etc/network/interfaces.d/*\n\n#loopback iface\nauto lo\niface lo inet loopback\n\n")
# Insertion de la conf de l'iface 1
interfaces.write("#Iface 1\nauto enp0s3\niface enp0s3 inet static\naddress {}\nnetmask {}\ngateway {}\n\n"
                 .format(IP1, NM1, GW1))
# Insertion de la conf de l'iface 2
interfaces.write("#Iface 2\nauto enp0s3\niface enp0s3 inet static\naddress {}\nnetmask {}\ngateway {}\n\n"
                 .format(IP2, NM2, GW2))
# Insertion de la conf de l'iface 3
interfaces.write("#Iface 3\nauto enp0s3\niface enp0s3 inet static\naddress {}\nnetmask {}\ngateway {}\n\n"
                 .format(IP3, NM3, GW3))
# Fermeture du fichier
interfaces.close()
# --- Configuration interface terminée --- #

# ---------- Configuration NAT et FIREWALL ---------- #

# NAT en postrouting
if NAT1 == 1:
    os.system('iptables -t nat -A POSTROUTING -o enp0s3 -j MASQUERADE')
if NAT2 == 1:
    os.system('iptables -t nat -A POSTROUTING -o enp0s8 -j MASQUERADE')
if NAT3 == 1:
    os.system('iptables -t nat -A POSTROUTING -o enp0s9 -j MASQUERADE')
#


