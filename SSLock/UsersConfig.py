import os
from SSLock import General

"""
useradd -m username
passwd username
usermod -aG sudo username
sudo chsh -s /bin/bash username
"""


def user_exists(user):
    if os.path.exists(f'/home/{user}'): return True
    return False


def create_users():
    while True:
        response = General.answer("Do you want to add a new user?")
        if not response: break
        user_name = General.input_message('New user nick: ')
        if not user_exists(user_name): General.run_cmd(f"useradd -m -d /home/{user_name} -s /bin/bash {user_name}")
        else: General.error_message('User already exists')


def configure_pw_quality():
    f_secure_pass = "/etc/pam.d/common-password"
    if not os.path.exists(f_secure_pass): return
    # Updating password requisites
    if General.check_lines_in_file(
            f_secure_pass,
            'password        requisite                       pam_pwquality.so'
    ):
        General.change_lines(
            f_secure_pass,
            _1=[
                'password        requisite                       pam_pwquality.so',
                "password        requisite                       pam_pwquality.so retry=3 minlen=10 difok=3 ucredit=-1 lcredit=-1 dcredit=-1 ocredit=-1 maxrepeat=3 gecoschec\n"
            ]
        )

        if General.check_lines_in_file(
                f_secure_pass,
                "password        requisite                       pam_pwquality.so retry=3 minlen=10 difok=3 ucredit=-1 lcredit=-1 dcredit=-1 ocredit=-1 maxrepeat=3 gecoschec"
        ):
            General.output_message('''
Password requisites have been update with the following rules:
retry=3         : prompt user 3 times before returning with error.
minlen=10       : the minimum length of the password, factoring in any credits (or debits) from these:
dcredit=-1      : must have at least one digit
ucredit=-1      : must have at least one upper case letter
lcredit=-1      : must have at least one lower case letter
ocredit=-1      : must have at least one non-alphanumeric character
difok=3         : at least 3 characters from the new password cannot have been in the old password
maxrepeat=3     : allow a maximum of 3 repeated characters
gecoschec       : do not allow passwords with the account's name
''')


def sudo_group_config():
    f_sudo_group = '/etc/sudoers'
    response = General.answer('Do you want sudo privileges limited to those who are in a group we specify?')

    if not response: return;

    General.run_cmd('apt install sudo -y')
    General.run_cmd('groupadd sudousers')
    General.output_message('Write the users that you want to be sudo enabled')
    while True:
        user = General.input_message("User [S for skip]: ")
        if user.upper() in ['S', 'SKIP']: break
        if user_exists(user):
            General.run_cmd(f'usermod -a -G sudousers {user}')
        else:
            General.error_message("User doesn't exists")
    General.insert_lines(
        f_sudo_group,
        '%sudousers   ALL=(ALL:ALL) ALL ',
        index_surplus=1,
        anchor_line="# Allow members of group sudo to execute any command"
    )


def securing_users_accounts():
    # Limit Who Can Use sudo

    f_motd = '/etc/motd'
    f_home_dir = '/etc/login.defs'
    f_new_users_conf = '/etc/adduser.conf'
    f_strong_pass_conf = '/etc/pam.d/login'

    response = General.answer(
"""
You can secure user accounts by doing this:
1. Adding warning to the motd
2. Securing /home directory
3. Preventing Bruteforce and Password attacks
4. Force Accounts To Use Secure Passwords
5. Configure sudo group
Do you want to do this steps for secure users accounts?""")
    if not response: return

    # --- Adding warning to the motd
    General.output_message('Adding Warning to the motd..')
    with open(f_motd, 'w') as file: file.write('Warning! Authorized Users Only! All others will be prosecuted.')

    # --- Securing /home directory
    General.output_message('Protecting /home directory..')
    General.change_lines(f_home_dir,
                         _1=['UMASK		022',
                     'UMASK		027\n'],
                         _2=['PASS_MAX_DAYS	99999',
                     'PASS_MAX_DAYS   30\n'],
                         _3=['PASS_MIN_DAYS	0',
                     'PASS_MIN_DAYS   1\n'],
                         _4=['PASS_WARN_AGE   7',
                     'PASS_WARN_AGE   7\n'],
                         )

    General.output_message('Making the home  directories of new users private..')
    General.change_lines(f_new_users_conf, _1=['DIR_MODE=0755', 'DIR_MODE=0700\n'])

    # --- Preventing Bruteforce and Password attacks
    General.output_message('Preventing Bruteforce and Password attacks, after')
    General.warning_message('5 failed attempts ')
    General.output_message('you will not be able to log in for 20 minutes')
    General.insert_lines(
        f_strong_pass_conf,
        'auth required pam_tally2.so deny=4',
        'even_deny_root unlock_time=1200',
        index_surplus=1,
        anchor_line='auth [success=ok new_authtok_reqd=ok ignore=ignore user_unknown=bad default=die] pam_securetty.so'
    )

    # --- Force Accounts To Use Secure Passwords
    General.run_cmd('apt install libpam-pwquality -y')
    General.output_message('Configuring pw quality')
    configure_pw_quality()

    create_users()

    # --- Configure sudo group
    sudo_group_config()



