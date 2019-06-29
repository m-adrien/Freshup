#!/usr/bin/python3.5
# -*-coding:utf-8 -*

# -------------------------------- Module | Conf.ini | Options ---------------------------- #

import argparse  # Importation argparse pour les options
import os  # Importation commandes bash de l'os
import configparser  # Importation de la configuration et le module argument
import threading  # Importation du module pour faire du thread
import sys  # Importation des commandes sys essentiels
import subprocess  # Importation du module subprocess

# Création des argument :
config = configparser.ConfigParser()
parser = argparse.ArgumentParser()
parser.add_argument("-d", "--dhcp", help="DHCP : will not ne installed", action="store_false")
parser.add_argument("-f", "--firewall", help="FIREWALL : will not be installed", action="store_false")
parser.add_argument("-i", "--interfaces", help="INTERFACES : will not be configured", action="store_false")
parser.add_argument("-n", "--nat", help="NAT : will not be configured", action="store_false")
parser.add_argument("-r", "--route", help="Forwarding will not be enable", action="store_false")
parser.add_argument("-t", "--tools", help="Net-tools dnsUtils tcp-dump and SSH: will be not installed",
                    action="store_false")
parser.add_argument("-R", "--restart", help="Sytème will be reboot at the end of FRESHUP", action="store_false")
parser.add_argument("-F", "--force", help="Force the installation on other distribution BE CAREFUL",
                    action="store_false")
args = parser.parse_args()

# Création d'un fichier de log

# ------------------------------------------ Vérifiations  -------------------------------- #

if args.force:
    print('Verification...')
    # Vérification de la distribution
    """On lance un sousprocess via popen et on redirige stdout dans child pour avoir le exit statut
       Ici uname -a donne la version complète et grep chercher la présence du mot Débian"""
    child = subprocess.Popen("uname -a | grep Debian", shell=True, stdout=subprocess.PIPE)
    streamdata = child.communicate()[0]
    if child.returncode != 0:  # Si exit status de grep Debian n'est pas bon on quitte
        print('Vous n\'êtes pas sur une distribution Debian\nYour are not on a Debian Distribution\n')
        sys.exit(1)
    print('done.\n')
    # Vérification connection internet
    child = subprocess.Popen("ping 8.8.8.8 -c 4", shell=True, stdout=subprocess.PIPE)
    streamdata = child.communicate()[0]
    ping = child.returncode
    if ping == 0:
        child = subprocess.Popen("ping google.com -c 4", shell=True, stdout=subprocess.PIPE)
        streamdata = child.communicate()[0]
        dns = child.returncode
        if dns == 0:
            print('Connection is ok')
        else:
            print('Ping is ok... but it seem to have other troubles (could be a DNS resolving)'
                  '\nPlease check your connection')
            print('Ping is ok... but it seem to have other troubles (could be a DNS resolving)'
                  '\nPlease check your connection')
            sys.exit(2)
    else:
        print('There is some troubles... can\'t ping 8.8.8.8\nPlease check your connection')
        print('There is some troubles... can\'t ping 8.8.8.8\nPlease check your connection')
        sys.exit(2)

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

        print('Ssh {}.\n').format(paquet)
        with open('freshup.log', 'w') as freshlog:
            freshlog.write('{} setup :\n\n\n').format(paquet)
            subprocess.Popen("apt-get install -y {}", shell=True, stdout=freshlog, stderr=freshlog).format(paquet)

    def main():  # Mise en thread et attente du thread dans def main
        thread = threading.Thread(target=install)
        thread.start()
        thread.join()
    if __name__ == '__main__':
        main()

# ------------------------------------ Installation des outils ---------------------------- #

if args.tools:
    print('Tools setup...\n')
    # ------------------------------------------------------------------ #
    def ssh_install():
        """Setup openssh-server on linux distribution which have aperture"""
        print('Ssh setup.\n')
        with open('freshup.log', 'w') as freshlog:
            freshlog.write('Ssh setup :\n\n\n')
            subprocess.Popen("apt-get install -y openssh-server", shell=True, stdout=freshlog, stderr=freshlog)

    def main():  # Mise en thread et attente du thread dans def main
        thread = threading.Thread(target=ssh_install)
        thread.start()
        thread.join()
    if __name__ == '__main__':
        main()
    # ------------------------------------------------------------------ #

    def nettools_install():
        """Setup net-tools on linux distribution which have aperture"""
        print('Net-tools setup.\n')
        with open('freshup.log', 'w') as freshlog:
            freshlog.write('Net-tools setup :\n\n\n')
            subprocess.Popen("apt-get install -y net-tools", shell=True, stdout=freshlog, stderr=freshlog)

    def main():  # Mise en thread et attente du thread dans def main
        thread = threading.Thread(target=nettools_install)
        thread.start()
        thread.join()
    if __name__ == '__main__':
        main()
    # ------------------------------------------------------------------ #

    def dnsutils_install():
        """Setup dnsutils on linux distribution which have aperture"""
        print('dnsutils setup.\n')
        with open('freshup.log', 'w') as freshlog:
            freshlog.write('Dnsutils setup :\n\n\n')
            subprocess.Popen("apt-get install -y dnsutils", shell=True, stdout=freshlog, stderr=freshlog)

    def main():  # Mise en thread et attente du thread dans def main
        thread = threading.Thread(target=dnsutils_install)
        thread.start()
        thread.join()
    if __name__ == '__main__':
        main()
    # ----------------------------------------------------------------- #

    def tcpdump_install():
        """Setup tcpdump on linux distribution which have aperture"""
        print('Tcpdump setup.\n')
        with open('freshup.log', 'w') as freshlog:
            freshlog.write('tcpdump setup :\n\n\n')
            subprocess.Popen("apt-get install -y tcpdump", shell=True, stdout=freshlog, stderr=freshlog)

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
    def dhcp_install():
        """Setup isc-dhcp-server on linux distribution which have aperture"""
        print('Isc-dhcp-server setup.\n')
        with open('freshup.log', 'w') as freshlog:
            freshlog.write('DHCP-server setup :\n\n\n')
            subprocess.Popen("apt-get install -y isc-dhcp-server", shell=True, stdout=freshlog, stderr=freshlog)

    def main():  # Mise en thread et attente du thread dans def main
        thread = threading.Thread(target=dhcp_install)
        thread.start()
        thread.join()
    if __name__ == '__main__':
        main()

    # Configuration de dhcpd.conf
    dhcpd = open("/etc/dhcp/dhcpd.conf", "a")
    dhcpd.write('\nautoritative;\n\n')
    if config['INTERFACE1']['Type'] == 'LAN':
        dhcpd.write("subnet {} netmask {} {{\n  range {} {};\n  option routers {};\n}}\n\n"
                   .format(config['DHCP1']['SUBNET'], config['DHCP1']['NETMASK'], config['DHCP1']['START'],
                   config['DHCP1']['END'], config['DHCP1']['DGATE']))

    if config['INTERFACE2']['Type'] == 'LAN':
        dhcpd.write("subnet {} netmask {} {{\n  range {} {};\n  option routers {};\n}}\n\n"
                   .format(config['DHCP2']['SUBNET'], config['DHCP2']['NETMASK'], config['DHCP2']['START'],
                   config['DHCP2']['END'], config['DHCP2']['DGATE']))

    if config['INTERFACE3']['Type'] == 'LAN':
        dhcpd.write("subnet {} netmask {} {{\n  range {} {};\n  option routers {};\n}}\n\n"
                   .format(config['DHCP3']['SUBNET'], config['DHCP3']['NETMASK'], config['DHCP3']['START'],
                   config['DHCP3']['END'], config['DHCP3']['DGATE']))
    dhcpd.close()

    # Configuration de default/isc-dhcp-server
    iscdhcpd = open("/etc/default/isc-dhcp-server", "w")  # Config de l'écoute en fnct des paramètres
    if config['DHCP1']['DHCP'] == '1' and config['DHCP2']['DHCP'] == '0' and config['DHCP3']['DHCP'] == '0':
        iscdhcpd.write('INTERFACESv4="enp0s3"\nINTERFACESv6=""\n')
    if config['DHCP1']['DHCP'] == '0' and config['DHCP2']['DHCP'] == '1' and config['DHCP3']['DHCP'] == '0':
        iscdhcpd.write('INTERFACESv4="enp0s8"\nINTERFACESv6=""\n')
    if config['DHCP1']['DHCP'] == '0' and config['DHCP2']['DHCP'] == '0' and config['DHCP3']['DHCP'] == '1':
        iscdhcpd.write('INTERFACESv4="enp0s9"\nINTERFACESv6=""\n')
    if config['DHCP1']['DHCP'] == '1' and config['DHCP2']['DHCP'] == '1' and config['DHCP3']['DHCP'] == '0':
        iscdhcpd.write('INTERFACESv4="enp0s3 enp0s8"\nINTERFACESv6=""\n')
    if config['DHCP1']['DHCP'] == '1' and config['DHCP2']['DHCP'] == '0' and config['DHCP3']['DHCP'] == '1':
        iscdhcpd.write('INTERFACESv4="enp0s3 enp0s9"\nINTERFACESv6=""\n')
    if config['DHCP1']['DHCP'] == '0' and config['DHCP2']['DHCP'] == '1' and config['DHCP3']['DHCP'] == '1':
        iscdhcpd.write('INTERFACESv4="enp0s8 enp0s9"\nINTERFACESv6=""\n')
    if config['DHCP1']['DHCP'] == '1' and config['DHCP2']['DHCP'] == '1' and config['DHCP3']['DHCP'] == '1':
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
    # On autorise en IPv4 les ports selon la config :
    # ----------------------------------------------------------------- #
    if config['FIREWALL1']['FW'] == '1':
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
    if config['FIREWALL2']['FW'] == '1':
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
    if config['FIREWALL3']['FW'] == '1':
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
    if config['NAT']['NAT1'] == '1':
        os.system('iptables -t nat -A POSTROUTING -o enp0s3 -j MASQUERADE')
    if config['NAT']['NAT2'] == '1':
        os.system('iptables -t nat -A POSTROUTING -o enp0s8 -j MASQUERADE')
    if config['NAT']['NAT3'] == '1':
        os.system('iptables -t nat -A POSTROUTING -o enp0s9 -j MASQUERADE')
    print('done.\n')

# ------------------------------- Installation Iptables-persistent ------------------------ #

if args.nat or args.firewall:
    print('Iptables-persistent setup...\n')

    def iptables_install():
        """Setup iptable-persistent with assume yes on linux distribution which have aperture"""
        os.system('echo iptables-persistent iptables-persistent/autosave_v4 boolean true | debconf-set-selections')
        os.system('echo iptables-persistent iptables-persistent/autosave_v6 boolean true | debconf-set-selections')
        with open('freshup.log', 'w') as freshlog:
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
    child = subprocess.Popen("sysctl -p /etc/sysctl.conf", shell=True, stdout=subprocess.PIPE)
    streamdata = child.communicate()[0]
    rc = child.returncode
    if child.returncode != 0:  # Si exit status de grep Debian n'est pas bon on quitte
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
                     .format(config['INTERFACES']['IP1'], config['INTERFACES']['NM1'], config['INTERFACES']['GW1']))
    # Insertion de la conf de l'iface 2
    interfaces.write("#Iface 2\nauto enp0s8\niface enp0s8 inet static\naddress {}\nnetmask {}\ngateway {}\n\n"
                     .format(config['INTERFACES']['IP2'], config['INTERFACES']['NM2'], config['INTERFACES']['GW2']))
    # Insertion de la conf de l'iface 3
    interfaces.write("#Iface 3\nauto enp0s9\niface enp0s9 inet static\naddress {}\nnetmask {}\ngateway {}\n\n"
                     .format(config['INTERFACES']['IP3'], config['INTERFACES']['NM3'], config['INTERFACES']['GW3']))
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
            with open('freshup.log', 'w') as freshlog:
                freshlog.write('Networking Restart :\n\n\n')
                subprocess.Popen("/etc/init.d/networking restart", shell=True, stdout=freshlog, stderr=freshlog)

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
            with open('freshup.log', 'w') as freshlog:
                freshlog.write('Isc-dhcp-server Restart :\n\n\n')
                subprocess.Popen("/etc/init.d/isc-dhcp-server restart", shell=True, stdout=freshlog, stderr=freshlog)

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
sys.exit(0)

# ---------------------------------- |||||||||||||||||| ----------------------------------- #
# ---------------------------------- |FIN DU PROGRAMME| ----------------------------------- #
# ---------------------------------- |||||||||||||||||| ----------------------------------- #
