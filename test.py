import configparser
config = configparser.ConfigParser()
config.read('conf.ini')
IP1 = config.get('INTERFACES', 'IP1')
IP2 = config.get('INTERFACES', 'IP2')
IP3 = config.get('INTERFACES', 'IP3')
NM1 = config.get('INTERFACES', 'NM1')
NM2 = config.get('INTERFACES', 'NM2')
NM3 = config.get('INTERFACES', 'NM3')
GW1 = config.get('INTERFACES', 'GW1')
GW2 = config.get('INTERFACES', 'GW2')
GW3 = config.get('INTERFACES', 'GW3')
NAT1 = config.get('NAT', 'NAT1')
NAT2 = config.get('NAT', 'NAT2')
NAT3 = config.get('NAT', 'NAT3')
DHCP1 = config.get('DHCP', 'DHCP1')
DHCP2 = config.get('DHCP', 'DHCP2')
DHCP3 = config.get('DHCP', 'DHCP3')
START1 = config.get('DHCP', 'START1')
START2 = config.get('DHCP', 'START2')
START3 = config.get('DHCP', 'START3')
END1 = config.get('DHCP', 'END1')
END2 = config.get('DHCP', 'END2')
END3 = config.get('DHCP', 'END3')
DGATE1 = config.get('DHCP', 'DGATE1')
DGATE2 = config.get('DHCP', 'DGATE2')
DGATE3 = config.get('DHCP', 'DGATE3')

print (GW2)
print (END2)
print (DGATE1)
print (IP3)