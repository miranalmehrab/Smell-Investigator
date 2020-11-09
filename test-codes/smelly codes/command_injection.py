process = input()
pre = 'kil - {}'.format(process)

subprocess.Popen('kil - {}'.format(process))
subprocess.Popen("A list: %s, %s" % process % pre)
subprocess.Popen('In the basket are %s and %s' % (comm,pre))
