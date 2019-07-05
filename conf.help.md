# Aide pour la configuration
Le fichier de configuration se nomme conf.json
Vous pouvez éditer ce fichier à votre guise, mais voici quelques éléments à savoir :

__1) Veuillez respecter la syntaxe JSON__

__2) Les interfaces seront renommé en eth0 eth1 et eth2.__

__3) Il y'a trois grands chapitres dans ce fichier :__
        -Interfaces
        -DHCP
        -Firewall

## Interfaces
Vous pourrez configurer les informations principales concernant chaque interface.

DHCP : Dans chaque onglet portant le nom de l'interface vous pourrez modifier les règles du service DHCP

Firewall : Dans chaque onglet portant le nom de l'interface vous trouverez les mêmes paramètres pour les sous-onglet INPUT et OUTPUT.
>0 = Force la fermeture du/des ports concernés (DROP)
>1 = Valeur par défaut : le/les ports seront ouverts ou fermés en fonction du type d'interface désigné
>2 = Force l'ouverture du/des ports concernés (ACCEPT)

-Vous pouvez configurer trois différents "Types" d'interfaces. Ces types seront en fonction de ce à quoi est relié l'interface en question à savoir :

#### TYPE = WAN
Destiné à connecter cette interface sur la partie locale du réseau à administrer

DHCP --> on
NAT en postrouting --> off
##### Firewall INPUT :
>Established --> on
>Ping --> off
>DNS --> on
>HTTP --> off
>HTTPS --> off
>Printer --> on
>DHCP --> on
>FTP --> off
>SSH --> on
>IMAP --> off
>SMTP --> off
>POP3 --> off
>NTP --> on
>Avahi --> off
>Netbios --> on
>LDAP --> on

##### Firewall OUTPUT :
>Established --> on
>Ping --> off
>DNS -->  on
>HTTP -->  on
>HTTPS -->  on
>Printer --> on
>DHCP --> on
>FTP --> on
>SSH --> on
>IMAP --> on
>SMTP --> on
>POP3 --> on
>NTP -->  on
>Avahi --> off
>Netbios --> on
>LDAP --> on

#### TYPE = WAN
Destiné à rejoindre une passerelle réseau publique.

DHCP --> off
NAT en postrouting --> on
##### Firewall INPUT :

>Established --> on
>Ping --> off
>DNS --> off
>HTTP --> on
>HTTPS --> on
>Printer --> off
>DHCP --> off
>FTP --> on
>SSH --> off
>IMAP --> on
>SMTP --> on
>POP3 --> on
>NTP --> off
>Avahi --> off
>Netbios --> off
>LDAP --> off

##### Firewall OUTPUT :
>Established --> on
>Ping --> off
>DNS --> on
>HTTP --> on
>HTTPS --> on
>Printer --> off
>DHCP --> on
>FTP --> on
>SSH --> on
>IMAP --> on
>SMTP --> on
>POP3 --> on
>NTP --> on
>Avahi --> off
>Netbios --> off
>LDAP --> off


#### TYPE = DMZ
Destiné à rejoindre une zone démilitarisée de notre réseau à administrer.

DHCP --> off
NAT en postrouting --> off
##### Firewall INPUT :
>Established --> on
>Ping --> off
>DNS --> off
>HTTP --> on
>HTTPS --> on
>Printer --> off
>DHCP --> off
>FTP --> on
>SSH --> on
>IMAP --> on
>SMTP --> on
>POP3 --> on
>NTP --> off
>Avahi --> off
>Netbios --> off
>LDAP --> off

##### Firewall OUTPUT :
>Established --> on
>Ping --> off
>DNS --> off
>HTTP --> off
>HTTPS --> off
>Printer --> off
>DHCP --> off
>FTP --> off
>SSH --> off
>IMAP --> off
>SMTP --> off
>POP3 --> off
>NTP --> off
>Avahi --> off
>Netbios --> off
>LDAP --> off

Pour bien comprendre de quoi il s'agit, ces paramètres représentent ce qui seras autorisé à rentrer ou sortir du réseau connecté à l'interface. A cet effet les règles INPUT et OUTPUT sont des sous-règles de catégorie FORWARD. Par exemple :

Supposons un type LAN sur eth0, on auras donc IN et OUT en DHCP ce qui signifie l'application des deux règles suivantes :
>iptables -A FORWARD -i eth0 -o eth0 -p tcp --dport 68 -j ACCEPT
>iptables -A FORWARD -i eth0 -o eth0 -p udp --dport 67 -j ACCEPT
>iptables -A FORWARD -i eth0 -o eth0 -p udp --dport 68 -j ACCEPT

Les règles INPUT et OUTPUT sont configuré dans l'onglet serveur de firewall, celui se doit pour des raisons de sécurité
de conserver le strict nécessaire permettant sa maintenance.

Ceci représente donc les fonctions personnalisables qui s'ajoute en plus des fonctions de bases décrites dans le readme.md. Vous trouverez ci-dessous un extrait de l'arborescence commenté.
Si aucun port n'est spécifié pour le Firewall alors la règle concerne l'ensemble du protocole.

Voici un exemple du fichier de configuration. Les informations se présentent sous forme d'une arborescence.
Si vous voulez visualiser ce fichier sous forme graphique : collé le contenue de conf.json dans un des nombreux outils dédiés à cela, comme par exemple : http://jsonviewer.stack.hu/
{
  "Interfaces": {
    "eth0": {                       Parramètres généraux de l'interface eth0
      "Activated": 1,               1 = Active la configuration de la carte 0 = Désactive
      "IP": "192.168.0.1",          Adresse ip de l'interface
      "NetMask": "255.255.255.0",   Masque de sous-réseau de l'interface
      "GateWay": "192.168.3.254",   Passerelle de réseau
      "Type": "LAN",                Type de l'interface (voir ci-dessus)
      "Firewall": 1,                1 = Active le Firewall les règles seront en fonction du type choisit 0 = Désactive la configuration du Firewall sur le réseau
      "ForceDHCP": 0                1 = Force l'installation et la configuration du DHCP malgrés le type 0= Ne force rien : sera installé selon le type d'interface
    },
    "eth1": {                       Parramètres généraux de l'interface eth0
    ...
    },
    "eth2": {                       Parramètres généraux de l'interface eth0
    ...
    }
  },
  "DHCP": {
    "eth0": {                       Parramètres DHCP de l'interface eth0
      "SubNet": "192.168.0.0",      Réseau de distribution d'adresse
      "NetMask": "255.255.255.0",   Masque de soius réseau correspondant
      "Start": "192.168.0.2",       Plage de distibution des adresses IP première adresse
      "End": "192.168.0.253",       Plage de distibution des adresses IP derniière adresse
      "Dgate": "192.168.0.254"      Configuration de passerelle sur les clients
    },
    "eth1": {                       Parramètre DHCP de l'interface eth1
    ...
    },
    "eth2": {                       Parramètre DHCP de l'interface eth2
    ...
    }
  },
  "FireWall": {
    "Server": {                     Parramètres Firewall du serveur lui même
      "Established": 1,
      "Ping": 1,
      "SSH": 1,
      "DHCP": 0,
      "DNS": 0,
      "NTP": 0
    },
    "eth0": {
      "INPUT": {
        "Established": 1,
        "Ping": 1,
        "DNS": 1,
        "HTTP": 1,
        "HTTPS": 1,
        "Printer": 1,
        "DHCP": 1,
        "FTP": 1,
        "SSH" : 1,
        "IMAP": 1,
        "SMTP": 1,
        "POP3": 1,
        "NTP": 1,
        "Avahi": 1,
        "Netbios": 1,
        "LDAP": 1
      },
      "OUTPUT": {
        "Established": 1,
        "Ping": 1,
        "DNS": 1,
        "HTTP": 1,
        "HTTPS": 1,
        "Printer": 1,
        "DHCP": 1,
        "FTP": 1,
        "SSH" : 1,
        "IMAP": 1,
        "SMTP": 1,
        "POP3": 1,
        "NTP": 1,
        "Avahi": 1,
        "Netbios": 1,
        "LDAP": 1
      }
    },
    "eth1": {
      "INPUT": {
        ...
      },
      "OUTPUT": {
        ...
      }
    },
    "eth2": {
      "INPUT": {
        ...
      },
      "OUTPUT": {
        ...
      }
    }
  }
}
