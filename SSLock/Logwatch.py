from SSLock import General

def logwatch(EMAIL):
    # logwatch - system log analyzer and reporter

    f_logwatch = '/etc/cron.daily/00logwatch'

    if not General.answer('Do you want to install and configure logwatch?'): return

    General.run_cmd('apt install logwatch -y')
    with open(f_logwatch, 'w') as file:
        file.write(f'''
    #!/bin/bash

    #Check if removed-but-not-purged
    test -x /usr/share/logwatch/scripts/logwatch.pl || exit 0

    #execute
    /usr/sbin/logwatch --output mail --format html --mailto {EMAIL} --range yesterday --service all
    ''')

    General.warning_message('Restarting firewall Maybe existing ssh connections will be stopped\n')
    General.run_cmd('ufw --force enable')