"""
This script does the setup of a server that has to run a wordpress site with apache2.
This script was made following some DigitalOcean guides

This are the following steps that you want to cover:

- SSH KEYS SETUP ( not covered in the script ) : https://www.digitalocean.com/community/tutorials/how-to-set-up-ssh-keys-on-ubuntu-20-04
- ADDING USERS
"""

import sys
import os
import traceback

sys.path.insert(0, os.path.abspath(__file__ + "/../../")) # add the current module to sys.path

from SSLock import General, UsersConfig, Mail, SSHConfig, Nvidia, Ntp, Proc, EntropyPool, Ufw, Fail2Ban, Aide, ClamAv, Maldet, \
    RkHunter, Logwatch, Audit, Psad, Alerts, Lynis, WordpresServerSetup, WPVirtualHostSetup

if General.internet_on(): print("Internet connection active")
# Installing non present packages


# Checking if script runs as root
General.output_message('Script is running as root?...')
if os.geteuid() != 0:
    General.error_message("You need to have root privileges to run this script.\nRe-run the script using 'sudo'. Exiting...")
    exit()

# Store global informations
EMAIL_ENABLE = General.answer(
    "To receive notifications from the system and for the correct configuration of some tools, email and Exim4 will"
    " be used ok? \n[if your system is already configured to send mail, you don't have to follow this step] "
)

if EMAIL_ENABLE:
    EMAIL = General.input_message("Email")
else:
    EMAIL = General.input_message("Also if you don't want to configure Exim4 we need your email for othe tools setup\nEmail")

SSH_ENABLE = General.answer("Do you want to enable the SSH service?")
if SSH_ENABLE:
    SSH_PORT = General.input_message(
        "Insert the port on which you want the ssh service to run, it will be used if you want to configure the ssh service")
else:
    SSH_PORT = None

# Main Terminal Menu

Functions = {
    1: [UsersConfig.securing_users_accounts],
    2: [Mail.autamated_email_allerts, EMAIL_ENABLE, EMAIL],
    3: [SSHConfig.ssh, SSH_ENABLE, EMAIL_ENABLE, SSH_PORT, EMAIL],
    4: [Nvidia.nvidia_drivers],
    5: [Ntp.ntp],
    6: [Proc.proc],
    7: [EntropyPool.entropy_pool],
    8: [Ufw.ufw, SSH_ENABLE, SSH_PORT],
    9: [Fail2Ban.fail2ban, EMAIL],
    10: [Aide.aide, EMAIL],
    11: [ClamAv.clamAv, EMAIL],
    12: [Maldet.maldet, EMAIL],
    13: [RkHunter.rkhunter, EMAIL],
    14: [Logwatch.logwatch, EMAIL],
    15: [Audit.auditd, EMAIL],
    16: [Psad.psad, EMAIL],
    17: [Alerts.alerts, EMAIL],
    18: [Lynis.lynis],
    19: [WordpresServerSetup.setup, EMAIL],
    20: [WPVirtualHostSetup.wpVirtualHost, EMAIL]
}

Menu = {
    1: ['Automated Email allerts with exim4', 2],
    2: ['Securing User Accounts', 1],
    3: ['Encrypting and SSH Hardening', 3],
    4: ['Securing your box with a Firewall', 8],
    5: ['Intrusion Detection And Prevention', 9, 16],
    6: ['Application Intrusion Detection And Prevention'],
    7: ['File/Folder Integrity Monitoring', 10],
    8: ['Automated Anti-Virus Scanning', 11, 12],
    9: ['Automated Rootkit Detection', 13],
    10: ['system log analyzer and reporter', 14, 15],
    11: ['Misc', 4],
    12: ['System & Kernel hardening', 5, 6, 7, 17, 18],
    13: ['Setup A wordpress server LAMP Stack ( Linux | Apache | Mysql | Php )', 19],
    14: ['Add a WP website to the server ( VIRTUALHOST ) ', 20]
}



BUILT_MENU = "\n\n"
section_counter = 0
for section, value in Menu.items():
    section_counter += 1
    BUILT_MENU += f"[{str(section_counter)}] {value[0]}\n"
BUILT_MENU += "Select the section number [Q for quit] [* for All]"




try:

    while True:
        section_selected = General.input_message(BUILT_MENU, tag=False)
        print("\n\n")
        if section_selected.strip() == "": continue
        if section_selected == "*": continue
        if section_selected.lower() == "q": break

        for num in Menu[int(section_selected.strip())][1:]:
            function_and_params = Functions[num]
            function = function_and_params[0]
            params = function_and_params[1:]
            function(*params)
except KeyboardInterrupt:
    print()
    exit(0)
except Exception as e:
  traceback.print_exc()

