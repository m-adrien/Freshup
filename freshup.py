#!/usr/bin/python3.5
# -*-coding:utf-8 -*

# -------------------------------- Module | Conf.ini | Options ---------------------------- #

import argparse  # Importation argparse pour les options
import os  # Importation commandes bash de l'os
import threading  # Importation du module pour faire du thread
import sys  # Importation des commandes sys essentiels
import subprocess  # Importation du module subprocess
import json  # Importation de la configuration
import time

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

# ------------------------------------- Création de nos fonctions ----------------------- #


def remplacement(fichier, cherche, remplace):
    """Cherche dans 'fichier' une chaine de caratère la valeur 'cherche'
    et remplace toutes les chaines de caracteres correspondante par remplace (sensible à la case)"""
    s = open(fichier).read()
    s = s.replace(cherche, remplace)
    f = open(fichier, 'w')
    f.write(s)
    f.close()


def installation(paquet,):
    def install():
        """Installe le paquet (écrire le nom exacte) donné en argument. Attent la fin de l'installation
        pour continuer le programme. Ecrit dans le log et dans la console l'installation du paquet"""

        print('{} setup....').format(paquet)
        with open('freshup.log', 'a') as freshlog:
            freshlog.write('{} setup :\n\n\n').format(paquet)
            subprocess.Popen("apt-get install -y {}", shell=True, stdout=freshlog, stderr=freshlog).format(paquet)

    def main():  # Mise en thread et attente du thread dans def main
        thread = threading.Thread(target=install)
        thread.start()
        thread.join()
    if __name__ == '__main__':
        main()
    print('done.\n')


# -------------------------------- Vérifiations Distribution ------------------------------ #

if args.force:
    print('Verification...')
    """On lance un sousprocess via popen et on redirige stdout dans child pour avoir le exit statut
       Ici uname -a donne la version complète et grep chercher la présence du mot Débian"""
    child = subprocess.Popen("uname -a | grep Debian", shell=True, stdout=subprocess.PIPE)
    streamdata = child.communicate()[0]
    if child.returncode != 0:  # Si exit status de grep Debian n'est pas bon on quitte
        print('Vous n\'êtes pas sur une distribution Debian\nYour are not on a Debian Distribution\n')
        sys.exit(1)
    print('done.\n')

# -------------------------------- Vérifiations connection -------------------------------- #

# Vérification connection internet
child = subprocess.Popen("ping 8.8.8.8 -c 4", shell=True, stdout=subprocess.PIPE)
streamdata = child.communicate()[0]
ping = child.returncode
if ping == 0:
    child = subprocess.Popen("ping google.com -c 4", shell=True, stdout=subprocess.PIPE)
    streamdata = child.communicate()[0]
    dns = child.returncode
    if dns == 0:
        print('Connection is ok : configuration will proceede')
    else:
        print('Ping is ok... but it seem to have other troubles (could be a DNS resolving)'
              '\nPlease check your connection')
        sys.exit(2)
else:
    print('There is some troubles... can\'t ping 8.8.8.8\nPlease check your connection\n')
    sys.exit(2)

# ------------------------------------ Installation des outils ---------------------------- #

if args.tools:
    print('Tools setup...\n')
    installation('openssh-server')
    installation('net-tools')
    installation('tcpdump')
    installation('dnsutils')

# --------------------------- Setup & Configuration du serveur DHCP ----------------------- #

if args.dhcp:
    installation('isc-dhcp-server')
    # Configuration de dhcpd.conf
    with open("/etc/dhcp/dhcpd.conf", "a") as dhcpd:
        dhcpd.write('\nautoritative;\n\n')
        if config['Interfaces']['eth0']['Type'] == 'LAN' or config['DHCP']['eth0']['Forced'] == 1:
            dhcpeth0 = 1 # Création de la variable pour la suite
            dhcpd.write("subnet {} netmask {} {{\n  range {} {};\n  option routers {};\n}}\n\n"
                        .format(config['DHCP']['eth0']['SubNet'], config['DHCP']['eth0']['NetMask'],
                                config['DHCP']['eth0']['Start'], config['DHCP']['eth0']['End'],
                                config['DHCP']['eth0']['Dgate']))

        if config['Interfaces']['eth1']['Type'] == 'LAN' or config['DHCP']['eth1']['Forced'] == 1:
            dhcpeth1 = 1 # Création de la variable pour la suite
            dhcpd.write("subnet {} netmask {} {{\n  range {} {};\n  option routers {};\n}}\n\n"
                        .format(config['DHCP']['eth1']['SubNet'], config['DHCP']['eth1']['NetMask'],
                                config['DHCP']['eth1']['Start'], config['DHCP']['eth1']['End'],
                                config['DHCP']['eth1']['Dgate']))

        if config['Interfaces']['eth2']['Type'] == 'LAN' or config['DHCP']['eth2']['Forced'] == 1:
            dhcpeth2 = 1 # Création de la variable pour la suite
            dhcpd.write("subnet {} netmask {} {{\n  range {} {};\n  option routers {};\n}}\n\n"
                        .format(config['DHCP']['eth2']['SubNet'], config['DHCP']['eth2']['NetMask'],
                                config['DHCP']['eth2']['Start'], config['DHCP']['eth2']['End'],
                                config['DHCP']['eth2']['Dgate']))

    # Configuration de default/isc-dhcp-server

    iscdhcpd = open("/etc/default/isc-dhcp-server", "w")  # Config de l'écoute en fnct des paramètres

    if dhcpeth0 == 1 and dhcpeth1 != 1 and dhcpeth2 != 1:
        remplacement('/etc/default/isc-dhcp-server', 'INTERFACESv4=""', 'INTERFACESv4="eth0"')
    if dhcpeth0 != 1 and dhcpeth1 == 1 and dhcpeth2 != 1:
        remplacement('/etc/default/isc-dhcp-server', 'INTERFACESv4=""', 'INTERFACESv4="eth1"')
    if dhcpeth0 != 1 and dhcpeth1 != 1 and dhcpeth2 == 1:
        remplacement('/etc/default/isc-dhcp-server', 'INTERFACESv4=""', 'INTERFACESv4="eth2"')

    if dhcpeth0 == 1 and dhcpeth1 == 1 and dhcpeth2 != 1:
        remplacement('/etc/default/isc-dhcp-server', 'INTERFACESv4=""', 'INTERFACESv4="eth0 eth1"')
    if dhcpeth0 == 1 and dhcpeth1 != 1 and dhcpeth2 == 1:
        remplacement('/etc/default/isc-dhcp-server', 'INTERFACESv4=""', 'INTERFACESv4="eth0 eth2"')
    if dhcpeth0 != 1 and dhcpeth1 == 1 and dhcpeth2 == 1:
        remplacement('/etc/default/isc-dhcp-server', 'INTERFACESv4=""', 'INTERFACESv4="eth1 eth2"')

    if dhcpeth0 == 1 and dhcpeth1 == 1 and dhcpeth2 == 1:
        remplacement('/etc/default/isc-dhcp-server', 'INTERFACESv4=""', 'INTERFACESv4="eth0 eth1 eth2"')
    print('done.\n')

# ------------------------------------ Configuration FIREWALL ----------------------------- #

# En plus de l'argument -r on ne configure rien si toutes les options FIrewall sont à zéro
if args.firewall and not (config['Interfaces']['eth0']['Firewall'] == 0 and
                          config['Interfaces']['eth1']['Firewall'] == 0 and
                          config['Interfaces']['eth2']['Firewall'] == 0):
    print('Firewall configuration ...\n')

    # On met en DROP toutes les policy ipv4 et ipv6
    os.system('iptables -P INPUT DROP')
    os.system('iptables -P OUTPUT DROP')
    os.system('iptables -P FORWARD DROP')
    os.system('ip6tables -P INPUT DROP')
    os.system('ip6tables -P OUTPUT DROP')
    os.system('ip6tables -P FORWARD DROP')
    # On autorise en IPv4 les ports selon la config :
    # ----------------------------------------------------------------- #
    # ------------------ CONFIGURATION eth0 --------------------------- #
    # ----------------------------------------------------------------- #
    if config['Interfaces']['eth0']['Firewall'] == 1:

        # Established dans tout les cas on install sauf si on force
        if config['FireWall']['eth0']['INPUT']['Established']!= 0:
            os.system('iptables -A FORWARD -i eth0 -m conntrack --ctstate RELATED,ESTABLISHED -j ACCEPT')
        if config['FireWall']['eth0']['INPUT']['Established'] != 0:
            os.system('iptables -A FORWARD -o eth0 -m conntrack --ctstate RELATED,ESTABLISHED -j ACCEPT')
        # Ping icmp
        if config['FireWall']['eth0']['INPUT']['Ping'] == 2:
            os.system('iptables -A FORWARD -i eth0 -p icmp -j ACCEPT')
        if config['FireWall']['eth0']['OUPUT']['Ping'] == 2:
            os.system('iptables -A FORWARD -o eth0 -p icmp -j ACCEPT')
        # DNS
            # INPUT
        if ((config['FireWall']['eth0']['INPUT']['DNS'] == 2 or
            config['Interfaces']['eth0']['Type'] == 'LAN') and config['FireWall']['eth0']['INPUT']['DNS'] != 0):
            os.system('iptables -A FORWARD -i eth0 -p tcp --dport 53 -j ACCEPT')
            os.system('iptables -A FORWARD -i eth0 -p udp --dport 53 -j ACCEPT')
            # OUTPUT
        if ((config['FireWall']['eth0']['OUTPUT']['DNS'] == 2 or
            config['Interfaces']['eth0']['Type'] == 'LAN' or config['Interfaces']['eth0']['Type'] == 'NET') and
            config['FireWall']['eth0']['OUTPUT']['DNS'] != 0):
            os.system('iptables -A FORWARD -o eth0 -p tcp --dport 53 -j ACCEPT')
            os.system('iptables -A FORWARD -o eth0 -p udp --dport 53 -j ACCEPT')
        # HTTP
            # INPUT
        if ((config['FireWall']['eth0']['INPUT']['HTTP'] == 2 or
            config['Interfaces']['eth0']['Type'] == 'NET' or config['Interfaces']['eth0']['Type'] == 'DMZ') and
                config['FireWall']['eth0']['INPUT']['HTTP'] != 0):
            os.system('iptables -A FORWARD -i eth0 -p tcp --dport 80 -j ACCEPT')
            # OUTPUT
        if ((config['FireWall']['eth0']['OUTPUT']['HTTP'] == 2 or
            config['Interfaces']['eth0']['Type'] == 'LAN' or config['Interfaces']['eth0']['Type'] == 'NET') and
            config['FireWall']['eth0']['OUTPUT']['HTTP'] != 0):
            os.system('iptables -A FORWARD -o eth0 -p tcp --dport 80 -j ACCEPT')
        # HTTPS
            # INPUT
        if ((config['FireWall']['eth0']['INPUT']['HTTPS'] == 2 or
            config['Interfaces']['eth0']['Type'] == 'NET' or config['Interfaces']['eth0']['Type'] == 'DMZ') and
                config['FireWall']['eth0']['INPUT']['HTTPS'] != 0):
            os.system('iptables -A FORWARD -i eth0 -p tcp --dport 443 -j ACCEPT')
            # OUTPUT
        if ((config['FireWall']['eth0']['OUTPUT']['HTTPS'] == 2 or
            config['Interfaces']['eth0']['Type'] == 'LAN' or config['Interfaces']['eth0']['Type'] == 'NET') and
            config['FireWall']['eth0']['OUTPUT']['HTTPS'] != 0):
            os.system('iptables -A FORWARD -o eth0 -p tcp --dport 443 -j ACCEPT')
        # PRINTER
            # INPUT
        if ((config['FireWall']['eth0']['INPUT']['Printer'] == 2 or
            config['Interfaces']['eth0']['Type'] == 'LAN') and
                config['FireWall']['eth0']['INPUT']['Printer'] != 0):
            os.system('iptables -A FORWARD -i eth0 -p tcp --dport 631 -j ACCEPT')
            os.system('iptables -A FORWARD -i eth0 -p udp --dport 631 -j ACCEPT')
            # OUTPUT
        if ((config['FireWall']['eth0']['OUTPUT']['Printer'] == 2 or
            config['Interfaces']['eth0']['Type'] == 'LAN') and
            config['FireWall']['eth0']['OUTPUT']['Printer'] != 0):
            os.system('iptables -A FORWARD -o eth0 -p tcp --dport 631 -j ACCEPT')
            os.system('iptables -A FORWARD -o eth0 -p udp --dport 631 -j ACCEPT')
        # DHCP
            # INPUT
        if ((config['FireWall']['eth0']['INPUT']['DHCP'] == 2 or
            config['Interfaces']['eth0']['Type'] == 'LAN') and
                config['FireWall']['eth0']['INPUT']['DHCP'] != 0):
            os.system('iptables -A FORWARD -i eth0 -p tcp --dport 68 -j ACCEPT')
            os.system('iptables -A FORWARD -i eth0 -p udp --dport 67 -j ACCEPT')
            os.system('iptables -A FORWARD -i eth0 -p udp --dport 68 -j ACCEPT')
            # OUTPUT
        if ((config['FireWall']['eth0']['OUTPUT']['DHCP'] == 2 or
            config['Interfaces']['eth0']['Type'] == 'LAN' or config['Interfaces']['eth0']['Type'] == 'NET') and
            config['FireWall']['eth0']['OUTPUT']['DHCP'] != 0):
            os.system('iptables -A FORWARD -o eth0 -p tcp --dport 68 -j ACCEPT')
            os.system('iptables -A FORWARD -o eth0 -p udp --dport 67 -j ACCEPT')
            os.system('iptables -A FORWARD -o eth0 -p udp --dport 68 -j ACCEPT')
        # FTP
            # INPUT
        if ((config['FireWall']['eth0']['INPUT']['FTP'] == 2 or
            config['Interfaces']['eth0']['Type'] == 'NET' or config['Interfaces']['eth0']['Type'] == 'DMZ') and
                config['FireWall']['eth0']['INPUT']['FTP'] != 0):
            os.system('iptables -A FORWARD -i eth0 -p tcp --dport 20 -j ACCEPT')
            os.system('iptables -A FORWARD -i eth0 -p tcp --dport 21 -j ACCEPT')
            # OUTPUT
        if ((config['FireWall']['eth0']['OUTPUT']['FTP'] == 2 or
            config['Interfaces']['eth0']['Type'] == 'LAN' or config['Interfaces']['eth0']['Type'] == 'NET') and
            config['FireWall']['eth0']['OUTPUT']['FTP'] != 0):
            os.system('iptables -A FORWARD -o eth0 -p tcp --dport 20 -j ACCEPT')
            os.system('iptables -A FORWARD -o eth0 -p tcp --dport 21 -j ACCEPT')
        # SSH
            # INPUT
        if ((config['FireWall']['eth0']['INPUT']['SSH'] == 2 or
            config['Interfaces']['eth0']['Type'] == 'LAN' or config['Interfaces']['eth0']['Type'] == 'DMZ') and
                config['FireWall']['eth0']['INPUT']['SSH'] != 0):
            os.system('iptables -A FORWARD -i eth0 -p tcp --dport 22 -j ACCEPT')
            # OUTPUT
        if ((config['FireWall']['eth0']['OUTPUT']['SSH'] == 2 or
            config['Interfaces']['eth0']['Type'] == 'LAN' or config['Interfaces']['eth0']['Type'] == 'NET') and
            config['FireWall']['eth0']['OUTPUT']['SSH'] != 0):
            os.system('iptables -A FORWARD -o eth0 -p tcp --dport 22 -j ACCEPT')
        # IMAP
            # INPUT
        if config['FireWall']['eth0']['INPUT']['IMAP'] != 0:
            os.system('iptables -A FORWARD -i eth0 -p tcp --dport 143 -j ACCEPT')
            os.system('iptables -A FORWARD -i eth0 -p tcp --dport 220 -j ACCEPT')
            os.system('iptables -A FORWARD -i eth0 -p tcp --dport 993 -j ACCEPT')
            # OUTPUT
        if ((config['FireWall']['eth0']['OUTPUT']['DNS'] == 2 or
            config['Interfaces']['eth0']['Type'] == 'LAN' or config['Interfaces']['eth0']['Type'] == 'NET') and
            config['FireWall']['eth0']['OUTPUT']['DNS'] != 0):
            os.system('iptables -A FORWARD -o eth0 -p tcp --dport 143 -j ACCEPT')
            os.system('iptables -A FORWARD -o eth0 -p tcp --dport 220 -j ACCEPT')
            os.system('iptables -A FORWARD -o eth0 -p tcp --dport 993 -j ACCEPT')
        # SMTP
            # INPUT
        if config['FireWall']['eth0']['INPUT']['SMTP'] != 0:
            os.system('iptables -A FORWARD -i eth0 -p tcp --dport 25 -j ACCEPT')
            os.system('iptables -A FORWARD -i eth0 -p tcp --dport 587 -j ACCEPT')
            os.system('iptables -A FORWARD -i eth0 -p tcp --dport 465 -j ACCEPT')
            # OUTPUT
        if ((config['FireWall']['eth0']['OUTPUT']['SMTP'] == 2 or
            config['Interfaces']['eth0']['Type'] == 'LAN' or config['Interfaces']['eth0']['Type'] == 'NET') and
            config['FireWall']['eth0']['OUTPUT']['SMTP'] != 0):
            os.system('iptables -A FORWARD -o eth0 -p tcp --dport 25 -j ACCEPT')
            os.system('iptables -A FORWARD -o eth0 -p tcp --dport 587 -j ACCEPT')
            os.system('iptables -A FORWARD -o eth0 -p tcp --dport 465 -j ACCEPT')
        # POP3
            # INPUT
        if config['FireWall']['eth0']['INPUT']['POP3'] != 0:
            os.system('iptables -A FORWARD -i eth0 -p tcp --dport 110 -j ACCEPT')
            os.system('iptables -A FORWARD -i eth0 -p tcp --dport 985 -j ACCEPT')
            # OUTPUT
        if ((config['FireWall']['eth0']['OUTPUT']['POP3'] == 2 or
            config['Interfaces']['eth0']['Type'] == 'LAN' or config['Interfaces']['eth0']['Type'] == 'NET') and
            config['FireWall']['eth0']['OUTPUT']['POP3'] != 0):
            os.system('iptables -A FORWARD -o eth0 -p tcp --dport 110 -j ACCEPT')
            os.system('iptables -A FORWARD -o eth0 -p tcp --dport 985 -j ACCEPT')
        # NTP
            # INPUT
        if (config['FireWall']['eth0']['INPUT']['NTP'] == 2 or
            config['Interfaces']['eth0']['Type'] == 'LAN' and
                config['FireWall']['eth0']['INPUT']['NTP'] != 0):
            os.system('iptables -A FORWARD -i eth0 -p udp --dport 123 -j ACCEPT')
            # OUTPUT
        if ((config['FireWall']['eth0']['OUTPUT']['NTP'] == 2 or
            config['Interfaces']['eth0']['Type'] == 'LAN' or config['Interfaces']['eth0']['Type'] == 'NET') and
            config['FireWall']['eth0']['OUTPUT']['NTP'] != 0):
            os.system('iptables -A FORWARD -o eth0 -p udp --dport 123 -j ACCEPT')
        # AVAHI
            # INPUT
        if config['FireWall']['eth0']['INPUT']['Avahi'] == 2:
            os.system('iptables -A FORWARD -i eth0 -p udp --dport 5353 -j ACCEPT')
            # OUTPUT
        if config['FireWall']['eth0']['OUTPUT']['Avahi'] == 2:
            os.system('iptables -A FORWARD -o eth0 -p udp --dport 5353 -j ACCEPT')
        # NETBIOS
            # INPUT
        if (config['FireWall']['eth0']['INPUT']['Netbios'] == 2 or
            config['Interfaces']['eth0']['Type'] == 'LAN' and
                config['FireWall']['eth0']['INPUT']['Netbios'] != 0):
            os.system('iptables -A FORWARD -i eth0 -p tcp --dport 137 -j ACCEPT')
            os.system('iptables -A FORWARD -i eth0 -p tcp --dport 138 -j ACCEPT')
            os.system('iptables -A FORWARD -i eth0 -p tcp --dport 139 -j ACCEPT')
            os.system('iptables -A FORWARD -i eth0 -p tcp --dport 445 -j ACCEPT')
            # OUTPUT
        if (config['FireWall']['eth0']['OUTPUT']['Netbios'] == 2 or
            config['Interfaces']['eth0']['Type'] == 'LAN' and
            config['FireWall']['eth0']['OUTPUT']['Netbios'] != 0):
            os.system('iptables -A FORWARD -o eth0 -p tcp --dport 137 -j ACCEPT')
            os.system('iptables -A FORWARD -o eth0 -p tcp --dport 138 -j ACCEPT')
            os.system('iptables -A FORWARD -o eth0 -p tcp --dport 139 -j ACCEPT')
            os.system('iptables -A FORWARD -o eth0 -p tcp --dport 445 -j ACCEPT')
        # LDAP
            # INPUT
        if (config['FireWall']['eth0']['INPUT']['LDAP'] == 2 or
            config['Interfaces']['eth0']['Type'] == 'LAN' and
                config['FireWall']['eth0']['INPUT']['LDAP'] != 0):
            os.system('iptables -A FORWARD -i eth0 -p tcp --dport 389 -j ACCEPT')
            # OUTPUT
        if (config['FireWall']['eth0']['OUTPUT']['LDAP'] == 2 or
            config['Interfaces']['eth0']['Type'] == 'LAN' and
            config['FireWall']['eth0']['OUTPUT']['LDAP'] != 0):
            os.system('iptables -A FORWARD -o eth0 -p tcp --dport 389 -j ACCEPT')
    # ----------------------------------------------------------------- #
    # ------------------ CONFIGURATION eth1 --------------------------- #
    # ----------------------------------------------------------------- #
    if config['Interfaces']['eth1']['Firewall'] == 1:

        # Established dans tout les cas on install sauf si on force
        if config['FireWall']['eth1']['INPUT']['Established'] != 0:
            os.system('iptables -A FORWARD -i eth1 -m conntrack --ctstate RELATED,ESTABLISHED -j ACCEPT')
        if config['FireWall']['eth1']['INPUT']['Established'] != 0:
            os.system('iptables -A FORWARD -o eth1 -m conntrack --ctstate RELATED,ESTABLISHED -j ACCEPT')
        # Ping icmp
        if config['FireWall']['eth1']['INPUT']['Ping'] == 2:
            os.system('iptables -A FORWARD -i eth1 -p icmp -j ACCEPT')
        if config['FireWall']['eth1']['OUPUT']['Ping'] == 2:
            os.system('iptables -A FORWARD -o eth1 -p icmp -j ACCEPT')
        # DNS
        # INPUT
        if ((config['FireWall']['eth1']['INPUT']['DNS'] == 2 or
             config['Interfaces']['eth1']['Type'] == 'LAN') and config['FireWall']['eth1']['INPUT']['DNS'] != 0):
            os.system('iptables -A FORWARD -i eth1 -p tcp --dport 53 -j ACCEPT')
            os.system('iptables -A FORWARD -i eth1 -p udp --dport 53 -j ACCEPT')
            # OUTPUT
        if ((config['FireWall']['eth1']['OUTPUT']['DNS'] == 2 or
             config['Interfaces']['eth1']['Type'] == 'LAN' or config['Interfaces']['eth1']['Type'] == 'NET') and
                config['FireWall']['eth1']['OUTPUT']['DNS'] != 0):
            os.system('iptables -A FORWARD -o eth1 -p tcp --dport 53 -j ACCEPT')
            os.system('iptables -A FORWARD -o eth1 -p udp --dport 53 -j ACCEPT')
        # HTTP
        # INPUT
        if ((config['FireWall']['eth1']['INPUT']['HTTP'] == 2 or
             config['Interfaces']['eth1']['Type'] == 'NET' or config['Interfaces']['eth1']['Type'] == 'DMZ') and
                config['FireWall']['eth1']['INPUT']['HTTP'] != 0):
            os.system('iptables -A FORWARD -i eth1 -p tcp --dport 80 -j ACCEPT')
            # OUTPUT
        if ((config['FireWall']['eth1']['OUTPUT']['HTTP'] == 2 or
             config['Interfaces']['eth1']['Type'] == 'LAN' or config['Interfaces']['eth1']['Type'] == 'NET') and
                config['FireWall']['eth1']['OUTPUT']['HTTP'] != 0):
            os.system('iptables -A FORWARD -o eth1 -p tcp --dport 80 -j ACCEPT')
        # HTTPS
        # INPUT
        if ((config['FireWall']['eth1']['INPUT']['HTTPS'] == 2 or
             config['Interfaces']['eth1']['Type'] == 'NET' or config['Interfaces']['eth1']['Type'] == 'DMZ') and
                config['FireWall']['eth1']['INPUT']['HTTPS'] != 0):
            os.system('iptables -A FORWARD -i eth1 -p tcp --dport 443 -j ACCEPT')
            # OUTPUT
        if ((config['FireWall']['eth1']['OUTPUT']['HTTPS'] == 2 or
             config['Interfaces']['eth1']['Type'] == 'LAN' or config['Interfaces']['eth1']['Type'] == 'NET') and
                config['FireWall']['eth1']['OUTPUT']['HTTPS'] != 0):
            os.system('iptables -A FORWARD -o eth1 -p tcp --dport 443 -j ACCEPT')
        # PRINTER
        # INPUT
        if ((config['FireWall']['eth1']['INPUT']['Printer'] == 2 or
             config['Interfaces']['eth1']['Type'] == 'LAN') and
                config['FireWall']['eth1']['INPUT']['Printer'] != 0):
            os.system('iptables -A FORWARD -i eth1 -p tcp --dport 631 -j ACCEPT')
            os.system('iptables -A FORWARD -i eth1 -p udp --dport 631 -j ACCEPT')
            # OUTPUT
        if ((config['FireWall']['eth1']['OUTPUT']['Printer'] == 2 or
             config['Interfaces']['eth1']['Type'] == 'LAN') and
                config['FireWall']['eth1']['OUTPUT']['Printer'] != 0):
            os.system('iptables -A FORWARD -o eth1 -p tcp --dport 631 -j ACCEPT')
            os.system('iptables -A FORWARD -o eth1 -p udp --dport 631 -j ACCEPT')
        # DHCP
        # INPUT
        if ((config['FireWall']['eth1']['INPUT']['DHCP'] == 2 or
             config['Interfaces']['eth1']['Type'] == 'LAN') and
                config['FireWall']['eth1']['INPUT']['DHCP'] != 0):
            os.system('iptables -A FORWARD -i eth1 -p tcp --dport 68 -j ACCEPT')
            os.system('iptables -A FORWARD -i eth1 -p udp --dport 67 -j ACCEPT')
            os.system('iptables -A FORWARD -i eth1 -p udp --dport 68 -j ACCEPT')
            # OUTPUT
        if ((config['FireWall']['eth1']['OUTPUT']['DHCP'] == 2 or
             config['Interfaces']['eth1']['Type'] == 'LAN' or config['Interfaces']['eth1']['Type'] == 'NET') and
                config['FireWall']['eth1']['OUTPUT']['DHCP'] != 0):
            os.system('iptables -A FORWARD -o eth1 -p tcp --dport 68 -j ACCEPT')
            os.system('iptables -A FORWARD -o eth1 -p udp --dport 67 -j ACCEPT')
            os.system('iptables -A FORWARD -o eth1 -p udp --dport 68 -j ACCEPT')
        # FTP
        # INPUT
        if ((config['FireWall']['eth1']['INPUT']['FTP'] == 2 or
             config['Interfaces']['eth1']['Type'] == 'NET' or config['Interfaces']['eth1']['Type'] == 'DMZ') and
                config['FireWall']['eth1']['INPUT']['FTP'] != 0):
            os.system('iptables -A FORWARD -i eth1 -p tcp --dport 20 -j ACCEPT')
            os.system('iptables -A FORWARD -i eth1 -p tcp --dport 21 -j ACCEPT')
            # OUTPUT
        if ((config['FireWall']['eth1']['OUTPUT']['FTP'] == 2 or
             config['Interfaces']['eth1']['Type'] == 'LAN' or config['Interfaces']['eth1']['Type'] == 'NET') and
                config['FireWall']['eth1']['OUTPUT']['FTP'] != 0):
            os.system('iptables -A FORWARD -o eth1 -p tcp --dport 20 -j ACCEPT')
            os.system('iptables -A FORWARD -o eth1 -p tcp --dport 21 -j ACCEPT')
        # SSH
        # INPUT
        if ((config['FireWall']['eth1']['INPUT']['SSH'] == 2 or
             config['Interfaces']['eth1']['Type'] == 'LAN' or config['Interfaces']['eth1']['Type'] == 'DMZ') and
                config['FireWall']['eth1']['INPUT']['SSH'] != 0):
            os.system('iptables -A FORWARD -i eth1 -p tcp --dport 22 -j ACCEPT')
            # OUTPUT
        if ((config['FireWall']['eth1']['OUTPUT']['SSH'] == 2 or
             config['Interfaces']['eth1']['Type'] == 'LAN' or config['Interfaces']['eth1']['Type'] == 'NET') and
                config['FireWall']['eth1']['OUTPUT']['SSH'] != 0):
            os.system('iptables -A FORWARD -o eth1 -p tcp --dport 22 -j ACCEPT')
        # IMAP
        # INPUT
        if config['FireWall']['eth1']['INPUT']['IMAP'] != 0:
            os.system('iptables -A FORWARD -i eth1 -p tcp --dport 143 -j ACCEPT')
            os.system('iptables -A FORWARD -i eth1 -p tcp --dport 220 -j ACCEPT')
            os.system('iptables -A FORWARD -i eth1 -p tcp --dport 993 -j ACCEPT')
            # OUTPUT
        if ((config['FireWall']['eth1']['OUTPUT']['DNS'] == 2 or
             config['Interfaces']['eth1']['Type'] == 'LAN' or config['Interfaces']['eth1']['Type'] == 'NET') and
                config['FireWall']['eth1']['OUTPUT']['DNS'] != 0):
            os.system('iptables -A FORWARD -o eth1 -p tcp --dport 143 -j ACCEPT')
            os.system('iptables -A FORWARD -o eth1 -p tcp --dport 220 -j ACCEPT')
            os.system('iptables -A FORWARD -o eth1 -p tcp --dport 993 -j ACCEPT')
        # SMTP
        # INPUT
        if config['FireWall']['eth1']['INPUT']['SMTP'] != 0:
            os.system('iptables -A FORWARD -i eth1 -p tcp --dport 25 -j ACCEPT')
            os.system('iptables -A FORWARD -i eth1 -p tcp --dport 587 -j ACCEPT')
            os.system('iptables -A FORWARD -i eth1 -p tcp --dport 465 -j ACCEPT')
            # OUTPUT
        if ((config['FireWall']['eth1']['OUTPUT']['SMTP'] == 2 or
             config['Interfaces']['eth1']['Type'] == 'LAN' or config['Interfaces']['eth1']['Type'] == 'NET') and
                config['FireWall']['eth1']['OUTPUT']['SMTP'] != 0):
            os.system('iptables -A FORWARD -o eth1 -p tcp --dport 25 -j ACCEPT')
            os.system('iptables -A FORWARD -o eth1 -p tcp --dport 587 -j ACCEPT')
            os.system('iptables -A FORWARD -o eth1 -p tcp --dport 465 -j ACCEPT')
        # POP3
        # INPUT
        if config['FireWall']['eth1']['INPUT']['POP3'] != 0:
            os.system('iptables -A FORWARD -i eth1 -p tcp --dport 110 -j ACCEPT')
            os.system('iptables -A FORWARD -i eth1 -p tcp --dport 985 -j ACCEPT')
            # OUTPUT
        if ((config['FireWall']['eth1']['OUTPUT']['POP3'] == 2 or
             config['Interfaces']['eth1']['Type'] == 'LAN' or config['Interfaces']['eth1']['Type'] == 'NET') and
                config['FireWall']['eth1']['OUTPUT']['POP3'] != 0):
            os.system('iptables -A FORWARD -o eth1 -p tcp --dport 110 -j ACCEPT')
            os.system('iptables -A FORWARD -o eth1 -p tcp --dport 985 -j ACCEPT')
        # NTP
        # INPUT
        if (config['FireWall']['eth1']['INPUT']['NTP'] == 2 or
                config['Interfaces']['eth1']['Type'] == 'LAN' and
                config['FireWall']['eth1']['INPUT']['NTP'] != 0):
            os.system('iptables -A FORWARD -i eth1 -p udp --dport 123 -j ACCEPT')
            # OUTPUT
        if ((config['FireWall']['eth1']['OUTPUT']['NTP'] == 2 or
             config['Interfaces']['eth1']['Type'] == 'LAN' or config['Interfaces']['eth1']['Type'] == 'NET') and
                config['FireWall']['eth1']['OUTPUT']['NTP'] != 0):
            os.system('iptables -A FORWARD -o eth1 -p udp --dport 123 -j ACCEPT')
        # AVAHI
        # INPUT
        if config['FireWall']['eth1']['INPUT']['Avahi'] == 2:
            os.system('iptables -A FORWARD -i eth1 -p udp --dport 5353 -j ACCEPT')
            # OUTPUT
        if config['FireWall']['eth1']['OUTPUT']['Avahi'] == 2:
            os.system('iptables -A FORWARD -o eth1 -p udp --dport 5353 -j ACCEPT')
        # NETBIOS
        # INPUT
        if (config['FireWall']['eth1']['INPUT']['Netbios'] == 2 or
                config['Interfaces']['eth1']['Type'] == 'LAN' and
                config['FireWall']['eth1']['INPUT']['Netbios'] != 0):
            os.system('iptables -A FORWARD -i eth1 -p tcp --dport 137 -j ACCEPT')
            os.system('iptables -A FORWARD -i eth1 -p tcp --dport 138 -j ACCEPT')
            os.system('iptables -A FORWARD -i eth1 -p tcp --dport 139 -j ACCEPT')
            os.system('iptables -A FORWARD -i eth1 -p tcp --dport 445 -j ACCEPT')
            # OUTPUT
        if (config['FireWall']['eth1']['OUTPUT']['Netbios'] == 2 or
                config['Interfaces']['eth1']['Type'] == 'LAN' and
                config['FireWall']['eth1']['OUTPUT']['Netbios'] != 0):
            os.system('iptables -A FORWARD -o eth1 -p tcp --dport 137 -j ACCEPT')
            os.system('iptables -A FORWARD -o eth1 -p tcp --dport 138 -j ACCEPT')
            os.system('iptables -A FORWARD -o eth1 -p tcp --dport 139 -j ACCEPT')
            os.system('iptables -A FORWARD -o eth1 -p tcp --dport 445 -j ACCEPT')
        # LDAP
        # INPUT
        if (config['FireWall']['eth1']['INPUT']['LDAP'] == 2 or
                config['Interfaces']['eth1']['Type'] == 'LAN' and
                config['FireWall']['eth1']['INPUT']['LDAP'] != 0):
            os.system('iptables -A FORWARD -i eth1 -p tcp --dport 389 -j ACCEPT')
            # OUTPUT
        if (config['FireWall']['eth1']['OUTPUT']['LDAP'] == 2 or
                config['Interfaces']['eth1']['Type'] == 'LAN' and
                config['FireWall']['eth1']['OUTPUT']['LDAP'] != 0):
            os.system('iptables -A FORWARD -o eth1 -p tcp --dport 389 -j ACCEPT')
    # ----------------------------------------------------------------- #
    # ------------------ CONFIGURATION eth2 --------------------------- #
    # ----------------------------------------------------------------- #
    if config['Interfaces']['eth2']['Firewall'] == 1:

        # Established dans tout les cas on install sauf si on force
        if config['FireWall']['eth2']['INPUT']['Established'] != 0:
            os.system('iptables -A FORWARD -i eth2 -m conntrack --ctstate RELATED,ESTABLISHED -j ACCEPT')
        if config['FireWall']['eth2']['INPUT']['Established'] != 0:
            os.system('iptables -A FORWARD -o eth2 -m conntrack --ctstate RELATED,ESTABLISHED -j ACCEPT')
        # Ping icmp
        if config['FireWall']['eth2']['INPUT']['Ping'] == 2:
            os.system('iptables -A FORWARD -i eth2 -p icmp -j ACCEPT')
        if config['FireWall']['eth2']['OUPUT']['Ping'] == 2:
            os.system('iptables -A FORWARD -o eth2 -p icmp -j ACCEPT')
        # DNS
        # INPUT
        if ((config['FireWall']['eth2']['INPUT']['DNS'] == 2 or
             config['Interfaces']['eth2']['Type'] == 'LAN') and config['FireWall']['eth2']['INPUT']['DNS'] != 0):
            os.system('iptables -A FORWARD -i eth2 -p tcp --dport 53 -j ACCEPT')
            os.system('iptables -A FORWARD -i eth2 -p udp --dport 53 -j ACCEPT')
            # OUTPUT
        if ((config['FireWall']['eth2']['OUTPUT']['DNS'] == 2 or
             config['Interfaces']['eth2']['Type'] == 'LAN' or config['Interfaces']['eth2']['Type'] == 'NET') and
                config['FireWall']['eth2']['OUTPUT']['DNS'] != 0):
            os.system('iptables -A FORWARD -o eth2 -p tcp --dport 53 -j ACCEPT')
            os.system('iptables -A FORWARD -o eth2 -p udp --dport 53 -j ACCEPT')
        # HTTP
        # INPUT
        if ((config['FireWall']['eth2']['INPUT']['HTTP'] == 2 or
             config['Interfaces']['eth2']['Type'] == 'NET' or config['Interfaces']['eth2']['Type'] == 'DMZ') and
                config['FireWall']['eth2']['INPUT']['HTTP'] != 0):
            os.system('iptables -A FORWARD -i eth2 -p tcp --dport 80 -j ACCEPT')
            # OUTPUT
        if ((config['FireWall']['eth2']['OUTPUT']['HTTP'] == 2 or
             config['Interfaces']['eth2']['Type'] == 'LAN' or config['Interfaces']['eth2']['Type'] == 'NET') and
                config['FireWall']['eth2']['OUTPUT']['HTTP'] != 0):
            os.system('iptables -A FORWARD -o eth2 -p tcp --dport 80 -j ACCEPT')
        # HTTPS
        # INPUT
        if ((config['FireWall']['eth2']['INPUT']['HTTPS'] == 2 or
             config['Interfaces']['eth2']['Type'] == 'NET' or config['Interfaces']['eth2']['Type'] == 'DMZ') and
                config['FireWall']['eth2']['INPUT']['HTTPS'] != 0):
            os.system('iptables -A FORWARD -i eth2 -p tcp --dport 443 -j ACCEPT')
            # OUTPUT
        if ((config['FireWall']['eth2']['OUTPUT']['HTTPS'] == 2 or
             config['Interfaces']['eth2']['Type'] == 'LAN' or config['Interfaces']['eth2']['Type'] == 'NET') and
                config['FireWall']['eth2']['OUTPUT']['HTTPS'] != 0):
            os.system('iptables -A FORWARD -o eth2 -p tcp --dport 443 -j ACCEPT')
        # PRINTER
        # INPUT
        if ((config['FireWall']['eth2']['INPUT']['Printer'] == 2 or
             config['Interfaces']['eth2']['Type'] == 'LAN') and
                config['FireWall']['eth2']['INPUT']['Printer'] != 0):
            os.system('iptables -A FORWARD -i eth2 -p tcp --dport 631 -j ACCEPT')
            os.system('iptables -A FORWARD -i eth2 -p udp --dport 631 -j ACCEPT')
            # OUTPUT
        if ((config['FireWall']['eth2']['OUTPUT']['Printer'] == 2 or
             config['Interfaces']['eth2']['Type'] == 'LAN') and
                config['FireWall']['eth2']['OUTPUT']['Printer'] != 0):
            os.system('iptables -A FORWARD -o eth2 -p tcp --dport 631 -j ACCEPT')
            os.system('iptables -A FORWARD -o eth2 -p udp --dport 631 -j ACCEPT')
        # DHCP
        # INPUT
        if ((config['FireWall']['eth2']['INPUT']['DHCP'] == 2 or
             config['Interfaces']['eth2']['Type'] == 'LAN') and
                config['FireWall']['eth2']['INPUT']['DHCP'] != 0):
            os.system('iptables -A FORWARD -i eth2 -p tcp --dport 68 -j ACCEPT')
            os.system('iptables -A FORWARD -i eth2 -p udp --dport 67 -j ACCEPT')
            os.system('iptables -A FORWARD -i eth2 -p udp --dport 68 -j ACCEPT')
            # OUTPUT
        if ((config['FireWall']['eth2']['OUTPUT']['DHCP'] == 2 or
             config['Interfaces']['eth2']['Type'] == 'LAN' or config['Interfaces']['eth2']['Type'] == 'NET') and
                config['FireWall']['eth2']['OUTPUT']['DHCP'] != 0):
            os.system('iptables -A FORWARD -o eth2 -p tcp --dport 68 -j ACCEPT')
            os.system('iptables -A FORWARD -o eth2 -p udp --dport 67 -j ACCEPT')
            os.system('iptables -A FORWARD -o eth2 -p udp --dport 68 -j ACCEPT')
        # FTP
        # INPUT
        if ((config['FireWall']['eth2']['INPUT']['FTP'] == 2 or
             config['Interfaces']['eth2']['Type'] == 'NET' or config['Interfaces']['eth2']['Type'] == 'DMZ') and
                config['FireWall']['eth2']['INPUT']['FTP'] != 0):
            os.system('iptables -A FORWARD -i eth2 -p tcp --dport 20 -j ACCEPT')
            os.system('iptables -A FORWARD -i eth2 -p tcp --dport 21 -j ACCEPT')
            # OUTPUT
        if ((config['FireWall']['eth2']['OUTPUT']['FTP'] == 2 or
             config['Interfaces']['eth2']['Type'] == 'LAN' or config['Interfaces']['eth2']['Type'] == 'NET') and
                config['FireWall']['eth2']['OUTPUT']['FTP'] != 0):
            os.system('iptables -A FORWARD -o eth2 -p tcp --dport 20 -j ACCEPT')
            os.system('iptables -A FORWARD -o eth2 -p tcp --dport 21 -j ACCEPT')
        # SSH
        # INPUT
        if ((config['FireWall']['eth2']['INPUT']['SSH'] == 2 or
             config['Interfaces']['eth2']['Type'] == 'LAN' or config['Interfaces']['eth2']['Type'] == 'DMZ') and
                config['FireWall']['eth2']['INPUT']['SSH'] != 0):
            os.system('iptables -A FORWARD -i eth2 -p tcp --dport 22 -j ACCEPT')
            # OUTPUT
        if ((config['FireWall']['eth2']['OUTPUT']['SSH'] == 2 or
             config['Interfaces']['eth2']['Type'] == 'LAN' or config['Interfaces']['eth2']['Type'] == 'NET') and
                config['FireWall']['eth2']['OUTPUT']['SSH'] != 0):
            os.system('iptables -A FORWARD -o eth2 -p tcp --dport 22 -j ACCEPT')
        # IMAP
        # INPUT
        if config['FireWall']['eth2']['INPUT']['IMAP'] != 0:
            os.system('iptables -A FORWARD -i eth2 -p tcp --dport 143 -j ACCEPT')
            os.system('iptables -A FORWARD -i eth2 -p tcp --dport 220 -j ACCEPT')
            os.system('iptables -A FORWARD -i eth2 -p tcp --dport 993 -j ACCEPT')
            # OUTPUT
        if ((config['FireWall']['eth2']['OUTPUT']['DNS'] == 2 or
             config['Interfaces']['eth2']['Type'] == 'LAN' or config['Interfaces']['eth2']['Type'] == 'NET') and
                config['FireWall']['eth2']['OUTPUT']['DNS'] != 0):
            os.system('iptables -A FORWARD -o eth2 -p tcp --dport 143 -j ACCEPT')
            os.system('iptables -A FORWARD -o eth2 -p tcp --dport 220 -j ACCEPT')
            os.system('iptables -A FORWARD -o eth2 -p tcp --dport 993 -j ACCEPT')
        # SMTP
        # INPUT
        if config['FireWall']['eth2']['INPUT']['SMTP'] != 0:
            os.system('iptables -A FORWARD -i eth2 -p tcp --dport 25 -j ACCEPT')
            os.system('iptables -A FORWARD -i eth2 -p tcp --dport 587 -j ACCEPT')
            os.system('iptables -A FORWARD -i eth2 -p tcp --dport 465 -j ACCEPT')
            # OUTPUT
        if ((config['FireWall']['eth2']['OUTPUT']['SMTP'] == 2 or
             config['Interfaces']['eth2']['Type'] == 'LAN' or config['Interfaces']['eth2']['Type'] == 'NET') and
                config['FireWall']['eth2']['OUTPUT']['SMTP'] != 0):
            os.system('iptables -A FORWARD -o eth2 -p tcp --dport 25 -j ACCEPT')
            os.system('iptables -A FORWARD -o eth2 -p tcp --dport 587 -j ACCEPT')
            os.system('iptables -A FORWARD -o eth2 -p tcp --dport 465 -j ACCEPT')
        # POP3
        # INPUT
        if config['FireWall']['eth2']['INPUT']['POP3'] != 0:
            os.system('iptables -A FORWARD -i eth2 -p tcp --dport 110 -j ACCEPT')
            os.system('iptables -A FORWARD -i eth2 -p tcp --dport 985 -j ACCEPT')
            # OUTPUT
        if ((config['FireWall']['eth2']['OUTPUT']['POP3'] == 2 or
             config['Interfaces']['eth2']['Type'] == 'LAN' or config['Interfaces']['eth2']['Type'] == 'NET') and
                config['FireWall']['eth2']['OUTPUT']['POP3'] != 0):
            os.system('iptables -A FORWARD -o eth2 -p tcp --dport 110 -j ACCEPT')
            os.system('iptables -A FORWARD -o eth2 -p tcp --dport 985 -j ACCEPT')
        # NTP
        # INPUT
        if (config['FireWall']['eth2']['INPUT']['NTP'] == 2 or
                config['Interfaces']['eth2']['Type'] == 'LAN' and
                config['FireWall']['eth2']['INPUT']['NTP'] != 0):
            os.system('iptables -A FORWARD -i eth2 -p udp --dport 123 -j ACCEPT')
            # OUTPUT
        if ((config['FireWall']['eth2']['OUTPUT']['NTP'] == 2 or
             config['Interfaces']['eth2']['Type'] == 'LAN' or config['Interfaces']['eth2']['Type'] == 'NET') and
                config['FireWall']['eth2']['OUTPUT']['NTP'] != 0):
            os.system('iptables -A FORWARD -o eth2 -p udp --dport 123 -j ACCEPT')
        # AVAHI
        # INPUT
        if config['FireWall']['eth2']['INPUT']['Avahi'] == 2:
            os.system('iptables -A FORWARD -i eth2 -p udp --dport 5353 -j ACCEPT')
            # OUTPUT
        if config['FireWall']['eth2']['OUTPUT']['Avahi'] == 2:
            os.system('iptables -A FORWARD -o eth2 -p udp --dport 5353 -j ACCEPT')
        # NETBIOS
        # INPUT
        if (config['FireWall']['eth2']['INPUT']['Netbios'] == 2 or
                config['Interfaces']['eth2']['Type'] == 'LAN' and
                config['FireWall']['eth2']['INPUT']['Netbios'] != 0):
            os.system('iptables -A FORWARD -i eth2 -p tcp --dport 137 -j ACCEPT')
            os.system('iptables -A FORWARD -i eth2 -p tcp --dport 138 -j ACCEPT')
            os.system('iptables -A FORWARD -i eth2 -p tcp --dport 139 -j ACCEPT')
            os.system('iptables -A FORWARD -i eth2 -p tcp --dport 445 -j ACCEPT')
            # OUTPUT
        if (config['FireWall']['eth2']['OUTPUT']['Netbios'] == 2 or
                config['Interfaces']['eth2']['Type'] == 'LAN' and
                config['FireWall']['eth2']['OUTPUT']['Netbios'] != 0):
            os.system('iptables -A FORWARD -o eth2 -p tcp --dport 137 -j ACCEPT')
            os.system('iptables -A FORWARD -o eth2 -p tcp --dport 138 -j ACCEPT')
            os.system('iptables -A FORWARD -o eth2 -p tcp --dport 139 -j ACCEPT')
            os.system('iptables -A FORWARD -o eth2 -p tcp --dport 445 -j ACCEPT')
        # LDAP
        # INPUT
        if (config['FireWall']['eth2']['INPUT']['LDAP'] == 2 or
                config['Interfaces']['eth2']['Type'] == 'LAN' and
                config['FireWall']['eth2']['INPUT']['LDAP'] != 0):
            os.system('iptables -A FORWARD -i eth2 -p tcp --dport 389 -j ACCEPT')
            # OUTPUT
        if (config['FireWall']['eth2']['OUTPUT']['LDAP'] == 2 or
                config['Interfaces']['eth2']['Type'] == 'LAN' and
                config['FireWall']['eth2']['OUTPUT']['LDAP'] != 0):
            os.system('iptables -A FORWARD -o eth2 -p tcp --dport 389 -j ACCEPT')
    # ----------------------------------------------------------------- #
    # -----------------FIN DE LA CONFIG PARE-FEU----------------------- #
    # ----------------------------------------------------------------- #
    print('done.\n')

# -------------------------------------- Configuration NAT -------------------------------- #

if args.nat:
    print('NAT configuration...\n')
    if config['Interfaces']['eth0']['Type'] == 'NET':
        os.system('iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE')
    if config['Interfaces']['eth1']['Type'] == 'NET':
        os.system('iptables -t nat -A POSTROUTING -o eth1 -j MASQUERADE')
    if config['Interfaces']['eth2']['Type'] == 'NET':
        os.system('iptables -t nat -A POSTROUTING -o eth2 -j MASQUERADE')
    print('done.\n')

# ------------------------------- Installation Iptables-persistent ------------------------ #

if args.nat or (args.firewall and not (config['Interfaces']['eth0']['Firewall'] == 0 and
                          config['Interfaces']['eth1']['Firewall'] == 0 and
                          config['Interfaces']['eth2']['Firewall'] == 0)):
    print('Iptables-persistent setup...\n')
# Ici on utilise une nouvelle fonction d'installation car iptables-persistent ne suporte pas le assume-yes (-y)
# on doit donc générer deux variable pour le système avant de lancer l'installation.
    def iptables_install():
        """setup iptables-persistent with "assume yes" on linux distribution which have aperture,
        two sys.var are added before launching the setup for disabling the windows display during the settup"""

        os.system('echo iptables-persistent iptables-persistent/autosave_v4 boolean true | debconf-set-selections')
        os.system('echo iptables-persistent iptables-persistent/autosave_v6 boolean true | debconf-set-selections')
        with open('freshup.log', 'a') as freshlog:
            freshlog.write('Ssh setp :\n\n\n')
            subprocess.Popen("apt-get install -y iptables-persistent", shell=True, stdout=freshlog, stderr=freshlog)

    def main():  # Attente de la fin d'installation mis en thread par la fonction main
        thread = threading.Thread(target=iptables_install)
        thread.start()
        thread.join()
    if __name__ == '__main__':
        main()
    print('done.\n')

# ----------------------------------- Activation du routage ------------------------------- #

if args.route:
    sysctl = open('/etc/sysctl.conf', 'r')
    if ('#net.ipv4.ip_forward=1' or '# net.ipv4.ip_forward=1') in sysctl:
        if '# net.ipv4.ip_forward=1' in sysctl:
            remplacement('/etc/sysctl.conf', '# net.ipv4.ip_forward=1', 'net.ipv4.ip_forward=1')
            sysctl.close()
        elif '#net.ipv4.ip_forward=1' in sysctl:
            remplacement('/etc/sysctl.conf', '#net.ipv4.ip_forward=1', 'net.ipv4.ip_forward=1')
            sysctl.close()
    elif 'net.ipv4.ip_forward=1' in sysctl:
        print('Sysctl.conf already configured for forwarding')
        sysctl.close()
    else:
        print('No line with ipv4 forwarding configuration found in sysctl.conf : '
              'adding a new line at the end of the file')
        sysctl = open("/etc/sysctl.conf", "a")
        sysctl.write('\nnet.ipv4.ip_forward=1\n')
        sysctl.close()
    os.system('sysctl -p /etc/sysctl.conf')
    print("Forwarding enable")

# --------------------------------- Configuration des interfaces -------------------------- #

if args.interfaces:
    print('Renaming in ethx...')
    remplacement('/etc/default/grub', 'GRUB_CMDLINE_LINUX=""', 'GRUB_CMDLINE_LINUX="net.ifnames=0 biosdevname=0"')
    print('Interfaces configuration...')
    # Ouverture et ecriture (erase) du fichier de conf
    interfaces = open("/etc/network/interfaces", "w")
    # Insertion de la conf de base
    interfaces.write("source /etc/network/interfaces.d/*\n\n#loopback iface\nauto lo\niface lo inet loopback\n\n")
    # Insertion de la conf de eth0
    if config['Interfaces']['eth0']['Activated'] == 1:
        interfaces.write("#Iface 1\nauto eth0\niface eth0 inet static\naddress {}\nnetmask {}\ngateway {}\n\n"
                         .format(config['Interfaces']['eth0']['IP'], config['Interfaces']['eth0']['NetMask'],
                                 config['Interfaces']['eth0']['GateWay']))
    # Insertion de la conf de eth1
    if config['Interfaces']['eth1']['Activated'] == 1:
        interfaces.write("#Iface 2\nauto eth1\niface eth1 inet static\naddress {}\nnetmask {}\ngateway {}\n\n"
                         .format(config['Interfaces']['eth1']['IP'], config['Interfaces']['eth1']['NetMask'],
                                 config['Interfaces']['eth1']['GateWay']))
    # Insertion de la conf de eth0
    if config['Interfaces']['eth2']['Activated'] == 1:
        interfaces.write("#Iface 3\nauto eth2\niface eth2 inet static\naddress {}\nnetmask {}\ngateway {}\n\n"
                         .format(config['Interfaces']['eth2']['IP'], config['Interfaces']['eth3']['NetMask'],
                                 config['Interfaces']['eth2']['GateWay']))
    # Fermeture du fichier
    interfaces.close()
    # --- Configuration interface terminée --- #
    print('done.\n')

# -------------------------------- Redémmarage ------------------------------- #
print('Thank you for using Fresh-up on your server !\nMerci d\'avoir utilisé Fresh-up sur votre serveur !\n')
print('Votre serveur va redémarer dans :')
i = 4
while i > 1:
    i = i - 1
    print(i)
    time.sleep(1)
os.system('init 6')
sys.exit(0)

# ---------------------------------- |||||||||||||||||| ----------------------------------- #
# ---------------------------------- |FIN DU PROGRAMME| ----------------------------------- #
# ---------------------------------- |||||||||||||||||| ----------------------------------- #
