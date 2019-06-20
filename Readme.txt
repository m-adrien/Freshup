________________________________________________________________________________________________________________
_______________________________________________FRESH UP_________________________________________________________

_______________________________________________FRANCAIS_________________________________________________________
Le script Freshup permet de configurer un serveur DEBIAN fraichement installé de manière simple et rapide avec
les outils essentiel à l'administration réseau.
Par défaut le programme :
          -Configure trois interfaces
          -Une route pour chacune d'elles
          -Active le parefeu en ne laissant passer que : icmp ssh http https dns et established
          -Active un NAT en sorite de l'interface n°1
          -Installe Iptables-persistent
          -Sauvegarde les règles
          -Active le routage
          -Installe DHCP-serveur
          -Configure DHCP serveur pour fournir deux plages d'adresses
		        sur les interfaces 2 et 3 avec les passerelles correspondantes
          -Installe SSH
          -Installe net-tools
          -Installe dns-utils
          -Installe tcp-dump
Votre serveur sera alors prêt à fonctionner ou y implémenter les derniers réglages.

Pour une optimisation des réglages veuillez modifiez les options dans le fichier conf.ini

OPTIONS :
Le script installant l'ensemble des fonctionnalités permises.
Utilisez les options suivantes afin d’empêcher leur installation :

-d = DHCP

-f = Firewall

-i = interfaces : ne seront pas configurées

-n = NAT

-t = tools : net-tools, dnsutils, tcpdump, SSH

	Si -f et -n sont activé de concert iptables persistent ne sera
	pas installé et la configuration de iptables non sauvegardée

Autres Options :
-F = Forcer l'installation sur une autre distribution que Debian
ATTENTION CE PARAMÈTRE PEUT AVOIR DES EFFETS INATTENDU !

-r = Redémarre le système à la fin du programme.

MERCI DE LANCER CE PROGRAMME EN ROOT

*Ce script à été réalisé par M.Adrien dans le cadre d'un projet de formation Openclassrooms
*Ce programme est libre d'accès et de modification sous licence GNU

_______________________________________________ENGLISH________________________________________________________
This program will simply and quily configure a freshly install of DEBIAN with in bonus somes essentiels
sysadmin tools.
By default the program will make :
          -Three network interfaces configuration
          -One gateway for each
          -Firewall activation and allow just : icmp ssh http https dns and established
          -Activate a postrouting NAT  on the first interface
          -Iptables-persistent setup
          -Save the new rules
          -Routing Activation
          -DHCP-serveur setup
          -DHCP configuration on Ifaces 2 and 3 with gateway configuration for theme
          -SSH setup
          -Net-tools setup
          -Dns-utils setup
          -Tcp-dump setup
Your server will be ready to play, however for a finer tune please edit the conf.ini file.

OPTIONS :
The programm will (by default) install the full features.
To prevent some basic features from setup use these options :

-d = DHCP

-f = Firewall

-i = interfaces : will be not configure

-n = NAT

-t = tools : net-tools, dnsutils, tcpdump, SSH

Other options :
-F : force the installation on other distrubutions
BE CAREFUL THIS OPTION MAY HAVE UNEXPECTED EFFECT ON THE SYSTEME !

-r : reboot the system at the end of Freshup

THIS PROGRAM NEED ROOT'S RIGHTS TO WORKS

*This script was created by Mr. Adrien as part of an Openclassrooms training project
*This program is freely accessible and modified under GNU license