from SSLock import General


def ufw(SSH_ENABLE, SSH_PORT):
    # Firewall With UFW

    f_ufw_smtptls = '/etc/ufw/applications.d/smtptls'

    if not General.answer('Do you want install and configure UFW?'): return

    General.run_cmd('apt install ufw -y')
    General.run_cmd(
        'ufw default deny outgoing comment "deny all outgoing traffic"',
        'ufw default deny incoming comment "deny all incoming traffic"',
        'ufw allow out 53 comment "allow DNS calls out"',
        'ufw allow out 123 comment "allow NTP out"',
        'ufw allow out http comment "allow HTTP traffic out"',
        'ufw allow out https comment "allow HTTPS traffic out"',
        'ufw allow out whois comment "allow whois"',
        'ufw allow out 25 comment "allow MAIL out"'
    )
    with open(f_ufw_smtptls, 'w') as file:
        file.write('''
[SMTPTLS]
title=SMTP through TLS
description=This opens up the TLS port 465 for use with SMPT to send e-mails.
ports=465/tcp
            ''')
    General.run_cmd('ufw allow out smtptls comment "open TLS port 465 for use with SMPT to send e-mails"')
    General.output_message('''
The following ufw rules have been entered automatically:
- deny all outgoing traffic
- deny all incoming traffic
- allow DNS calls out-
- allow NTP out
- allow HTTP traffic out
- allow HTTPS traffic out
- allow whois
- allow SMPT out
- allow MAIL out
''')
    # ufw ssh rules
    if SSH_ENABLE and General.answer('(UFW) Do  you need ssh rule?'):
        General.run_cmd(f'ufw limit in {SSH_PORT} comment "allow SSH connections in"')
        General.output_message('Added Rules')

    # ufw ftp out rule
    if General.answer('(UFW) Do you need ftp out rule?'):
        General.run_cmd('ufw allow out ftp comment "allow FTP traffic out"')
        General.output_message('Added Rules')

    # ufw dhcp rule
    if General.answer('(UFW) Are you using DHCP?'):
        General.run_cmd('ufw allow out 68 comment "allow the DHCP client to update"')
        General.output_message('Added Rules')
       
    # ufw http/https rule
    if General.answer('(UFW) Do you nedd to allow http/https ( yes for websites servers ) ?'):
        General.run_cmd('ufw allow http comment "allow http traffic update"')
        General.run_cmd('ufw allow https comment "allow https traffic update"')
        General.output_message('Added Rules')

    General.output_message('Starting Firewall')
    General.warning_message('Maybe existing ssh connections will be stopped\n')
    General.warning_message('sometimes the next cmd get stuck so press ENTER after 1 minute')
    General.run_cmd('ufw --force enable')
