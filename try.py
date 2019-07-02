errorX = None
try:
    a1 = True
    print('print this will not work{}'.format(a1))
except Exception as erreur:
    errorX = erreur

if errorX:
    print('This is working')
