________________________________________________________________________________________________________________
_______________________________________________FRESH UP_________________________________________________________

_______________________________________________FRANCAIS_________________________________________________________
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

Pour une optimisation des réglages veuillez modifiez les options dans le fichier conf.ini

OPTIONS :
Le script installant l'ensemble des fonctionnalités permisespar le script vous pouvez utiliser les options
suivantes afin d'empècher complètement leur installation.

-d = DHCP

-f = Firewall

-i = interfaces : ne seront pas configuré

-n = NAT

-t = tools : net-tools, ns-lookup

Autres Options :
-F = Forcer l'installation sur une autre distribution que debian
ATTENTION CE PARRAMETRE PEUT AVOIR DES EFFETS INNATENDU !

*Ce script à été réalisé par M.Adrien dans le cadre d'un projet de formation Openclassrooms
*Ce programme est libre d'accès et de modification sous licence GNU

_______________________________________________ENGLISH________________________________________________________
This program will configure a freshly install of DEBIAN with these features :
          -Three network interfaces
          -One gateway for each
          -Firewall activation and allow just : icmp http https dns and established
          -Activate a postrouting NAT  on the first interface
          -Installe Iptables-persistent
          -Save the new rules
          -Routing Activation
          -DHCP-serveur setup
          -DHCP configuration on Ifaces 2 and 3 with gateway configuration for theme
          -Net-tools and ns-lookup setup
Your server will be ready to play, however for a finer tune please edit the conf.ini file

Pour une optimisation des réglages veuillez modifiez les options dans le fichier conf.py

OPTIONS :
The programm will (by default) install the full features. To prevent some basic features from setup use these options :

-d = DHCP

-f = Firewall

-i = interfaces : will be not configure

-n = NAT

-t = tools : net-tools, ns-lookup

Other options :
-F : force the installation on other distrubutions
BE CAREFUL THIS OPTION MAY HAVE UNEXPECTED EFFECT ON THE SYSTEME !

*This script was created by Mr. Adrien as part of an Openclassrooms training project
*This program is freely accessible and modified under GNU license