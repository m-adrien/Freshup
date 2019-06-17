#!/usr/bin/python3.7
# -*-coding:utf-8 -*

####Vérifions que nous sommes sur Debian####

##Création de la variable verif en fonction de la présence du mot debian dans la version de la distribution##
#Import commandes bash de l'os#
import os
os.system('uname -a | grep Debian')
verif = os.system('echo $?')
#Si la varible est 1 (pas de ligne avec Debian dans la version du système) alors on arrête le programme
if verif = 1 :
   sys.exit([0])
#On importe la configuration
conf = open("freshup.conf", "r")
#On recupère nos variables

#On ferme le fichier de conf
conf.close()

##Maintenant que les vérifications et la conf est charger c'est parti##
#Configuration des interfaces
interfaces = open("/etc/network/interfaces", "w")
#Importation du module pickle
import pickle
#Création du pickle de conf de base
iface0 = "source /etc/network/interfaces.d/*\n\n#loopback iface\nauto lo\niface lo inet loopback\n\n"
with open('iface0', 'wb') as fichier:
    mon_pickler = pickle.Pickler(fichier)
    mon_pickler.dump(score)
#Création du pickle de conf d'interfaces 1
iface1 = f"#Iface 1\nauto enp0s3\niface enp0s3 inet static\naddress {IP1}\n"
with open('iface0', 'wb') as fichier:
    mon_pickler = pickle.Pickler(fichier)
    mon_pickler.dump(score)