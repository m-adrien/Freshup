# FRESH UP
Merci d'utiliser Freshup, ce fichier ainsi que conf.help.md sont écrit en Markdown.
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
Pour une aide concernant les réglages veuillez consulter **conf.help.md**

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


*Ce script a été réalisé dans le cadre d'un projet de formation Openclassrooms
Ce programme est libre d'accès et de modification sous licence GNU*

## Comment contribuer :

__Les deux fichiers fonctionnels sont :__
-freshup écrit en python 3.7 contenant le programme
-conf.json écrit en json qui contient l'ensemble des paramètres

__Vous pouvez modifier le programme freshup, voici ce qu'il faut savoir :__

Le programme est écrit sous forme de blocs presque tous interchangeables en position. Ces blocs sont séparés par une ligne de commentaire ayant la structure # ------ Ce que le bloc fait ------- #.
De plus il recommence tous à l'indentation 0. 
Très souvent ces blocs sont optionnels et débute par if args.notreargument.
Cet argument est stocké en false dans les lignes de parser en début de fichier. En conséquence : s’il est sélectionné derrière la ligne de commande en argument (freshup -x) cela désactivera tout le bloc dépendent.

Attention vous devez utilisé os.systeme à la place de la nouvelle commande subprocess.popen lorsque vous fait du threat.
Les deux fonctions présentent dans ce programme n'étant pas compatible ensemble sous Debian.

En revanche ailleurs il est recommandé d'utiliser subprocess : ceci est recommander par la documentation officielle et vous permettra notamment de récupérer les STDOUT et STDERR voir le child afin de connaitre le statuts d'une commande effectuer sous Debian ou d'afficher l'erreur sur l'écran utilisateur.
Vous trouverez un exemple # ----- Vérifications Connection ------ #

conf.json est stocké sous une variable 'config' de type dictionnaire de dictionnaire de dictionnaire. Vous devez ainsi l'appeler sous la forme :
config['Dictionaire 1']['Dictionaire 2']['Dictionaire 3']['clé']

Toute fonction touchant au fonctionnement central du système doit être encapsulée dans un try afin d'éviter de corrompre le système, veuillez rajouter un sys.exit() avec le code du exit statuts en correspondance avec la liste décrite ci-dessus.

__Vous pouvez rajouter l'ensemble des options que vous souhaitez dans le fichier conf.json en prenant soin :__
De ne pas modifier la structure existante
Rajouter un contrôle de la clé dans freshup dans le bloc # ---- Vérification de conf.json -----#
Respectant la syntaxe .json


Vous pouvez également rajouter de la structure en suivant les règles d'indentations :
