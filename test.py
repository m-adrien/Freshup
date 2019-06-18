#!/usr/bin/python3.5
# -*-coding:utf-8 -*

# ---------- Module | Conf.ini | Options ---------- #

# Import argparse pour les options
import argparse
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
# HELP OPTION
parser.add_argument("-d", help="DHCP : will be not installed")
parser.add_argument("-f", help="FIREWALL : will be not installed")
parser.add_argument("-i", help="INTERFACES : will be not configured")
parser.add_argument("-n", help="NAT : will be not configured")
parser.add_argument("-f", help="net-tools and ns-lookup : will be not installed")
parser.add_argument("-f", help="net-tools and ns-lookup : will be not installed")
#
parser.parse_args()