_______________________________________________________________________________________________________________
_______________________________________________FRESH UP________________________________________________________

_______________________________________________FRANCAIS________________________________________________________
Pour lancer ce programme vous devez :
1) Avoir les droits root
2) Avoir une connection internet fonctionelle
3) Avoir dans le même dossier freshup et conf.ini
4) Vous placer dans ce dossier avec la commande "cd /chemin/vers/votre/fichier/"
5) Executer la commande suivante : "python3 freshup" (sans les guillemets)

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
3 : Problème dans le ficher de configuration
4 : Problème durant l'installation d'un composant
5 : Porbleme durant la configuration du DHCP
6 : Problème durant la configuration du FireWall
7 : Autre probleme de configuration rencontré

*Ce script à été réalisé par Mr M Adrien dans le cadre d'un projet de formation Openclassrooms
*Ce programme est libre d'accès et de modification sous licence GNU