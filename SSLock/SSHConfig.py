import os
import time
from SSLock import General
from SSLock import UsersConfig
# PermitRootLogin prohibit-password
#
# service sshd restart

# ssh-copy-id -i ~/.ssh/key_rsa.pub user@ip


def ssh(SSH_ENABLE, EMAIL_ENABLE, SSH_PORT, EMAIL):

    f_ssh_config = '/etc/ssh/sshd_config'
    if not SSH_ENABLE or not EMAIL_ENABLE: return
    General.run_cmd("apt install ssh -y")
    options_list = [
        'Port', 'ClientAliveCountMax',
        'ClientAliveInterval', 'LoginGraceTime',
        'MaxAuthTries', 'MaxSessions',
        'MaxStartups', 'PasswordAuthentication',
        'AllowGroups', 'PermitRootLogin'
    ]

    for option in options_list:
        status1 = General.check_lines_in_file(f_ssh_config, option)
        status2 = General.check_lines_in_file(f_ssh_config, '#' + option)
        if not status1 and not status2:
            with open(f_ssh_config, 'a') as file:
                file.write(option + '\n')

    generate_key = General.answer('Do you want enable ssh for some users?')
    if generate_key:
        generate_root_key = General.answer(f'Do you also want to enable ssh for Current user [{General.USER}] ? ')
        if generate_root_key:
            key_path = f'/{General.USER}/.ssh/id_rsa'
            if not os.path.exists(key_path):
                key_pass = General.input_message('Enter a passphrase for the key (empty for no passphrase):')
                General.run_cmd(f'ssh-keygen -C "{EMAIL}" -b 2048 -t rsa -f {key_path} -q -N "{key_pass}"')
                General.warning_message(f'[ALERT] your private key has been sent by email to {EMAIL}, please retrieve and save it, after destroy the email\n')
                time.sleep(3)
                General.run_cmd(f'echo " DANGER here you will find your private key attached for your device, destroy this mail and its contents instantly." | mail -s "Private key for: {General.USER} on {General.HOSTNAME}" {EMAIL} -A {key_path}')
            else:
                General.error_message('A key pair for the current user yet exists')
        else:
            General.change_lines(f_ssh_config,
                                 _19=[
                    '#PermitRootLogin yes',
                    'PermitRootLogin no\n'
                ],
                                 _20=[
                    'PermitRootLogin yes',
                    'PermitRootLogin no\n'
                ]
                                 )

        General.run_cmd('groupadd sshusers')
        General.output_message("which user do you want to have ssh enabled?")
        while True:
            user = General.input_message("User to enable ssh  [S to skip]: ")
            if user.upper() in ['S', 'SKIP']: break

            if not UsersConfig.user_exists(user): General.error_message("User doesn't exists")
            else:
                General.run_cmd(f'usermod -a -G sshusers {user}')
                generate_key_for_user = General.answer(f'[{user}] Do you want a ssh key pair for this user?')
                if generate_key_for_user:
                    key_path = f'/home/{user}/.ssh/id_rsa'
                    if not os.path.exists(f'/home/{user}/.ssh'):
                        os.mkdir(f'/home/{user}/.ssh')
                    if not os.path.exists(key_path):
                        key_pass = General.input_message('Enter a passphrase for the key (empty for no passphrase):')
                        General.run_cmd(f'ssh-keygen -C "{EMAIL}" -b 2048 -t rsa -f {key_path} -q -N "{key_pass}"')
                        General.warning_message(f'[ALERT] your private key has been sent by email to {EMAIL}, please retrieve and save it, after destroy the email\n')
                        time.sleep(3)
                        General.run_cmd(f'echo " DANGER here you will find your private key attached for your device, destroy this mail and its contents instantly." | mail -s "Private key for: {user} on {General.HOSTNAME}" {EMAIL} -A {key_path}')
                    else:
                        General.error_message(f'A key pair for the user "{user}" yet exists')


        General.change_lines(f_ssh_config,
                             _1=[
                         'Port',
                         f"Port {SSH_PORT}\n"
                     ],
                             _2=[
                         '#Port',
                         f"Port {SSH_PORT}\n"
                     ],
                             _3=[
                         'ClientAliveCountMax',
                         "ClientAliveCountMax 0\n"
                     ],
                             _4=[
                         '#ClientAliveCountMax',
                         "ClientAliveCountMax 0\n"
                     ],
                             _5=[
                         'ClientAliveInterval',
                         "ClientAliveInterval 300\n"
                     ],
                             _6=[
                         '#ClientAliveInterval',
                         "ClientAliveInterval 300\n"
                     ],
                             _7=[
                         'LoginGraceTime',
                         "LoginGraceTime 30\n"
                     ],
                             _8=[
                         '#LoginGraceTime',
                         "LoginGraceTime 30\n"
                     ],
                             _9=[
                         'MaxAuthTries',
                         "MaxAuthTries 2\n"
                     ],
                             _10=[
                         '#MaxAuthTries',
                         "MaxAuthTries 2\n"
                     ],
                             _11=[
                         'MaxSessions',
                         "MaxSessions 2\n"
                     ],
                             _12=[
                         '#MaxSessions',
                         "MaxSessions 2\n"
                     ],
                             _13=[
                         'MaxStartups',
                         "MaxStartups 2\n"
                     ],
                             _14=[
                         '#MaxStartups',
                         "MaxStartups 2\n"
                     ],
                             _15=[
                         'PasswordAuthentication',
                         "PasswordAuthentication no\n"
                     ],
                             _16=[
                         '#PasswordAuthentication',
                         "PasswordAuthentication no\n"
                     ],
                             _17=[
                         'AllowGroups',
                         "AllowGroups sshusers\n"
                     ],
                             _18=[
                         '#AllowGroups',
                         "AllowGroups sshusers\n"],

                             )

        General.output_message('These changes have been made to the config')
        General.warning_message('/etc/ssh/sshd_config')
        General.output_message(f'''If u need more advanced options feel free to modify it.
    - Port                      {SSH_PORT};
    - ClientAliveCountMax                0;
    - ClientAliveInterval              300;
    - LoginGraceTime                    30;
    - MaxAuthTries                       2;
    - MaxSessions                        2;
    - MaxStartups                        2;
    - PasswordAuthentication            no;
    - AllowGroups                 sshusers;
    - PermitRootLogin                   no;
''')


        General.output_message('removing all Diffie-Hellman keys that are less than 3072 bits long')
        General.run_cmd("awk '$5 >= 3071' /etc/ssh/moduli | sudo tee /etc/ssh/moduli.tmp")
        General.run_cmd('mv /etc/ssh/moduli.tmp /etc/ssh/moduli')

        response = General.answer('do you want to enable 2FA/MFA for SSH?')
        if response:
            General.warning_message('Note: a user will only need to enter their 2FA/MFA code if they are logging on with their password but not if they are using SSH public/private keys.\n')
            General.run_cmd('apt install libpam-google-authenticator -y')
            General.warning_message('\n[ALERT]  Notice this can not run as root, at the next machine restart RUN "google-authenticator"\n')
            time.sleep(5)
            General.output_message('Select default option (y in most cases) for all the questions it asks and remember to save the emergency scratch codes.')
            time.sleep(2)
            General.run_cmd('echo -e "\nauth       required     pam_google_authenticator.so nullok         # added by $(whoami) on $(date +"%Y-%m-%d @ %H:%M:%S")" | tee -a /etc/pam.d/sshd')
