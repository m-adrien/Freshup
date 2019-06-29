________________________________________________________________________________________________________________
_______________________________________________FRESH UP_________________________________________________________

_______________________________________________FRANCAIS_________________________________________________________
Pour lancer ce programme vous devez :
1) Avoir les droits root
<<<<<<< HEAD
2) Avoir une connection internet fonctionelle
3) Avoir dans le même dossier freshup et conf.ini
4) Vous placer dans ce dossier avec la commande "cd /chemin/vers/votre/fichier/"
5) Executer la commande suivante : "python3 freshup" (sans les guillemets)
=======
2) Avoir dans le même dossier freshup.py et conf.ini
3) Vous placer dans ce dossier avec la commande "cd /chemin/vers/votre/fichier/"
4) Executer la commande suivante : "python3 freshup.py" (sans les guillemets)
>>>>>>> parent of b58b8da... v1.1

Le script Freshup permet de configurer un serveur DEBIAN fraichement installé de manière simple et rapide avec
les outils essentiels à l'administration réseau.
Par défaut le programme :
          -Configure trois interfaces
          -Une route pour chacune d'elles
          -Active le pare-feu en ne laissant passer que : icmp ssh http https dns et established
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
Pour une optimisation des réglages veuillez modifier les options dans le fichier conf.ini

OPTIONS :
Le script installant l'ensemble des fonctionnalités permises.
Utilisez les options suivantes afin d’empêcher l'installation des fonctionalités non-voulues :

-d = DHCP
-f = Firewall
-i = Interfaces : ne seront pas configurées
-n = NAT
-r = routage
-t = tools : net-tools, dnsutils, tcpdump, SSH
	**Si -f et -n sont activées de concert iptables persistent ne sera
	  pas installé et la configuration de iptables non sauvegardée

AUTRES OPTIONS :
-F = Forcer l'installation sur une autre distribution que Debian
ATTENTION CE PARAMÈTRE PEUT AVOIR DES EFFETS INATTENDUS !
-R = Redémarrer le système à la fin du programme.
-h = Help pour Obtenir de l'aide à propos des options.

LOG :
Un fichier freshup.log sera créer dans le répertoire actuel vous trouverez à l'interieur l'ensemble
des logs d'installation des différents composants.

EXIT STATUS :
0 : Le programme c'est terminé correctement
1 : Problème de detection de distribution (Etes-vous sur Debian?)
2 : Problème de connectivité internet

*Ce script à été réalisé par Mr M Adrien dans le cadre d'un projet de formation Openclassrooms
*Ce programme est libre d'accès et de modification sous licence GNU

_______________________________________________ENGLISH________________________________________________________
To run this programm you need to :
1)Get the root's rights
<<<<<<< HEAD
2)Have a working internet connection
3)Have in the same directory freshup and conf.ini
4)Move into this directory with "cd /path/to/your/file/"
5)Enter this command "python3 freshup" (without the "")
=======
2)Have in the same directory freshup.py and conf.ini
3)Move into this directory with "cd /path/to/your/file/"
4)Enter this command "python3 freshup.py" (without the "")
>>>>>>> parent of b58b8da... v1.1

This program will simply and quickly configure a freshly setup of DEBIAN with somes essentials sysadmin tools.
By default the program will make :
          -Three network interfaces configuration
          -One gateway for each
          -Firewall activation and allow just : icmp ssh http https dns and established
          -Activate a postrouting NAT on the first interface
          -Iptables-persistent setup
          -Save the new rules
          -Routing Activation
          -DHCP-serveur setup
          -DHCP configuration on Ifaces 2 and 3 with gateway configuration for them
          -SSH setup
          -Net-tools setup
          -Dns-utils setup
          -Tcp-dump setup
Your server will be ready to play, however for a finer tune please edit the conf.ini file.

OPTIONS :
The programm will (by default) install the full features.
To prevent some basics features from setup use these options :

-d = DHCP
-f = Firewall
-i = interfaces : will not be configured
-n = NAT
-r = route : forwarding will not be enable
-t = tools : net-tools, dnsutils, tcpdump, SSH
	**If -f and -n are both activated iptables-persistent will be not setup
	  and the iptables configuration not saved

OTHER OPTIONS :
-F = force the installation on other distrubutions
BE CAREFUL THIS OPTION MAY HAVE UNEXPECTED EFFECT ON THE SYSTEME !
-R = reboot the system at the end of Freshup
-h = Help : provide some informations about these options

LOG:
A freshup.log file will be created in the current directory you will find inside the
installation logs of the different components.

EXIT STATUS :
0 : Programme was correctly finished
1 : Distribution reading got a probleme (Are you on Debian?)
2 : Problème de connectivité internet

*This script was created by Mr. M Adrien for an Openclassrooms training project
*This program is freely accessible and modified under GNU license