#!/usr/bin/python3.5
# -*-coding:utf-8 -*

# -------------------------------- Module | Conf.ini | Options ---------------------------- #

import argparse  # Importation argparse pour les options
import os  # Importation commandes bash de l'os
import configparser  # Importation de la configuration et le module argument
import threading  # Importation du module pour faire du thread
import sys  # Importation des commandes sys essentiels
import subprocess  # Importation du module subprocess

# Création des argument options :
print("Initialisation...")
config = configparser.ConfigParser()
parser = argparse.ArgumentParser()
parser.add_argument("-d", "--dhcp", help="DHCP : will not ne installed", action="store_false")
parser.add_argument("-f", "--firewall", help="FIREWALL : will not be installed", action="store_false")
parser.add_argument("-i", "--interfaces", help="INTERFACES : will not be configured", action="store_false")
parser.add_argument("-n", "--nat", help="NAT : will not be configured", action="store_false")
parser.add_argument("-r", "--restart", help="Sytème will be reboot at the end of FRESHUP", action="store_false")
parser.add_argument("-t", "--tools", help="Net-tools dnsUtils tcp-dump and SSH: will be not installed",
                    action="store_false")
parser.add_argument("-F", "--force", help="Force the installation on other distribution BE CAREFUL",
                    action="store_false")
args = parser.parse_args()

# On récupère nos variables du fichier .ini
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

# ---------------------------- Vérifions que nous sommes sur Debian ----------------------- #

if args.force:
    print('Verification...')
    # On lance un sousprocess via popen et on redirige stdout dans child pour avoir le exit statut
    # Ici uname -a donne la version complète et grep chercher la présence du mot Débian
    child = subprocess.Popen("uname -a | grep Debian", shell=True, stdout=subprocess.PIPE)
    streamdata = child.communicate()[0]
    rc = child.returncode
    if child.returncode != 0:  # Si exit status de grep Debian n'est pas bon on quitte
        print('Vous n\'êtes pas sur une distribution Debian\nYour are not on a Debian Distribution\n')
        sys.exit()
    # Vérification OK --> C'est partit !
    print('done.\n')

# ------------------------------------ Installation des outils ---------------------------- #

if args.tools:
    print('Tools setup...\n')
    # ------------------------------------------------------------------ #

    def ssh_install():
        """Setup openssh-server on linux distribution which have aperture"""
        os.system('apt-get install -y openssh-server > /dev/null')
        print('Ssh setup...')

    def main():  # Mise en thread et attente du thread dans def main
        thread = threading.Thread(target=ssh_install)
        thread.start()
        thread.join()
    if __name__ == '__main__':
        main()
    # ------------------------------------------------------------------ #

    def nettools_install():
        """Setup net-tools on linux distribution which have aperture"""
        os.system('apt-get install -qq -y net-tools > /dev/null')
        print('Net-tools setup...')

    def main():  # Mise en thread et attente du thread dans def main
        thread = threading.Thread(target=nettools_install)
        thread.start()
        thread.join()
    if __name__ == '__main__':
        main()
    # ------------------------------------------------------------------ #

    def dnsutils_install():
        """Setup dnsutils on linux distribution which have aperture"""
        os.system('apt-get install -qq -y dnsutils > /dev/null')
        print('Dns-utils setup...')

    def main():  # Mise en thread et attente du thread dans def main
        thread = threading.Thread(target=dnsutils_install)
        thread.start()
        thread.join()
    if __name__ == '__main__':
        main()
    # ----------------------------------------------------------------- #

    def tcpdump_install():
        """Setup tcpdump on linux distribution which have aperture"""
        os.system('apt-get install -qq -y tcpdump > /dev/null')
        print('TcpDump setup...')

    def main():  # Mise en thread et attente du thread dans def main
        thread = threading.Thread(target=tcpdump_install)
        thread.start()
        thread.join()
    if __name__ == '__main__':
        main()
    # ----------------------------------------------------------------- #
    print('done.\n')

# --------------------------- Setup & Configuration du serveur DHCP ----------------------- #

if args.dhcp:
    print('DHCP-server setup...\n')

    def dhcp_install():
        """Setup isc-dhcp-server on linux distribution which have aperture"""
        os.system('apt-get install -qq -y isc-dhcp-server > /dev/null')

    def main():  # Mise en thread et attente du thread dans def main
        thread = threading.Thread(target=dhcp_install)
        thread.start()
        thread.join()
    if __name__ == '__main__':
        main()

    # Configuration de dhcpd.conf
    dhcpd = open("/etc/dhcp/dhcpd.conf", "a")
    dhcpd.write('\nautoritative;\n\n')
    if DHCP1 == '1':
        dhcpd.write("subnet {} netmask {} {{\n  range {} {};\n  option routers {};\n}}\n\n"
                    .format(DHSUB1, DHNM1, ST1, END1, IP1))
    if DHCP2 == '1':
        dhcpd.write("subnet {} netmask {} {{\n  range {} {};\n  option routers {};\n}}\n\n"
                    .format(DHSUB2, DHNM2, ST2, END2, IP2))
    if DHCP3 == '1':
        dhcpd.write("subnet {} netmask {} {{\n  range {} {};\n  option routers {};\n}}\n\n"
                    .format(DHSUB3, DHNM3, ST3, END3, IP3))
    dhcpd.close()
    iscdhcpd = open("/etc/default/isc-dhcp-server", "w")  # Config de l'écoute en fnct des paramètres
    if DHCP1 == '1' and DHCP2 == '0' and DHCP3 == '0':
        iscdhcpd.write('INTERFACESv4="enp0s3"\nINTERFACESv6=""\n')
    if DHCP1 == '0' and DHCP2 == '1' and DHCP3 == '0':
        iscdhcpd.write('INTERFACESv4="enp0s8"\nINTERFACESv6=""\n')
    if DHCP1 == '0' and DHCP2 == '0' and DHCP3 == '1':
        iscdhcpd.write('INTERFACESv4="enp0s9"\nINTERFACESv6=""\n')
    if DHCP1 == '1' and DHCP2 == '1' and DHCP3 == '0':
        iscdhcpd.write('INTERFACESv4="enp0s3 enp0s8"\nINTERFACESv6=""\n')
    if DHCP1 == '1' and DHCP2 == '0' and DHCP3 == '1':
        iscdhcpd.write('INTERFACESv4="enp0s3 enp0s9"\nINTERFACESv6=""\n')
    if DHCP1 == '0' and DHCP2 == '1' and DHCP3 == '1':
        iscdhcpd.write('INTERFACESv4="enp0s8 enp0s9"\nINTERFACESv6=""\n')
    if DHCP1 == '1' and DHCP2 == '1' and DHCP3 == '1':
        iscdhcpd.write('INTERFACESv4="enp0s3 enp0s8 enp0s9"\nINTERFACESv6=""\n')
    print('done.\n')

# ------------------------------------ Configuration FIREWALL ----------------------------- #

if args.firewall:
    print('Firewall configuration ...\n')
    # On met en DROP toutes les policy ipv4 et ipv6cd
    os.system('iptables -P INPUT DROP')
    os.system('iptables -P OUTPUT DROP')
    os.system('iptables -P FORWARD DROP')
    os.system('ip6tables -P INPUT DROP')
    os.system('ip6tables -P OUTPUT DROP')
    os.system('ip6tables -P FORWARD DROP')
    # On autorise en IPv4
    if FWE == '1':
        # Connections déjà établies
        os.system('iptables -A INPUT -m conntrack --ctstate RELATED,ESTABLISHED -j ACCEPT')
        os.system('iptables -A OUTPUT -m conntrack --ctstate RELATED,ESTABLISHED -j ACCEPT')
        os.system('iptables -A FORWARD -m conntrack --ctstate RELATED,ESTABLISHED -j ACCEPT')
    if FWP == '1':
        # Ping : icmp
        os.system('iptables -A INPUT -p icmp -j ACCEPT')
        os.system('iptables -A OUTPUT -p icmp -j ACCEPT')
        os.system('iptables -A FORWARD -p icmp -j ACCEPT')
    if FWD == '1':
        # DNS : udp 53
        os.system('iptables -A INPUT -p udp --dport 53 -j ACCEPT')
        os.system('iptables -A OUTPUT -p udp --dport 53 -j ACCEPT')
        os.system('iptables -A FORWARD -p udp --dport 53 -j ACCEPT')
    if FWH == '1':
        # HTTP : tcp 80
        os.system('iptables -A INPUT -p tcp --dport 80 -j ACCEPT')
        os.system('iptables -A OUTPUT -p tcp --dport 80 -j ACCEPT')
        os.system('iptables -A FORWARD -p tcp --dport 80 -j ACCEPT')
    if FWS == '1':
        # HTTPS : tcp 443
        os.system('iptables -A INPUT -p tcp --dport 443 -j ACCEPT')
        os.system('iptables -A OUTPUT -p tcp --dport 443 -j ACCEPT')
        os.system('iptables -A FORWARD -p tcp --dport 443 -j ACCEPT')
    # FIN DE LA CONFIG PARE-FEU
    print('done.\n')

# -------------------------------------- Configuration NAT -------------------------------- #

if args.nat:
    print('NAT configuration...\n')
    if NAT1 == '1':
        os.system('iptables -t nat -A POSTROUTING -o enp0s3 -j MASQUERADE')
    if NAT2 == '1':
        os.system('iptables -t nat -A POSTROUTING -o enp0s8 -j MASQUERADE')
    if NAT3 == '1':
        os.system('iptables -t nat -A POSTROUTING -o enp0s9 -j MASQUERADE')
    print('done.\n')

# ------------------------------- Installation Iptables-persistent ------------------------ #

if args.nat or args.firewall:
    print('Iptables-persistent setup...\n')

    def iptables_install():
        """Setup iptable-persistent with assume yes on linux distribution which have aperture"""
        os.system('echo iptables-persistent iptables-persistent/autosave_v4 boolean true | debconf-set-selections')
        os.system('echo iptables-persistent iptables-persistent/autosave_v6 boolean true | debconf-set-selections')
        os.system('apt-get install -qq -y iptables-persistent > /dev/null')

    def main():  # Attente de la fin d'installation mis en thread par la fonction main
        thread = threading.Thread(target=iptables_install)
        thread.start()
        thread.join()
    if __name__ == '__main__':
        main()
    print('done.\n')

# ----------------------------------- Activation du routage ------------------------------- #

sysctl = open("/etc/sysctl.conf", "a")
sysctl.write('\nnet.ipv4.ip_forward=1\n')
sysctl.close()
os.system('sysctl -p /etc/sysctl.conf')
print("Forwarding enable")

# --------------------------------- Configuration des interfaces -------------------------- #

if args.interfaces:
    print('Interfaces configuration...')
    # Ouverture et ecriture (erase) du fichier de conf
    interfaces = open("/etc/network/interfaces", "w")
    # Insertion de la conf de base
    interfaces.write("source /etc/network/interfaces.d/*\n\n#loopback iface\nauto lo\niface lo inet loopback\n\n")
    # Insertion de la conf de l'iface 1
    interfaces.write("#Iface 1\nauto enp0s3\niface enp0s3 inet static\naddress {}\nnetmask {}\ngateway {}\n\n"
                     .format(IP1, NM1, GW1))
    # Insertion de la conf de l'iface 2
    interfaces.write("#Iface 2\nauto enp0s8\niface enp0s8 inet static\naddress {}\nnetmask {}\ngateway {}\n\n"
                     .format(IP2, NM2, GW2))
    # Insertion de la conf de l'iface 3
    interfaces.write("#Iface 3\nauto enp0s9\niface enp0s9 inet static\naddress {}\nnetmask {}\ngateway {}\n\n"
                     .format(IP3, NM3, GW3))
    # Fermeture du fichier
    interfaces.close()
    # --- Configuration interface terminée --- #
    print('done.\n')

# -------------------------------- Redémmarage des services ------------------------------- #

# Si on ne force pas le reboot alors on relance les services qui ont été modifiés
if args.restart:
    # ----------------------------------------------------------------------- #
    if args.interfaces:
        def network_restart():
            """Restart the network interfaces on Debian"""
            os.system('/etc/init.d/networking restart')

        def main():  # Attente fin restart mis en thread par la fonction main
            thread = threading.Thread(target=network_restart)
            thread.start()
            thread.join()
        if __name__ == '__main__':
            main()
    # ----------------------------------------------------------------------- #
    if args.dhcp:
        def dhcp_restart():
            """Restart the isc-dhcp-serveur"""
            os.system('/etc/init.d/isc-dhcp-server restart')

        def main():  # Attente de la fin du restart mis en thread par la fonction main
            thread = threading.Thread(target=dhcp_restart)
            thread.start()
            thread.join()
        if __name__ == '__main__':
            main()
    # ----------------------------------------------------------------------- #
# Si on reboot (-r) alors on ne relance pas les services.
if not args.restart:
    os.system('init 6')
print('Thank you for using Fresh-up on your server !\nMerci d\'avoir utilisé Fresh-up sur votre serveur !\n')

# ---------------------------------- |||||||||||||||||| ----------------------------------- #
# ---------------------------------- |FIN DU PROGRAMME| ----------------------------------- #
# ---------------------------------- |||||||||||||||||| ----------------------------------- #
