import re
regip = re.compile("^(25[0–5]|2[0–4][0–9]|[01]?[0–9][0–9]?).(25[0–5]|2[0–4][0–9]|[01]?[0–9][0–9]?)."
                   "(25[0–5]|2[0–4][0–9]|[01]?[0–9][0–9]?).(25[0–5]|2[0–4][0–9]|[01]?[0–9][0–9]?)$")
values = '0.0.0.0'
if not regip.match(values):
    print('There is an error in conf.json > DHCP.')