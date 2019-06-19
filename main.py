#!/usr/bin/python3.5
# -*-coding:utf-8 -*

# ---------- Module | Conf.ini | Options ---------- #

import argparse  # Importe argparse pour les options
import os  # Importe commandes bash de l'os
import configparser  # On importe la configuration et le module argument
import threading  # Importe modul pour faire du thread
import sys

# Création des argument options :
print("Initialisation...")
config = configparser.ConfigParser()
parser = argparse.ArgumentParser()
parser.add_argument("-d", "--dhcp", help="DHCP : will be not installed", action="store_false")
parser.add_argument("-f", "--firewall", help="FIREWALL : will be not installed", action="store_false")
parser.add_argument("-i", "--interfaces", help="INTERFACES : will be not configured", action="store_false")
parser.add_argument("-n", "--nat", help="NAT : will be not configured", action="store_false")
parser.add_argument("-r", "--restart", help="Sytème will be reboot at the end of FRESHUP", action="store_false")
parser.add_argument("-t", "--tools", help="net-tools ns-lookup and tcp-dump : will be not installed",
                    action="store_false")
parser.add_argument("-F", "--force", help="Force the installation on other distribution BE CAREFUL",
                    action="store_false")
parser.parse_args()

# On recupère nos variables du fichier .ini
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
FWE = config.get('FIREWALL', 'FWE')
FWP = config.get('FIREWALL', 'FWP')
FWD = config.get('FIREWALL', 'FWD')
FWH = config.get('FIREWALL', 'FWH')
FWS = config.get('FIREWALL', 'FWS')
DHCP1 = config.get('DHCP', 'DHCP1')
DHCP2 = config.get('DHCP', 'DHCP2')
DHCP3 = config.get('DHCP', 'DHCP3')
DHSUB1 = config.get('DHCP', 'SUBNET1')
DHSUB2 = config.get('DHCP', 'SUBNET2')
DHSUB3 = config.get('DHCP', 'SUBNET3')
DHNM1 = config.get('DHCP', 'NETMASK1')
DHNM2 = config.get('DHCP', 'NETMASK2')
DHNM3 = config.get('DHCP', 'NETMASK3')
ST1 = config.get('DHCP', 'START1')
ST2 = config.get('DHCP', 'START2')
ST3 = config.get('DHCP', 'START3')
END1 = config.get('DHCP', 'END1')
END2 = config.get('DHCP', 'END2')
END3 = config.get('DHCP', 'END3')
DGATE1 = config.get('DHCP', 'DGATE1')
DGATE2 = config.get('DHCP', 'DGATE2')
DGATE3 = config.get('DHCP', 'DGATE3')
print('done.\n')

# ----------- Vérifions que nous sommes sur Debian ----------- #

if arg.force:
    # Création -> variable verif -> présence du mot debian dans la version de la distribution
    print('Verification...')
    os.system('uname -a | grep Debian')
    verif = os.system('echo $?')
    # Si Verif = 1 = pas sur Debian = On arrête le programme
    if verif == 1:
        sys.stdout.write('Vous n\'êtes pas sur une distribution Debian\nYour are not on a Debian Distribution')
        sys.exit([0])
    # ---Verification OK + Conf Chargé --> C'est parti !--- #
    print('done.\n')
# ----------- Configuration des interfaces -----------#

if arg.interfaces:
    print('Interfaces configuration...')
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
    print('done.\n')

# ---------- Configuration NAT et FIREWALL ---------- #

# -- Firewall -- #
if arg.firewall:
    print('Firewall configuration ...\n')
    # On met en DROP toutes les policy ipv4 et ipv6
    os.system('iptables -P INPUT DROP')
    os.system('iptables -P OUTPUT DROP')
    os.system('iptables -P FORWARD DROP')
    os.system('ip6tables -P INPUT DROP')
    os.system('ip6tables -P OUTPUT DROP')
    os.system('ip6tables -P FORWARD DROP')
    # On autorise en IPv4
    if FWE == 1:
        # Connections déjà établies
        os.system('iptables -A INPUT -m conntrack --ctstate RELATED,ESTABLISHED -j ACCEPT')
        os.system('iptables -A OUTPUT -m conntrack --ctstate RELATED,ESTABLISHED -j ACCEPT')
        os.system('iptables -A FORWARD -m conntrack --ctstate RELATED,ESTABLISHED -j ACCEPT')
    if FWP == 1:
        # Ping : icmp
        os.system('iptables -A INPUT -p icmp -j ACCEPT')
        os.system('iptables -A OUTPUT -p icmp -j ACCEPT')
        os.system('iptables -A FORWARD -p icmp -j ACCEPT')
    if FWD == 1:
        # DNS : udp 53
        os.system('iptables -A INPUT -p udp --dport 53 -j ACCEPT')
        os.system('iptables -A OUTPUT -p udp --dport 53 -j ACCEPT')
        os.system('iptables -A FORWARD -p udp --dport 53 -j ACCEPT')
    if FWH == 1:
        # HTTP : tcp 80
        os.system('iptables -A INPUT -p tcp --dport 80 -j ACCEPT')
        os.system('iptables -A OUTPUT -p tcp --dport 80 -j ACCEPT')
        os.system('iptables -A FORWARD -p tcp --dport 80 -j ACCEPT')
    if FWS == 1:
        # HTTPS : tcp 443
        os.system('iptables -A INPUT -p tcp --dport 443 -j ACCEPT')
        os.system('iptables -A OUTPUT -p tcp --dport 443 -j ACCEPT')
        os.system('iptables -A FORWARD -p tcp --dport 443 -j ACCEPT')
    # FIN DE LA CONFIG PARE-FEU
    print('done.\n')

# -- NAT en postrouting -- #
if arg.nat:
    print('NAT configuration...\n')
    if NAT1 == 1:
        os.system('iptables -t nat -A POSTROUTING -o enp0s3 -j MASQUERADE')
    if NAT2 == 1:
        os.system('iptables -t nat -A POSTROUTING -o enp0s8 -j MASQUERADE')
    if NAT3 == 1:
        os.system('iptables -t nat -A POSTROUTING -o enp0s9 -j MASQUERADE')
    print('done.\n')

# -- Iptalbes-persistent -- #
if (arg.nat) or (arg.firewall):
    print('Iptables-persistent setup...\n')
    # Création de la fonction d'install
    def iptables_install():
        """Setup iptable-persistent on linux distribution which have aperture"""
        os.system('apt-get install -y iptables-persistent')
    # Attente de la fin d'installation mis en thread par la fonction
    def wait_iptables():
        thread = threading.Thread(target=iptables_install)
        thread.start()
    print('done.\n')

# ---------- Configuration du serveur DHCP --------- #
if arg.dhcp:
    print('DHCP-server setup...\n')
    # Création de la fonction d'install
    def dhcp_install():
        """Setup isc-dhcp-server on linux distribution which have aperture"""
        os.system('apt-get install -y isc-dhcp-serveur')
    # Attente de la fin d'installation mis en thread par la fonction
    def wait_dhcp():
        thread = threading.Thread(target=dhcp_install)
        thread.start()
    # Configuration de dhcpd.conf
    dhcpd = open("/etc/dhcp/dhcpd.conf", "a")
    dhcpd.write('\nautoritative;\n\n')
    if DHCP1 == 1:
        dhcpd.write("subnet {} netmask {} {\n  range {} {};\n  option routers {};\n}\n\n"
                      .format(DHSUB1, DHNM1, ST1, END1, IP1))
    if DHCP2 == 1:
        dhcpd.write("subnet {} netmask {} {\n  range {} {};\n  option routers {};\n}\n\n"
                      .format(DHSUB2, DHNM2, ST2, END2, IP2))
    if DHCP3 == 1:
        dhcpd.write("subnet {} netmask {} {\n  range {} {};\n  option routers {};\n}\n\n"
                      .format(DHSUB3, DHNM3, ST3, END3, IP3))
    dhcpd.close()
    iscdhcpd = open("/etc/default/isc-dhcp-server", "w") # Config de l'écoute en fct des paramètres
    if DHCP1 == 1 and DHCP2 == 0 and DHCP3 == 0:
        iscdhcpd.write('INTERFACESv4="enp0s3"\nINTERFACESv6=""\n')
    if DHCP1 == 0 and DHCP2 == 1 and DHCP3 == 0:
        iscdhcpd.write('INTERFACESv4="enp0s8"\nINTERFACESv6=""\n')
    if DHCP1 == 0 and DHCP2 == 0 and DHCP3 == 1:
        iscdhcpd.write('INTERFACESv4="enp0s9"\nINTERFACESv6=""\n')
    if DHCP1 == 1 and DHCP2 == 1 and DHCP3 == 0:
        iscdhcpd.write('INTERFACESv4="enp0s3 enp0s8"\nINTERFACESv6=""\n')
    if DHCP1 == 1 and DHCP2 == 0 and DHCP3 == 1:
        iscdhcpd.write('INTERFACESv4="enp0s3 enp0s9"\nINTERFACESv6=""\n')
    if DHCP1 == 0 and DHCP2 == 1 and DHCP3 == 1:
        iscdhcpd.write('INTERFACESv4="enp0s8 enp0s9"\nINTERFACESv6=""\n')
    if DHCP1 == 1 and DHCP2 == 1 and DHCP3 == 1:
        iscdhcpd.write('INTERFACESv4="enp0s3 enp0s8 enp0s9"\nINTERFACESv6=""\n')
    print('done.\n')
# ---------- Activation du routage ---------- #
sysctl = open("/etc/sysctl.conf", "a")
sysctl.write('\nnet.ipv4.ip_forward=1\n')
sysctl.close()
os.system('sysctl -p /etc/sysctl.conf')
print("Forwarding enable")
# ---------- Redémmarage des services ---------- #
# Si on ne force pas le reboot alors on relance les services qui ont été modifiés
if not arg.restart:
    if arg.interfaces:
        os.system('/etc/init.d/networking restart')
    if arg.dhcp:
        os.system('service dhcp restart')
# Si on reboot (-r) alors on ne relance pas les services.
if arg.restart:
    os.system('init 6')
print('Thank you to make a fresh up of your server !\n')

# --------------------- |||||||||||||||||| ---------------------- #
# --------------------- |FIN DU PROGRAMME| ---------------------- #
# --------------------- |||||||||||||||||| ---------------------- #
