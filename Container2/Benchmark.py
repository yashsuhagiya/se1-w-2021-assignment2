import os
import stat

def prepare_exp(SSHHost, SSHPort, REMOTEROOT, optpt):
    f = open("config", 'w')
    f.write("Host benchmark\n")
    f.write("   Hostname %s\n" % SSHHost)
    f.write("   Port %d\n" % SSHPort)
    f.write("   IdentityFile ~/.ssh/sshcontainerkey\n")
    f.write("   StrictHostKeyChecking no\n")
    f.close()
    

    f = open("run-experiment.sh", 'w')
    f.write("#!/bin/bash\n")
    f.write("set -x\n\n")
    
    f.write("ssh -F config benchmark \"memcached -p 11211 -P memcached.pid > memcached.out 2> memcached.err &\"\n") # adjust this line to properly start memcached

    f.write("RESULT=`ssh -F config benchmark \"pidof memcached\"`\n")

    f.write("sleep 5\n")

    f.write("if [[ -z \"${RESULT// }\" ]]; then echo \"memcached process not running\"; CODE=1; else CODE=0; fi\n")

    f.write("mcperf -N %d -R %d -n %d -s %s > stats.log 2> stats.err\n\n" % (optpt["noRequests"]*10 ,optpt["noRequests"], optpt["concurrency"], SSHHost)) #adjust this line to properly start the client

    # f.write("REQPERSEC=`cat stats.log | cut -d \" \" -f 2 `\n")
    # f.write("LATENCY=`cat stats.log | cut -d \" \" -f 5 `\n")

    f.write("REQPERSEC=`cat stats.log | grep \"Response rate\" | cut -d \" \" -f 2`\n")
    f.write("LATENCY=`cat stats.log | grep \"Response time \[ms\]: avg\" | cut -d \" \" -f 5`\n")

    f.write("ssh -F config benchmark \"sudo kill -9 $RESULT\"\n")

    f.write("echo \"requests latency\" > stats.csv\n")
    f.write("echo \"$REQPERSEC $LATENCY\" >> stats.csv\n")

    f.write("scp -F config benchmark:~/memcached.* .\n")

    f.write("if [[ $(wc -l <stats.csv) -le 1 ]]; then CODE=1; fi\n\n")
    
    f.write("exit $CODE\n")

    f.close()
    
    os.chmod("run-experiment.sh", stat.S_IRWXU) 
