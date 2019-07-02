# FRESH UP
Merci d'utiliser Freshup, ce fichier ainsi que conf.help sont écrit en Markdown.
Pour plus de confort et de lisibilité, n'hésitez pas à coller le contenu de ces fichiers dans un outil dédié.


Pour lancer ce programme vous devez :
>1) Avoir les droits root
>2) Avoir une connexion internet fonctionnelle
>3) Avoir dans le même dossier freshup et conf.json
>4) Vous placer dans ce dossier avec la commande "cd /chemin/vers/votre/fichier/" (sans les guillemets)
>5) Exécuter la commande suivante : "python3 freshup" (sans les guillemets)

Le script Freshup permet de configurer un serveur DEBIAN fraichement installé de manière simple et rapide avec les outils essentiels à l'administration réseau.
## Le programme :
>Renomme les interfaces en ethx
>Configure jusqu'à trois interfaces
>Une route pour chacune d'elles
>Active et configure le pare-feu de manière avancé
>Active un NAT en postrouting en fonction du type d'interface choisie
>Installe Iptables-persistent
>Sauvegarde les règles
>Active le routage
>Installe DHCP-serveur
>Configure DHCP serveur pour fournir automatiquement les plages d'adresses
>Installe SSH
>Installe net-tools
>Installe dns-utils
>Installe tcp-dump

Votre serveur sera alors prêt à fonctionner ou y implémenter les derniers réglages.
Pour une optimisation des réglages veuillez modifier les options dans le fichier **conf.json**
Pour une aide concernant les réglages veuillez consulter **conf.help**

# OPTIONS :
Le script installant l'ensemble des fonctionnalités permises.
Utilisez les options suivantes afin d’empêcher l'installation des fonctionnalités non-voulues :

>-d = --dhcp
>-f = --firewall
>-i = --interfaces (elles ne seront pas configurées)
>-n = --nat
>-r = --route
>-t = --tools (net-tools, dnsutils, tcpdump, SSH ne seront pas installé)

Si -f et -n sont activées de concert iptables persistent ne sera pas installé et la configuration de iptables non sauvegardée.

#### AUTRES OPTIONS :
>-F = --force (force l'installation sur une autre distribution que Debian)
>-R = --restart (Redémarre la machine à la fin du programme)
>-h = --help (pour obtenir de l'aide à propos des options)


### EXIT STATUS :
0 : Le programme c'est terminé correctement
1 : Problème de détection de distribution (Etes-vous sur Debian?)
2 : Problème de connectivité internet
3 : Problème dans le fichier de configuration
4 : Problème durant l'installation d'un composant
5 : Problème durant la configuration du DHCP
6 : Problème durant la configuration du Firewall
7 : Autre problème de configuration rencontré

*Ce script a été réalisé par Mr M. Adrien dans le cadre d'un projet de formation Openclassrooms
Ce programme est libre d'accès et de modification sous licence GNU*