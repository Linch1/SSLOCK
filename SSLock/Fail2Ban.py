from SSLock import General

def fail2ban(EMAIL):

    # Application Intrusion Detection And Prevention With Fail2Ban
    f_f2b_jail = '/etc/fail2ban/jail.local'
    if not General.answer('Do you want to install and configure Fail2Ban?'): return

    General.run_cmd('apt install fail2ban -y')
    General.run_cmd(
        'systemctl start fail2ban',
        'systemctl enable fail2ban'
    )
    General.output_message("fail2ban is running")

    with open(f_f2b_jail, 'w') as file:
        lan_segment = General.input_message('What is you lan segment? (ex. 192.168.1.1/24) :')
        file.write(f'''
    [DEFAULT]
    # the IP address range we want to ignore
    ignoreip = 127.0.0.1/8 {lan_segment}

    # who to send e-mail to
    destemail = {EMAIL}

    # who is the email from
    sender = {General.USER}.{General.HOSTNAME}.{EMAIL}

    # since we're using exim4 to send emails
    mta = mail

    # get email alerts
    action = %(action_mwl)s
                ''')

    General.output_message('Configuring Intrusion and detection tools')

    if not General.answer('Do You need a jail for SSH that tells fail2ban to look at SSH logs and use ufw to ban/unban IPs ?') : return

    with open(f_f2b_jail, 'a') as jail_file:
        jail_file.write('''
    [sshd]
    enabled = true
    banaction = ufw
    port = ssh
    filter = sshd
    logpath = %(sshd_log)s
    maxretry = 5
    ''')

    General.run_cmd(
        'fail2ban-client start',
        'fail2ban-client reload'
    )
    General.output_message("Tools reloaded")
    General.run_cmd('systemctl restart fail2ban')
