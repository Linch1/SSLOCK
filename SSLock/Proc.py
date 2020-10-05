from SSLock import General
import os
from datetime import datetime


def proc():
    # Securing /proc | /proc mounted with hidepid=2 so users can only see information about their processes
    error = 'Fatal Error: PROC will have to be configured manually'
    f_ntp_conf = "/etc/ntp.conf"
    response = General.answer('Securing /proc so users can only see information about their processes?')


    if not response: return
    General.output_message('Configuring proc')

    if not os.path.exists(f_ntp_conf):
        General.error_message(f"could not localte the file {f_ntp_conf}. Exiting /proc configuration.")
        return

    with open(f_ntp_conf, 'a') as file:
        file.write(f'''
       # added by debian9_Hardening.py on {datetime.today().strftime('%Y-%m-%d')} @ {datetime.now().strftime(
            '%H:%M:%S')}       
       proc     /proc     proc     defaults,hidepid=2     0     0
               ''')
