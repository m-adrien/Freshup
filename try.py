import json
data = open('conf.json', 'r')
config = json.load(data)
data.close()

if config['Interfaces']['eth0']['Type'] == 'LAN' or config['DHCP']['eth0']['Forced'] == 1:
    dhcpeth0 = 1  # Création de la variable pour la suite
    print("subnet {} netmask {} {{\n  range {} {};\n  option routers {};\n}}\n\n".format(
    config['DHCP']['eth0']['SubNet'], config['DHCP']['eth0']['NetMask'],
    config['DHCP']['eth0']['Start'], config['DHCP']['eth0']['End'],
    config['DHCP']['eth0']['Dgate']))

if config['Interfaces']['eth1']['Type'] == 'LAN' or config['DHCP']['eth1']['Forced'] == 1:
    dhcpeth1 = 1  # Création de la variable pour la suite
    print("subnet {} netmask {} {{\n  range {} {};\n  option routers {};\n}}\n\n".format(
        config['DHCP']['eth1']['SubNet'], config['DHCP']['eth1']['NetMask'],
        config['DHCP']['eth1']['Start'], config['DHCP']['eth1']['End'],
        config['DHCP']['eth1']['Dgate']))

if config['Interfaces']['eth2']['Type'] == 'LAN' or config['DHCP']['eth2']['Forced'] == 1:
    dhcpeth2 = 1  # Création de la variable pour la suite
    print("subnet {} netmask {} {{\n  range {} {};\n  option routers {};\n}}\n\n".format(
        config['DHCP']['eth2']['SubNet'], config['DHCP']['eth2']['NetMask'],
        config['DHCP']['eth2']['Start'], config['DHCP']['eth2']['End'],
        config['DHCP']['eth2']['Dgate']))