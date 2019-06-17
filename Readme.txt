________________________________________________________________________________________________________________
_______________________________________________FRESH UP_________________________________________________________

Le script freshup permet de configurer un serveur DEBIAN fraichement installé de manière simple et rapide
Par défaut le fichier :
          -Configure trois interfaces
          -Une route pour chacune d'elles
          -Active le parefeu en ne laissant passer que : icmp http https dns et established
          -Active un NAT en sorite de l'interface n°1
          -Installe Iptables-persistent
          -Sauvegarde les règles
          -Active le routage
          -Installe DHCP-serveur
          -Configure DHCP serveur pour fournir deux plages d'adresses avec les passerelles correspondante
          -Installe net-tools; ns-lookup
Votre serveur sera alors prêt à fonctionner ou y implémenter les derniers réglages.

Pour une optimisation des réglages veuillez modifiez les options dans le fichier conf.py

OPTIONS :
Le script installant l'ensemble des fonctionnalités vous pouvez utiliser les options suivantes afin d'en enlever.
To remove some basic features use this :

-d = DHCP

-f = Firewall

-n = NAT

-t = tools : net-tools, ns-lookup

*Ce script à été réalisé par M.Adrien dans le cadre d'un projet de formation Openclasroom


________CONF FILE DESCRIPTION________

[INTERFACES]
Configuration des interfaces de la machine

IFACE 1 : enp0s3
#adresse IP
IP1=192.168.3.1
#netmask
NM1=255.255.255.0
#Passerelle gateway
GW1=192.168.3.254

###IFACE 2 : enp0s8
#adresse IP
IP2=192.168.2.254
#netmask
NM2=255.255.255.0
#Passerelle gateway
GW1=192.168.2.254

###IFACE 3 : enp0s9
#adresse IP
IP2=192.168.1.1
#netmask
NM2=255.255.255.0
#Passerelle gateway
GW2=192.168.1.254

[NAT]

#NAT sur IFACE 1 : 0=non 1=oui
NAT1 = 1
#NAT sur IFACE 2 : 0=non 1=oui
NAT2 = 0
#NAT sur IFACE 3 : 0=non 1=oui
NAT3 = 0

[DHCP]

###Ecoute

#Ecoute sur IFACE 1 : 0=non 1=oui
DHCP1 = 0
#Ecoute sur IFACE 2 : 0=non 1=oui
DHCP2 = 1
#Ecoute sur IFACE 3 : 0=non 1=oui
DHCP3 = 1

###Plages

#Sur IFACE 1
START1 = ""
END1 = ""
DGATE1 = ""

#Sur IFACE 2
START2 = "192.168.2.1"
END2 = "192.168.2.253"
DGATE2 = "192.168.2.254"

#Sur IFACE 3
START3 = "192.168.1.1"
END3 = "192.168.1.253"
DGATE3 = "192.168.1.254"