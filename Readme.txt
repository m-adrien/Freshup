FRESH UP
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
          -Configure DHCP serveur pour fournir deux plage d'adresses avec la passerelle correspondante
          -Installe net-tools; ns-lookup
Votre serveur sera alors prêt à faire à fonctionner ou y implémenter les derniers réglages.

Pour une optimisation des réglages veuillez modifiez les options dans le fichier freshup.conf.

*Ce script à été réalisé par M.Adrien dans le cadre d'un projet de formation Openclasroom
