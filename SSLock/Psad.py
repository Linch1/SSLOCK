from SSLock import General
import subprocess


def psad(EMAIL):
    # iptables Intrusion Detection And Prevention with

    f_psad_conf = '/etc/psad/psad.conf'
    f_before_rules = '/etc/ufw/before.rules'
    f_before6_rules = '/etc/ufw/before6.rules'

    if not General.answer('Do you want to install and configure psad?'): return

    General.run_cmd('apt install psad -y')
    homenet = General.input_message('Type your Home net: ex(192.168.1.1/24) ')
    General.output_message('Configuring psad')
    General.change_lines(
         f_psad_conf,
         _1=[
             'EMAIL_ADDRESSES             root@localhost;',
             f'EMAIL_ADDRESSES             {EMAIL};\n'
         ],
         _2=[
             'HOSTNAME                     _CHANGEME_;',
             f'HOSTNAME                   {General.HOSTNAME};\n'
         ],
         _3=[
             'ENABLE_AUTO_IDS             N;',
             'ENABLE_AUTO_IDS             Y;\n'
         ],
         _4=[
             'HOME_NET                    any;',
             f'HOME_NET                    {homenet};\n'
         ],
         _5=[
             'PORT_RANGE_SCAN_THRESHOLD   1;',
             'PORT_RANGE_SCAN_THRESHOLD   2;\n'
         ],
         _6=[
             'ENABLE_MAC_ADDR_REPORTING   N;',
             'ENABLE_MAC_ADDR_REPORTING   Y;\n'
         ],
         _7=[
             'ALERT_ALL                   Y;',
             'ALERT_ALL                   N;\n'
         ]

    )


    General.output_message(f'''
These changes have been made to the config '/etc/psad/psad.conf'.
If u need more advanced options feel free to modify it.
    - EMAIL_ADDRESSES             {EMAIL};
    - HOSTNAME                   {General.HOSTNAME};
    - ENABLE_AUTO_IDS             Y;
    - HOME_NET                    {homenet};
    - PORT_RANGE_SCAN_THRESHOLD   2;
    - ENABLE_MAC_ADDR_REPORTING   Y;
    - ALERT_ALL                   N;

                ''')

    with open(f_before_rules, 'r') as file:
        lines = file.readlines()
        text = file.read()
        if not ( General.check_lines_in_file(f_before_rules,
                                    '# log all traffic so psad can analyze',
                                    '-A INPUT -j LOG --log-tcp-options --log-prefix "[IPTABLES]"',
                                    '-A FORWARD -j LOG --log-tcp-options --log-prefix "[IPTABLES]"') ):

            for index, line in enumerate(lines):
                if line.strip() == "COMMIT":
                    lines.insert(index - 2,
                                 '# log all traffic so psad can analyze\n-A INPUT -j LOG --log-tcp-options --log-prefix "[IPTABLES]"\n-A FORWARD -j LOG --log-tcp-options --log-prefix "[IPTABLES]"')
                    break
            with open(f_before_rules, 'w') as file:
                for line in lines:
                    file.write(line)

    with open(f_before6_rules, 'r') as file:
        lines = file.readlines()
        text = file.read()
        if not ( General.check_lines_in_file(f_before_rules,
                                    '# log all traffic so psad can analyze',
                                    '-A INPUT -j LOG --log-tcp-options --log-prefix "[IPTABLES]"',
                                    '-A FORWARD -j LOG --log-tcp-options --log-prefix "[IPTABLES]"') ):
            for index, line in enumerate(lines):
                if line.strip() == "COMMIT":
                    lines.insert(index - 2,
                                 '# log all traffic so psad can analyze\n-A INPUT -j LOG --log-tcp-options --log-prefix "[IPTABLES]"\n-A FORWARD -j LOG --log-tcp-options --log-prefix "[IPTABLES]"')
                    break
            with open(f_before6_rules, 'w') as file:
                for line in lines:
                    file.write(line)

    General.warning_message('Restarting psad and Firewall..\n')
    General.warning_message('Maybe existing ssh connections will be stopped\n')
    General.run_cmd('ufw --force enable')
    General.run_cmd('ufw reload')
    subprocess.check_call(['psad', '-R'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    General.run_cmd('psad --sig-update')
    General.run_cmd('psad -H')
    General.output_message('Done')
