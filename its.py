import crypt
for n in xrange (17000, 22000):
  if n % 100 == 0:
      print '        '+ str(n)    
  for e in xrange(12000, 20000):
    pw = '60' + str(n) + '011' + str(e)
    c = crypt.crypt(pw, '$6$ggyverZF')
    if (c[12:22] == '2i28Y2Jw9w'):
       print n, e, pw

