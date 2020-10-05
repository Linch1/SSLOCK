from SSLock import General
import os
from datetime import datetime

def ntp():
    # installing NTP client and keeping server time in-sync

    error = 'Fatal Error: NTP will have to be configured manually'
    response = General.answer('Install NTP client and keeping server time in-sinc ?')
    check_attempt = 0
    f_ntp_conf = '/etc/ntp.conf'
    if not response: return

    General.run_cmd('apt install ntp -y')

    if not os.path.exists(f_ntp_conf):
        General.error_message(f"could not localte the file {f_ntp_conf}. Exiting ntp configuration.")
        return

    General.output_message('Configuring NTP')
    with open(f_ntp_conf, 'w') as file:
        file.write(f'''
    # added by debian9_Hardening.py on {datetime.today().strftime('%Y-%m-%d')} @ {datetime.now().strftime('%H:%M:%S')}        
    driftfile /var/lib/ntp/ntp.drift
    statistics loopstats peerstats clockstats
    filegen loopstats file loopstats type day enable
    filegen peerstats file peerstats type day enable
    filegen clockstats file clockstats type day enable
    restrict -4 default kod notrap nomodify nopeer noquery limited
    restrict -6 default kod notrap nomodify nopeer noquery limited
    restrict 127.0.0.1
    restrict ::1
    restrict source notrap nomodify noquery
    pool pool.ntp.org iburst
            ''')

    General.run_cmd('service ntp restart')
