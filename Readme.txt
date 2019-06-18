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

*Ce script à été réalisé par M.Adrien dans le cadre d'un projet de formation Openclassrooms