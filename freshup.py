#!/usr/bin/python3.5
# -*-coding:utf-8 -*

# -------------------------------- Module | Conf.ini | Options ---------------------------- #

import argparse  # Importation argparse pour les options
import os  # Importation commandes bash de l'os
import threading  # Importation du module pour faire du thread
import sys  # Importation des commandes sys essentiels
import subprocess  # Importation du module subprocess
import json  # Importation de la configuration

# Création du dictionnaire de config :
data = open('conf.json', 'r')
config = json.load(data)
data.close()
# Création du dictionaire des types
data2 = open('type.json', 'r')
iftype = json.load(data2)
data2.close()

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


# ------------------------------------ Vérifiations Distribution -------------------------------- #

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
    if config['Interfaces']['eth0']['Firewall'] == 1:
        if config['FIREWALL1']['EST'] == '1':
            # Connections déjà établies
            os.system('iptables -A INPUT -i enp0s3 -m conntrack --ctstate RELATED,ESTABLISHED -j ACCEPT')
            os.system('iptables -A OUTPUT -m conntrack --ctstate RELATED,ESTABLISHED -j ACCEPT')
            os.system('iptables -A FORWARD -i enp0s3  -o enp0s3 -m conntrack --ctstate RELATED,ESTABLISHED -j ACCEPT')
        if config['FIREWALL1']['PING'] == '1':
            # Ping : icmp
            os.system('iptables -A INPUT -i enp0s3 -p icmp -j ACCEPT')
            os.system('iptables -A OUTPUT -o enp0s3 -p icmp -j ACCEPT')
            os.system('iptables -A FORWARD -i enp0s3 -o enp0s3 -p icmp -j ACCEPT')
        if config['FIREWALL1']['DNS'] == '1':
            # DNS : udp 53
            os.system('iptables -A INPUT -i enp0s3 -p udp --dport 53 -j ACCEPT')
            os.system('iptables -A OUTPUT -o enp0s3 -p udp --dport 53 -j ACCEPT')
            os.system('iptables -A FORWARD -i enp0s3 -o enp0s3 -p udp --dport 53 -j ACCEPT')
        if config['FIREWALL1']['HTTP'] == '1':
            # HTTP : tcp 80
            os.system('iptables -A INPUT -i enp0s3 -p tcp --dport 80 -j ACCEPT')
            os.system('iptables -A OUTPUT -o enp0s3 -p tcp --dport 80 -j ACCEPT')
            os.system('iptables -A FORWARD -i enp0s3 -o enp0s3 -p tcp --dport 80 -j ACCEPT')
        if config['FIREWALL1']['HTTPS'] == '1':
            # HTTPS : tcp 443
            os.system('iptables -A INPUT -i enp0s3 -p tcp --dport 443 -j ACCEPT')
            os.system('iptables -A OUTPUT -o enp0s3 -p tcp --dport 443 -j ACCEPT')
            os.system('iptables -A FORWARD -i enp0s3 -o enp0s3 -p tcp --dport 443 -j ACCEPT')
    # ----------------------------------------------------------------- #
    # ----------------------------------------------------------------- #
    if config['Interfaces']['eth1']['Firewall'] == 1:
        if config['FIREWALL2']['EST'] == '1':
            # Connections déjà établies
            os.system('iptables -A INPUT -i enp0s8 -m conntrack --ctstate RELATED,ESTABLISHED -j ACCEPT')
            os.system('iptables -A OUTPUT -o enp0s8 -m conntrack --ctstate RELATED,ESTABLISHED -j ACCEPT')
            os.system('iptables -A FORWARD -i enp0s8 -o enp0s8 -m conntrack --ctstate RELATED,ESTABLISHED -j ACCEPT')
        if config['FIREWALL2']['PING'] == '1':
            # Ping : icmp
            os.system('iptables -A INPUT -i enp0s8 -p icmp -j ACCEPT')
            os.system('iptables -A OUTPUT -o enp0s8 -p icmp -j ACCEPT')
            os.system('iptables -A FORWARD -i enp0s8 -o enp0s8 -p icmp -j ACCEPT')
        if config['FIREWALL2']['DNS'] == '1':
            # DNS : udp 53
            os.system('iptables -A INPUT -i enp0s8 -p udp --dport 53 -j ACCEPT')
            os.system('iptables -A OUTPUT -o enp0s8 -p udp --dport 53 -j ACCEPT')
            os.system('iptables -A FORWARD -i enp0s8 -o enp0s8 -p udp --dport 53 -j ACCEPT')
        if config['FIREWALL2']['HTTP'] == '1':
            # HTTP : tcp 80
            os.system('iptables -A INPUT -i enp0s8 -p tcp --dport 80 -j ACCEPT')
            os.system('iptables -A OUTPUT -o enp0s8 -p tcp --dport 80 -j ACCEPT')
            os.system('iptables -A FORWARD -i enp0s8 -o enp0s8 -p tcp --dport 80 -j ACCEPT')
        if config['FIREWALL2']['HTTPS'] == '1':
            # HTTPS : tcp 443
            os.system('iptables -A INPUT -i enp0s8 -p tcp --dport 443 -j ACCEPT')
            os.system('iptables -A OUTPUT -o enp0s8 -p tcp --dport 443 -j ACCEPT')
            os.system('iptables -A FORWARD -i enp0s8 -o enp0s8 -p tcp --dport 443 -j ACCEPT')
    # ----------------------------------------------------------------- #
    # ----------------------------------------------------------------- #
    if config['Interfaces']['eth2']['Firewall'] == 1:
        if config['FIREWALL3']['EST'] == '1':
            # Connections déjà établies
            os.system('iptables -A INPUT -i enp0s9 -m conntrack --ctstate RELATED,ESTABLISHED -j ACCEPT')
            os.system('iptables -A OUTPUT -o enp0s9 -m conntrack --ctstate RELATED,ESTABLISHED -j ACCEPT')
            os.system('iptables -A FORWARD -i enp0s9 -o enp0s9 -m conntrack --ctstate RELATED,ESTABLISHED -j ACCEPT')
        if config['FIREWALL3']['PING'] == '1':
            # Ping : icmp
            os.system('iptables -A INPUT -i enp0s9 -p icmp -j ACCEPT')
            os.system('iptables -A OUTPUT -o enp0s9 -p icmp -j ACCEPT')
            os.system('iptables -A FORWARD -i enp0s9 -o enp0s9 -p icmp -j ACCEPT')
        if config['FIREWALL3']['DNS'] == '1':
            # DNS : udp 53
            os.system('iptables -A INPUT -i enp0s9 -p udp --dport 53 -j ACCEPT')
            os.system('iptables -A OUTPUT -o enp0s9 -p udp --dport 53 -j ACCEPT')
            os.system('iptables -A FORWARD -i enp0s9 -o enp0s9 -p udp --dport 53 -j ACCEPT')
        if config['FIREWALL3']['HTTP'] == '1':
            # HTTP : tcp 80
            os.system('iptables -A INPUT -i enp0s9 -p tcp --dport 80 -j ACCEPT')
            os.system('iptables -A OUTPUT -o enp0s9 -p tcp --dport 80 -j ACCEPT')
            os.system('iptables -A FORWARD -i enp0s9 -o enp0s9 -p tcp --dport 80 -j ACCEPT')
        if config['FIREWALL3']['HTTPS'] == '1':
            # HTTPS : tcp 443
            os.system('iptables -A INPUT -i enp0s9 -p tcp --dport 443 -j ACCEPT')
            os.system('iptables -A OUTPUT -o enp0s9 -p tcp --dport 443 -j ACCEPT')
            os.system('iptables -A FORWARD -i enp0s9 -o enp0s9 -p tcp --dport 443 -j ACCEPT')
    # ----------------------------------------------------------------- #
    # FIN DE LA CONFIG PARE-FEU
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
if args.nat or args.firewall:
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

# -------------------------------- Redémmarage des services ------------------------------- #
print('Thank you for using Fresh-up on your server !\nMerci d\'avoir utilisé Fresh-up sur votre serveur !\n')
os.system('init 6')
sys.exit(0)

# ---------------------------------- |||||||||||||||||| ----------------------------------- #
# ---------------------------------- |FIN DU PROGRAMME| ----------------------------------- #
# ---------------------------------- |||||||||||||||||| ----------------------------------- #
