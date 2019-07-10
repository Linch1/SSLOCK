import os
from urllib.error import *
from urllib.request import urlopen
from datetime import datetime
import subprocess
import socket
import getpass
from subprocess import DEVNULL, STDOUT, check_call
import sys
import time
import threading
from os import listdir
import tarfile

end_cmds = []

def run_cmd(*cmds):
    for cmd in cmds:
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        output, errors = p.communicate()
        if not errors is None:
            print(errors)


class Progressbar:

    def __init__(self, text=' '):
        self.status = True
        self.text_ = text

    def bar_char(self, char):
        sys.stdout.write('\b' * (len(self.text_) + len(char) + 10))
        sys.stdout.flush()
        sys.stdout.write(' ' * (len(self.text_) + len(char) + 10))
        sys.stdout.write('\b' * (len(self.text_) + len(char) + 10))
        sys.stdout.write(self.text_ + char)
        sys.stdout.flush()

    def start(self, chars=('|', '/', '-', '\\')):
        time_ = 0.5
        while self.status:
            for char in chars:
                if not self.status:
                    break
                self.bar_char(char)
                time.sleep(time_)

    def run(self, chars=()):
        self.status = True
        if len(chars) != 0:
            t = threading.Thread(target=self.start, args=[chars])
        else:
            t = threading.Thread(target=self.start)

        t.daemon = True
        t.start()

    def text(self, text):
        self.text_ = text

    def stop(self):
        self.status = False
        time.sleep(1)
        sys.stdout.write('\b' * (len(self.text_) + 10))
        sys.stdout.flush()
        sys.stdout.write(' ' * (len(self.text_) + 10))
        sys.stdout.flush()
        sys.stdout.write('\b' * (len(self.text_) + 10))
        sys.stdout.flush()

    def auto(self, text="", function=None, args=(), chars=()):
        self.text_ = text
        if len(chars) != 0:
            self.run(chars=chars)
        else:
            self.run()
        if len(args) == 1:
            function(args[0])
        else:
            function(*args)
        self.stop()


def output_message(text):
    print(colored(text, output_color), end='')


def internet_on():
    try:
        urlopen('http://216.58.192.142', timeout=1)
        return
    except URLError as err:
        exit('No internet connection')


bar = Progressbar()
print("""

         .:+shdmNMMMMMMNmdhs+:.         
     -MMNMMMMMMMMMMMMMMMMMMMMMMNMM-     
    `MMMMMMMMMMMMMMMMMMMMMMMMMMMMMM     
    `MMMMMMMMMMMNMMMMMMNMMMMMMMMMMM     
    `MMMMMMMMMy`-SSLock-`yMMMMMMMMM     
    `MMMMMMMMMN .MMMMMM. NMMMMMMMMM     
    `MMMMMMMMMm :MMMMMM: mMMMMMMMMM     
    `MMMMMMMMMN+yMMMMMMy+NMMMMMMMMM     
    `MMMMMMMN-............-NMMMMMMM     
    `MMMMMMMm              mMMMMMMM     
    `MMMMMMMm              mMMMMMMM     
     dMMMMMMm              mMMMMMMd     
     .NMMMMMm              mMMMMMN.     
      .mMMMMN-............-NMMMMm.      
       `sMMMMMMMMMMMMMMMMMMMMMMs`       
         -dMMMMMMMMMMMMMMMMMMd-         
           :mMMMMMMMMMMMMMMm:           
             :dMMMMMMMMMMd:             
               -yMMMMMMy-               
                 `+mm+`                 
""")

internet_on()

try:
    from termcolor import colored, cprint
except:
    bar.auto('Installing python pacakge..', run_cmd, args=['pip3 install termcolor'])
try:
    from pyfiglet import figlet_format
except:
    bar.auto('Installing python pacakge..', run_cmd, args=['pip3 install pyfiglet'])
try:
    from colorama import Fore, Back, Style
except:
    bar.auto('Installing python pacakge..', run_cmd, args=['pip3 install colorama'])

from termcolor import colored, cprint
from colorama import Fore, Back, Style
from pyfiglet import figlet_format


print(Style.BRIGHT)

input_color = 'yellow'
output_color = 'blue'

ssh_service_is_configured = False
ssh_port = ''
email = ''
hostname = socket.gethostname()
username = getpass.getuser()


def green_message(text):
    print(colored(text, 'green'))


def status_ok_message(text):
    output_message(text)
    task_status_ok()


def status_error_message(text):
    output_message(text)
    task_status_error()


def input_message(text):
    print(colored(text, input_color), end='')


def output_message_alone(text):
    print(colored(text, output_color))


def task_status_ok():
    print(' [', colored('OK', 'green'), ']')


def task_status_error():
    print(' [', colored('ERROR', 'red'), ']')


def error_message(text):
    print(colored(text, 'red'))


def user_exists(user):
    if os.path.exists(f'/home/{user}'):
        return True
    return False


def check_answer(question):
    print(colored(question + '[Y/N] ', input_color), end='')
    response = input(' ')
    response = response.upper().strip()
    while response not in ['Y', 'YES', 'N', 'NO']:
        print(colored('Please write Y or N', 'red'))
        print(colored(question + '[Y/N] ', input_color), end='')
        response = input(' ')
        response = response.upper().strip()
    if response in ['Y', 'YES']:
        return True
    elif response in ['N', 'NO']:
        return False


def check_lines_in_file(file_path, *phrases):
    phrases = list(phrases)

    for index, phrase in enumerate(phrases):
        phrases[index] = frozenset(phrase.split())

    with open(file_path, 'r') as file:
        file_lines = file.readlines()
        for index, line in enumerate(file_lines):
            file_lines[index] = frozenset(line.split())

    for phrase in phrases:
        is_subset = False
        for line in file_lines:
            if phrase.issubset(line):
                is_subset = True
        if is_subset == False:
            return False
    return True


def change_lines(file_path, **lines):
    lines_to_change = dict()

    for index, lines in lines.items():
        previous_line = lines[0]
        new_line = lines[1]
        previous_line = frozenset(previous_line.strip().split())
        lines_to_change[previous_line] = new_line

    with open(file_path, 'r') as file:
        file_lines = file.readlines()
        for index, line in enumerate(file_lines):
            file_lines[index] = frozenset(line.split())

    with open(file_path, 'r') as file:
        file_lines_to_change = file.readlines()
        for line_to_change in lines_to_change:
            for index_to_change, file_line in enumerate(file_lines):
                if line_to_change.issubset(file_line):
                    file_lines_to_change[index_to_change] = lines_to_change[line_to_change]

    with open(file_path, 'w') as file:
        for line in file_lines_to_change:
            file.write(line)


def insert_lines(file_path, *lines, index_surplus=1, anchor_line=None):
    new_lines = '\n'

    for line in lines:
        new_lines += line + '\n'

    status = check_lines_in_file(file_path, *lines)
    if not check_lines_in_file(file_path, *lines):
        with open(file_path, 'r') as file:
            lines = file.readlines()
            for index, line in enumerate(lines):
                if set(line.strip().split()) == set(anchor_line.strip().split()):
                    lines.insert(index + index_surplus, new_lines)

        with open(file_path, 'w') as file:
            for line in lines:
                file.write(line)

def create_users():
    question = "Do you want to add a new user?"
    response = check_answer(question)
    if response:
        while response:
            input_message('New user nick: ')
            user_name = input(' ')
            if not user_exists(user_name):
                bar.auto('Adding new user', run_cmd,
                         args=[f'useradd -m -d /home/{user_name} -s /bin/bash {user_name}'],
                         chars=['.', '..', '...'])
                status_ok_message('Added User')
            else:
                status_error_message('User already exists')

            response = check_answer(question)


def autamated_email_allerts():
    global username, hostname, email
    # Exim4 As MTA With Implicit TLS

    print()
    response = check_answer("to receive notifications from the system and for the correct configuration of some tools, email and Exim4 will be used ok? \nNote: if your system is already configured to send mail, you don't have to follow this step")
    file_path = '/etc/exim4/update-exim4.conf.conf'
    file_path_3 = '/etc/exim4/exim4.conf.template'
    file_path_4 = '/var/lib/exim4/config.autogenerated'

    file_path_1 = '/etc/exim4/passwd.client'
    file_path_2 = '/etc/exim4/exim4.conf.localmacros'
    if response:
        bar.auto('Installing exim4 openssl ca-certificates..', run_cmd, args=['apt install exim4 openssl ca-certificates -y'])
        status_ok_message('Installed Exim')

        bar.text('Editing configuration files..')
        bar.run()
        run_cmd('chown root:Debian-exim /etc/exim4/passwd.client')
        run_cmd('chown 640 /etc/exim4/passwd.client')

        if not os.path.exists('/usr/share/doc/exim4-base/examples/exim-gencert'):
            run_cmd('bash /usr/share/doc/exim4-base/examples/exim-gencert')

        with open(file_path_2, 'w') as file:
            file.write('''
    MAIN_TLS_ENABLE = 1
    REMOTE_SMTP_SMARTHOST_HOSTS_REQUIRE_TLS = *
    TLS_ON_CONNECT_PORTS = 465
    REQUIRE_PROTOCOL = smtps
    IGNORE_SMTP_LINE_LENGTH_LIMIT = true
                ''')

        run_cmd(f'wget -q https://raw.githubusercontent.com/TheeBlind/Exim4_Gmail_conf/master/nconf/config.autogenerated -O {file_path_4}' )
        run_cmd(f'wget -q https://raw.githubusercontent.com/TheeBlind/Exim4_Gmail_conf/master/nconf/exim4.conf.template -O {file_path_3}')
        run_cmd(f'wget -q https://raw.githubusercontent.com/TheeBlind/Exim4_Gmail_conf/master/nconf/update-exim4.conf.conf -O {file_path}')


        local_ip = subprocess.check_output(['hostname', '-I'], stderr=subprocess.STDOUT)
        local_ip = str(local_ip).strip("b'n\\ ")

        change_lines(file_path_3,
                     _1=[
                         '* changeme Ffrs',
                         f"* {local_ip}@{username}.{hostname} Ffrs\n"
                     ])

        change_lines(file_path_4,
                     _1=[
                         '* chengeme Ffrs',
                         f"* {local_ip}@{username}.{hostname} Ffrs\n"
                     ])



        run_cmd('update-exim4.conf')
        run_cmd('systemctl restart exim4')
        bar.stop()
        status_ok_message('Correctly edited configuration')
        run_cmd(f"""echo "Automatic SSlock notification test, if you received this mail, you can go ahead in the setup. if you have received this mail by mistake, please delete it." | mail -s 'Test!' {email}""")
        output_message('Mail setup')
        task_status_ok()
        response = check_answer(f'We have sent a test mail to the address {email}. Have you recived it?\nCheck the spam folder!')
        if not response:
            error_message('Contact us for solve the problem.')
            time.sleep(3)


def securing_users_accounts():
    # Limit Who Can Use sudo
    question = 'Do you want secure users accounts?'
    file_path = '/etc/sudoers'
    file_path_1 = '/etc/motd'
    file_path_2 = '/etc/login.defs'
    file_path_3 = '/etc/adduser.conf'
    file_path_5 = '/etc/pam.d/login'
    file_path_4 = "/etc/pam.d/common-password"
    error = 'Fatal Error: sudo will have to be configured manually'
    response = check_answer(question)
    if response:

        output_message('Adding Warning to the motd..')
        with open(file_path_1, 'w') as file:
            file.write('Warning! Authorized Users Only! All others will be prosecuted.')
        task_status_ok()

        output_message('Protecting /home directory..')
        change_lines(file_path_2,
                     _1=['UMASK		022',
                        'UMASK		027\n'],
                     _2=['PASS_MAX_DAYS	99999',
                         'PASS_MAX_DAYS   30\n'],
                     _3=['PASS_MIN_DAYS	0',
                         'PASS_MIN_DAYS   1\n'],
                     _4=['PASS_WARN_AGE   7',
                         'PASS_WARN_AGE   7\n'],
                     )
        task_status_ok()

        output_message('Making the home  directories of new users private..')
        change_lines(file_path_3, _1=['DIR_MODE=0755', 'DIR_MODE=0700\n'])
        task_status_ok()

        create_users()


        output_message('Preventing Bruteforce and Password attacs, after')
        print(colored(' 5 failed attempts ', 'red'), end='')
        output_message('you will not be able to log in for ')
        print(colored('20 minutes', 'red'))

        insert_lines(file_path_5, 'auth required pam_tally2.so deny=4', 'even_deny_root unlock_time=1200',
                     index_surplus=1,
                     anchor_line='auth [success=ok new_authtok_reqd=ok ignore=ignore user_unknown=bad default=die] pam_securetty.so')

        # Force Accounts To Use Secure Passwords

        bar.auto('Installing pw quality..', run_cmd, args=['apt install libpam-pwquality -y'])

        output_message('Configuring pw quality')

        if os.path.exists(file_path_4):
            if check_lines_in_file(file_path_4,
                                   'password        requisite                       pam_pwquality.so'):
                change_lines(file_path_4,
                             _1=[
                                 'password        requisite                       pam_pwquality.so',
                                 "password        requisite                       pam_pwquality.so retry=3 minlen=10 difok=3 ucredit=-1 lcredit=-1 dcredit=-1 ocredit=-1 maxrepeat=3 gecoschec\n"
                             ])
            task_status_ok()
            with open(file_path, 'r') as file:
                if check_lines_in_file(file_path_4,
                                       "password        requisite                       pam_pwquality.so retry=3 minlen=10 difok=3 ucredit=-1 lcredit=-1 dcredit=-1 ocredit=-1 maxrepeat=3 gecoschec"):
                    print('''
    
    
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


        question = 'Do you want sudo privileges limited to those who are in a group we specify?'
        response = check_answer(question)
        check_attempt = 0
        if response:
            while check_attempt < 2:
                bar.auto('Installing sudo..', run_cmd, args=['apt install sudo -y'])
                status_ok_message('Installed Sudo')
                if 'sudo is already the newest version' in str(subprocess.check_output(['apt', 'install', 'sudo'], stderr=subprocess.STDOUT)).strip("b'"):
                    run_cmd('groupadd sudousers')

                    input_message('Write the users that you want to be sudo enabled')
                    print()
                    answer = "User [S for skip]: "
                    input_message(answer)
                    user = input(' ')
                    while user.upper() not in ['S', 'SKIP']:
                        if user_exists(user):

                            bar.auto('Adding user', run_cmd,
                                     args=[f'usermod -a -G sudousers {user}'],
                                     chars=['.', '..', '...'])
                            status_ok_message('Added User')
                        else:
                            status_error_message("User doesn't exists")
                        input_message(answer)
                        user = input(' ')

                    insert_lines(file_path, '%sudousers   ALL=(ALL:ALL) ALL ', index_surplus=1, anchor_line="# Allow members of group sudo to execute any command")

                    break
                else:
                    check_attempt += 1
                    if check_attempt == 2:
                        print(colored(error, 'red'))


#  =====================================
# !                                     !
# !  Installation & Configuration SSH   !
# !                                     !
#  =====================================

def ssh():
    global ssh_service_is_configured, ssh_port, email, hostname, username

    print()
    response = check_answer('Do you need SSH service on this machine?')
    ssh_service_is_configured = response
    file_path = '/etc/ssh/sshd_config'
    if response:

        bar.auto('Installation SSH..', run_cmd, args=['apt install ssh -y'])
        status_ok_message('SSH Installed')

        options_list = ['Port', 'ClientAliveCountMax', 'ClientAliveInterval', 'LoginGraceTime', 'MaxAuthTries',
                        'MaxSessions', 'MaxStartups', 'PasswordAuthentication', 'AllowGroups', 'PermitRootLogin']

        for option in options_list:
            status1 = check_lines_in_file(file_path, option)
            status2 = check_lines_in_file(file_path, '#' + option)

            if not status1 and not status2:
                with open(file_path, 'a') as file:
                    file.write(option + '\n')

        generate_key = check_answer('Do you want enable ssh for some users?')
        if generate_key:
            generate_root_key = check_answer('Do you also want to enable ssh for ROOT?')
            if generate_root_key:

                key_path = f'/{username}/.ssh/id_rsa'
                if not os.path.exists(key_path):
                    bar.auto('Generating keys for root', run_cmd,
                             args=[f'ssh-keygen -C "{email}" -b 2048 -t rsa -f {key_path} -q -N ""'],
                             chars=['.', '..', '...'])
                    status_ok_message('Generated keys')

                    error_message(f'[ALERT] your private key has been sent by email to {email}, please retrieve and save it, after destroy the email')
                    time.sleep(3)
                    run_cmd(f'echo " DANGER here you will find your private key attached for your device, destroy this mail and its contents instantly." | mail -s "Private key for: {username} on {hostname}" {email} -A {key_path}')
                else:
                    status_error_message('A key pair for the root yet exists')
            else:
                change_lines(file_path,
                             _19=[
                                 '#PermitRootLogin yes',
                                 'PermitRootLogin no\n'],
                             _20=[
                                 'PermitRootLogin yes',
                                 'PermitRootLogin no\n']
                             )

            run_cmd('groupadd sshusers')

            input_message("which user do you want to have ssh enabled?")
            print()
            answer = "User to enable ssh  [S to skip]: "

            input_message(answer)
            user = input(' ')
            while user.upper() not in ['S', 'SKIP']:
                if not user_exists(user):
                    status_error_message("User doesn't exists")
                else:

                    run_cmd(f'usermod -a -G sshusers {user}')
                    generate_key_for_user = check_answer(f'[{user}] Do you want a ssh key pair for this user?')

                    if generate_key_for_user:
                        key_path = f'/home/{user}/.ssh/id_rsa'
                        if not os.path.exists(f'/home/{user}/.ssh'):
                            os.mkdir(f'/home/{user}/.ssh')

                        if not os.path.exists(key_path):
                            bar.auto(f'Generating keys for {user}', run_cmd,
                                     args=[f'ssh-keygen -C "{email}" -b 2048 -t rsa -f {key_path} -q -N ""'],
                                     chars=['.', '..', '...'])
                            status_ok_message('Generated keys')

                            error_message(f'[ALERT] your private key has been sent by email to {email}, please retrieve and save it, after destroy the email')
                            time.sleep(3)
                            run_cmd(f'echo " DANGER here you will find your private key attached for your device, destroy this mail and its contents instantly." | mail -s "Private key for: {user} on {hostname}" {email} -A {key_path}')
                        else:
                            status_error_message(f'A key pair for the user "{user}" yet exists')
                input_message(answer)
                user = input(' ')

        input_message('What port do you want to use for the SSH service?')
        ssh_port = input(' ')


        change_lines(file_path,
                     _1=[
                         'Port',
                         f"Port {ssh_port}\n"
                     ],
                     _2=[
                         '#Port',
                         f"Port {ssh_port}\n"
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

        output_message_alone(f'''
        These changes have been made to the config '/etc/ssh/sshd_config'.
        If u need more advanced options feel free to modify it.

            - Port                      {ssh_port};
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

        output_message('removing all Diffie-Hellman keys that are less than 3072 bits long')
        run_cmd("awk '$5 >= 3071' /etc/ssh/moduli | sudo tee /etc/ssh/moduli.tmp")
        run_cmd('mv /etc/ssh/moduli.tmp /etc/ssh/moduli')
        task_status_ok()

        response = check_answer('do you want to enable 2FA/MFA for SSH?')
        if response:
            output_message_alone('note: a user will only need to enter their 2FA/MFA code if they are logging on with their password but not if they are using SSH public/private keys.')
            bar.auto('Installing Authenticator..', run_cmd, args=['apt install libpam-google-authenticator -y'])
            status_ok_message('Installed Authenticator')
            error_message('\n[ALERT]  Notice this can not run as root, at the next machine restart RUN "google-authenticator"')
            time.sleep(5)
            output_message('Select default option (y in most cases) for all the questions it asks and remember to save the emergency scratch codes.')
            time.sleep(2)
            run_cmd('echo -e "\nauth       required     pam_google_authenticator.so nullok         # added by $(whoami) on $(date +"%Y-%m-%d @ %H:%M:%S")" | tee -a /etc/pam.d/sshd')


def nvidia_drivers():
    # Installation invidia driver
    response = check_answer('Do you need nvidia drivers?')
    if response:
        print(colored('Since the nvidia-driver package in Debian is proprietary, we need to enable contrib and non-free component in /etc/apt/sources.list file',output_color))
        bar.auto('Installing common software properties..', run_cmd, args=['apt install software-properties-common'])
        status_ok_message('Installed common software properties ')
        run_cmd('add-apt-repository contrib')
        run_cmd('add-apt-repository non-free')
        bar.auto('Updating..', run_cmd, args=['apt update -y'])
        bar.auto('Installing drivers. Will be aviable at next reboot..', run_cmd, args=['apt install nvidia-driver -y'])
        status_ok_message('Installed nvidia drivers')

def ntp():

    # installing NTP client and keeping server time in-sync

    question = 'Install NTP client and keeping server time in-sinc ?'
    error = 'Fatal Error: NTP will have to be configured manually'
    response = check_answer(question)
    check_attempt = 0
    file_path = '/etc/ntp.conf'
    if response:
        while response and check_attempt < 2:
            bar.auto('Installing NTP..', run_cmd, args=['apt install ntp -y'])
            status_ok_message('Installed NTP')
            if os.path.exists('/etc/ntp.conf'):
                output_message('Configuring NTP')
                with open(file_path, 'w') as file:
                    file.write(f'''
                # added by debian9_Hardening.py on {datetime.today().strftime('%Y-%m-%d')} @ {datetime.now().strftime(
                        '%H:%M:%S')}        
    
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

                # Restarting NTP service
                run_cmd('service ntp restart')
                if 'pool.ntp.org' in str(subprocess.check_output(['ntpq', '-p'], stderr=subprocess.STDOUT)).strip("b'"):
                    pass
                    task_status_ok()
                else:
                    error_message(error)
                break
            else:
                error_message('Error, restarting current process')
                check_attempt += 1
                if check_attempt == 2:
                    error_message(error)

def proc():
    # Securing /proc | /proc mounted with hidepid=2 so users can only see information about their processes
    question = 'Securing /proc?'
    error = 'Fatal Error: PROC will have to be configured manually'
    file_path = "/etc/ntp.conf"
    response = check_answer(question)
    check_attempt = 0

    if response:
        while response and check_attempt < 2:
            output_message('Configuring proc')
            if os.path.exists(file_path):
                with open(file_path, 'a') as file:

                    file.write(f'''
                   # added by debian9_Hardening.py on {datetime.today().strftime('%Y-%m-%d')} @ {datetime.now().strftime(
                        '%H:%M:%S')}       
                   proc     /proc     proc     defaults,hidepid=2     0     0
                           ''')

                # Process check
                if 'proc     /proc     proc     defaults,hidepid=2     0     0' in str(subprocess.check_output(['cat', file_path], stderr=subprocess.STDOUT)).strip("b'"):
                    pass
                    task_status_ok()
                else:
                    print(colored(error, 'red'))
                break
            else:
                print(colored('Error, restarting current process', 'red'))
                check_attempt += 1
                if check_attempt == 2:
                    print(colored(error, 'red'))



def entropy_pool():
    # More Secure Random Entropy Pool (WIP)
    question = 'Do you want More Secure Random Entropy Pool (WIP)?'
    error = 'Fatal Error: rng-tools will have to be configured manually'
    response = check_answer(question)
    check_attempt = 0

    if response:
        while response and check_attempt < 2:
            bar.auto('Installing rng tools..', run_cmd, args=['apt install rng-tools -y'])
            status_ok_message('Installed rng tools')
            # Process check
            if 'rng-tools is already the newest version' in str(subprocess.check_output(['apt', 'install', 'rng-tools'], stderr=subprocess.STDOUT)).strip("b'"):

                run_cmd('echo "HRNGDEVICE=/dev/urandom" >> /etc/default/rng-tools')
                run_cmd('systemctl start rng-tools')
                if 'Active' in str(subprocess.check_output(['systemctl', 'status', 'rng-tools'], stderr=subprocess.STDOUT)).strip("b'"):
                    status_ok_message('Rng tools Running')
                    break
                else:
                    error_message(error)
                break
            else:
                error_message('Error, restarting current process')
                check_attempt += 1
                if check_attempt == 2:
                    error_message(error)

def ufw():

    # Firewall With UFW
    question = 'Do you want install and configure UFW?'
    file_path = '/etc/ufw/applications.d/smtptls'
    error = 'Fatal Error: UFW will have to be configured manually'
    response = check_answer(question)
    check_attempt = 0
    ufw_service_status = response
    if response:
        while response and check_attempt < 2:
            bar.auto('Installing Firewall..', run_cmd, args=['apt install ufw -y'])
            status_ok_message('Installed Firewall')
            # Process check
            if 'ufw is already the newest version' in str(subprocess.check_output(['apt', 'install', 'ufw'], stderr=subprocess.STDOUT)).strip("b'"):
                bar.auto('Configuring Firewall..', run_cmd, args=[
                    'ufw default deny outgoing comment "deny all outgoing traffic"',
                    'ufw default deny incoming comment "deny all incoming traffic"',
                    'ufw allow out 53 comment "allow DNS calls out"',
                    'ufw allow out 123 comment "allow NTP out"',
                    'ufw allow out http comment "allow HTTP traffic out"',
                    'ufw allow out https comment "allow HTTPS traffic out"',
                    'ufw allow out whois comment "allow whois"'
                    'ufw allow out 25 comment "allow MAIL out"'
                ])
                with open(file_path, 'w') as file:
                    file.write('''
    [SMTPTLS]
    title=SMTP through TLS
    description=This opens up the TLS port 465 for use with SMPT to send e-mails.
    ports=465/tcp
                    ''')
                run_cmd('ufw allow out smtptls comment "open TLS port 465 for use with SMPT to send e-mails"')
                output_message('''
                
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
                output_message('Starting Firewall')
                run_cmd('ufw start')
                task_status_ok()

                break
            else:
                error_message('Error, restarting current process')
                check_attempt += 1
                if check_attempt == 2:
                    error_message(error)

    if ufw_service_status:
        # ufw ssh rules

        if ssh_service_is_configured:
            question = '(UFW) Do  you need ssh rule?'
            response = check_answer(question)
            check_attempt = 0
            if response:
                bar.auto('Adding rules', run_cmd,
                         args=[f'ufw limit in {ssh_port} comment "allow SSH connections in"'],
                         chars=['.', '..', '...'])
                status_ok_message('Added Rules')

        # ufw ftp out rule

        question = '(UFW) Do you need ftp out rule?'
        response = check_answer(question)
        check_attempt = 0
        if response:
            bar.auto('Adding rules', run_cmd,
                     args=['ufw allow out ftp comment "allow FTP traffic out"'],
                     chars=['.', '..', '...'])
            status_ok_message('Added Rules')


        # ufw dhcp rule

        question = '(UFW) Are you using DHCP?'
        response = check_answer(question)
        check_attempt = 0
        if response:
            bar.auto('Adding rules', run_cmd,
                     args=['ufw allow out 68 comment "allow the DHCP client to update"'],
                     chars=['.', '..', '...'])
            status_ok_message('Added Rules')

        run_cmd('ufw enable')


def fail2ban():
    global email
    # Application Intrusion Detection And Prevention With Fail2Ban
    question = 'Do you want to install and configure Fail2Ban?'
    file_path = '/etc/fail2ban/jail.local'
    jail_error = 'Fatal Error: Fail2Ban Jail will have to be configured manually'
    error = 'Fatal Error: Fail2Ban will have to be configured manually'
    response = check_answer(question)
    check_attempt = 0
    if response:

        while check_attempt < 2:
            bar.auto('Installing Intrusion and detection tools..', run_cmd, args=['apt install fail2ban -y'])
            status_ok_message('Installed Intrusion and detection tools')

            if 'fail2ban is already the newest version' in str(subprocess.check_output(['apt', 'install', 'fail2ban'], stderr=subprocess.STDOUT)).strip("b'"):
                bar.auto('Running Intrusion and detection tools..', run_cmd, args=['systemctl start fail2ban',
                                                                                   'systemctl enable fail2ban'])

                status_ok_message('Tools are running')

                with open(file_path, 'w') as file:
                    input_message('What is you lan segment? (ex. 192.168.1.1/24) :')
                    lan_segment = input(' ')
                    file.write(f'''
    [DEFAULT]
    # the IP address range we want to ignore
    ignoreip = 127.0.0.1/8 {lan_segment}
    
    # who to send e-mail to
    destemail = {email}
    
    # who is the email from
    sender = {email}
    
    # since we're using exim4 to send emails
    mta = mail
    
    # get email alerts
    action = %(action_mwl)s
                ''')
                status_ok_message('Configuring Intrusion and detection tools')
                jail_status = check_answer('Do You need a jail for SSH that tells fail2ban to look at SSH logs and use ufw to ban/unban IPs ?')
                if jail_status:
                    with open('/etc/fail2ban/jail.d/ssh.local', 'w') as jail_file:
                        jail_file.write('''
    [sshd]
    enabled = true
    banaction = ufw
    port = ssh
    filter = sshd
    logpath = %(sshd_log)s
    maxretry = 5
                        ''')

                bar.auto('Reloading Intrusion and detection tools..', run_cmd, args=['fail2ban-client start',
                                                                                   'fail2ban-client reload'])
                status_ok_message('Tools reloaded')

                if jail_status:
                    # Process check for jail
                    if set('Number of jail:\\t1\\n`-'.split()).issubset(set(str(subprocess.check_output(['fail2ban-client', 'status'], stderr=subprocess.STDOUT)).strip("b'").split())) :
                        run_cmd('fail2ban-client add sshd')
                        pass
                    else:
                        error_message(jail_error)
                break
            else:
                check_attempt += 1
                if check_attempt == 2:
                    error_message(error)


def aide():
    global email
    # File/Folder Integrity Monitoring With AIDE

    question = 'Do you want Monitoring  File/Folder Integrity With AIDE?'
    file_path = '/etc/default/aide'
    error = 'Fatal Error: AIDE will have to be configured manually'
    response = check_answer(question)
    check_attempt = 0
    if response:
        while check_attempt < 2:
            bar.auto('Installing File/Folder Monitoring tools..', run_cmd, args=['apt install aide -y'])

            if 'aide is already the newest version' in str(subprocess.check_output(['apt', 'install', 'aide'], stderr=subprocess.STDOUT)).strip("b'"):
                output_message('Configuration File/Folder Monitoring tools..')
                change_lines(file_path,
                                 _1=[
                                     'MAILTO=root',
                                     f'MAILTO={email}\n'
                                 ],
                                 _2=[
                                     '#CRON_DAILY_RUN=yes',
                                     'CRON_DAILY_RUN=yes\n'
                                 ]
                             )
                task_status_ok()

                response = check_answer("Aide, for work, needs to create a new database and install it. Do it now!  (this process require time..)")

                if response:
                    bar.auto('Running Aide tasks..', run_cmd, args=['aideinit -y -f'])
                else:
                    end_cmds.append('aideinit -y -f')
                break
            else:
                check_attempt += 1
                if check_attempt == 2:
                    print(colored(error, 'red'))


def clamAv():
    global email
    # Anti-Virus Scanning With ClamAV

    question = 'Do you want to use ClamAV for Anti-virus Scanning with root permissions?'
    file_path = '/etc/clamav/freshclam.conf'
    error = 'Fatal Error: ClamAV will have to be configured manually'
    response = check_answer(question)
    check_attempt = 0
    if response:
        while check_attempt < 2:
            bar.auto('Installing Anti-virus Scanning tools..', run_cmd, args=[' apt install clamav clamav-freshclam -y'])
            status_ok_message('Installed Anti-virus Scanning tools')
            print()

            if 'clamav is already the newest version' in str(subprocess.check_output(['apt', 'install', 'clamav'], stderr=subprocess.STDOUT)).strip("b'"):

                change_lines(file_path,
                                 _1=[
                                    '# Check for new database 24 times a day',
                                     '# Check for new database 1 times a day\n'
                                 ],
                                 _2=[
                                     'Checks 24',
                                     'Checks 1\n'
                                 ]
                             )
                run_cmd('freshclam -v')

                input_message("Using clamscan as root is dangerous because if a file is in fact a virus there is risk that it could use the root privileges.\n"
                              "You can create another user by writing [U] \nPlease chose a user that can run clamscan:")
                user = input(' ')
                while not user_exists(user):
                    if user.upper() == 'U':
                        create_users()
                    else:
                        status_error_message("User doesn't exists")
                        output_message_alone('For create a new user type [U]')
                    input_message('Chose a user that can run clamscan:')
                    user = input(' ')

                file_path_1 = f'/home/{user}/clamscan_daily.sh'

                dir_to_scan = ''
                all_directories_exists = False
                while not all_directories_exists:
                    all_directories_exists = True
                    input_message('Which direcotry should be scanned by clamAV? (ex. /var/www /var/vmail): ')
                    dir_to_scan = input(' ')

                    for dir in dir_to_scan.split():
                        if not os.path.exists(dir):
                            status_error_message(f"The directory {dir} doesn't exists, select another path")
                            all_directories_exists = False
                output_message('Configuration Anti-virus Scanning tools..')
                with open(file_path_1, 'w') as file:
                    file.write('''
    #!/bin/bash
    LOGFILE="/var/log/clamav/clamav-$(date +'%Y-%m-%d').log";
    EMAIL_MSG="Please see the log file attached.";
    EMAIL_FROM="''' + email + '''";
    DIRTOSCAN="''' + dir_to_scan + '''";
    
    for S in ${DIRTOSCAN}; do
     DIRSIZE=$(du -sh "$S" 2>/dev/null | cut -f1);
    
     echo "Starting a daily scan of "$S" directory.
     Amount of data to be scanned is "$DIRSIZE".";
    
     clamscan -ri "$S" >> "$LOGFILE";
    
     # get the value of "Infected lines"
     MALWARE=$(tail "$LOGFILE"|grep Infected|cut -d" " -f3);
    
     # if the value is not equal to zero, send an email with the log file attached
     if [ "$MALWARE" -ne "0" ];then
     # using heirloom-mailx below
     echo "$EMAIL_MSG"|mail -A "$LOGFILE" -s "Malware Found" "$EMAIL_FROM";
    fi 
    done
    
    exit 0
                    ''')
                task_status_ok()
                run_cmd('chmod 0755 /root/clamscan_daily.sh')
                run_cmd('ln /root/clamscan_daily.sh /etc/cron.daily/clamscan_daily')

                if 'Active' in str(subprocess.check_output(['service', 'clamav-freshclam', 'status'], stderr=subprocess.STDOUT)):
                    status_ok_message('clamav-freshclam Active')

                run_cmd('service clamav-freshclam start')

                output_message_alone('Running first scan for check if all is ok..')



                bar.text('Scanning..')
                bar.run()
                try:
                    output = set(str(subprocess.check_output(['clamscan', '-r', dir_to_scan], stderr=subprocess.STDOUT)).strip("b'").split())
                    bar.stop()
                except subprocess.CalledProcessError as e:
                    output = e.output
                    error_message('[SCAN ERROR]' + output)
                    output_message_alone('To execute manually the script\n'
                                         'run the below commands:\n\n'
                                         'service clamav-freshclam start\n'
                                         'clamscan -r <directories to scan>\n')


                expected_partial_output = set('OK\\n\\n----------- SCAN SUMMARY -----------\\nKnown'.split())

                if not expected_partial_output.issubset(output) :
                    print(colored(error, 'red'))
                    error_message(error)
                green_message('Completed')
                break
            else:
                check_attempt += 1
                if check_attempt == 2:
                    print(colored('Max retries error', 'red'))
                    print(colored(error, 'red'))


def maldet():
    global email
    # Anti-Virus Scanning With Maldet

    question = 'Do you want to use Maldet for Anti-virus Scanning?'
    dir_path = '/usr/local/src/'

    response = check_answer(question)
    if response:
        bar.auto('Downloading Maldet..', run_cmd, args=[f'wget -q http://www.rfxn.com/downloads/maldetect-current.tar.gz -P {dir_path}'])
        status_ok_message('Maldet Downloaded')

        tarfile = '/usr/local/src/maldetect-current.tar.gz'
        path = '/usr/local/src/'
        retcode = subprocess.call(['tar', '-xvf', tarfile, '-C', path], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

        for elem in listdir(dir_path):
            if ('maldetect-' in elem) and (not 'maldetect-current' in elem):
                maldect_path = dir_path + elem
                file_path = f'{maldect_path}/files/conf.maldet'
                bar.auto('Installing Maldet', run_cmd, args=[f'sh {maldect_path}/install.sh'])
                status_ok_message('Maldet Installed')
                output_message('Configuring Maldet..')

                change_lines(file_path,
                             _1=[
                                 'email_alert="0"',
                                 'email_alert="1"\n'],
                             _2=[
                                 'email_addr="you@domain.com"',
                                 f'email_alert="{email}"\n'],
                             _3=[
                                 'email_ignore_clean="1"',
                                 'email_ignore_clean="0"\n']
                             )

                task_status_ok()

                break



def rkhunter():
    global email
    # Rootkit Detection With Rkhunter
    question = 'Do you want to install and configure rkhunter?\n'
    file_path = '/etc/rkhunter.conf'
    error = 'Fatal Error: rkhunter will have to be configured manually'
    response = check_answer(question)
    check_attempt = 0
    if response:
        while check_attempt < 2:
            bar.auto('Installing rkhunter..', run_cmd, args=['apt install rkhunter -y'])
            error_message('[ALERT] If this is the first installation select yes to the three questions you will be asked to answer ')
            time.sleep(5)
            if 'rkhunter is already the newest version' in str(subprocess.check_output(['apt', 'install', 'rkhunter'], stderr=subprocess.STDOUT)).strip("b'"):
                output_message('Configuring rkhunter..')
                change_lines(file_path,
                                 _1=[
                                     'UPDATE_MIRRORS=0',
                                     'UPDATE_MIRRORS=1\n'
                                 ],
                                 _2=[
                                     'MIRRORS_MODE=1',
                                     'MIRRORS_MODE=0\n'
                                 ],
                                 _3=[
                                     '#MAIL-ON-WARNING=root',
                                     f'MAIL-ON-WARNING={email}\n'
                                 ],
                                 _4=[
                                     '#COPY_LOG_ON_ERROR=0',
                                     'COPY_LOG_ON_ERROR=1\n'
                                 ],
                                 _5=[
                                     '#PKGMGR=NONE',
                                     'PKGMGR=DPKG\n'
                                 ],
                                 _6=[
                                     '#PHALANX2_DIRTEST=0',
                                     'PHALANX2_DIRTEST=1\n'
                                 ],
                                 _7=[
                                     '#USE_LOCKING=0',
                                    'USE_LOCKING=1\n'
                                 ],
                                 _8=[
                                     '#SHOW_SUMMARY_WARNINGS_NUMBER=0',
                                     'SHOW_SUMMARY_WARNINGS_NUMBER=1\n'
                                 ],
                                _9 = [
                                    'WEB_CMD="/bin/false"',
                                    'WEB_CMD=""\n'
                                ]
                             )
                task_status_ok()
                subprocess.check_call(['dpkg-reconfigure', 'rkhunter'],  stderr=subprocess.STDOUT)

                bar.auto('Running rkhunter..', run_cmd, args=['rkhunter --propupd', 'rkhunter --update'])
                status_ok_message('Rkhunter Done')

                break
            else:
                check_attempt += 1
                if check_attempt == 2:
                    error_message(error)

def logwatch():
    global email
    # logwatch - system log analyzer and reporter
    question = 'Do you want to install and configure logwatch?'
    file_path = '/etc/cron.daily/00logwatch'
    error = 'Fatal Error: logwatch will have to be configured manually'
    response = check_answer(question)
    check_attempt = 0
    if response:
        while check_attempt < 2:
            bar.auto('Installing system log analyzer and reporter tools..', run_cmd, args=['apt install logwatch -y'])
            output_message('Configuring system log analyzer and reporter tools')
            if 'logwatch is already the newest version' in str(subprocess.check_output(['apt', 'install', 'logwatch'], stderr=subprocess.STDOUT)).strip("b'"):
                with open(file_path, 'w') as file:
                    file.write(f'''
    #!/bin/bash
    
    #Check if removed-but-not-purged
    test -x /usr/share/logwatch/scripts/logwatch.pl || exit 0
    
    #execute
    /usr/sbin/logwatch --output mail --format html --mailto {email} --range yesterday --service all
    
                    ''')
                task_status_ok()
                break
            else:
                check_attempt += 1
                if check_attempt == 2:
                    error_message(error)

    run_cmd('ufw enable')

def auditd():
    global email
    # logwatch - system log analyzer and reporter
    question = 'Do you want to install and configure auditd?'
    file_path = '/etc/audit/audit.rules'
    file_path_1 = '/etc/cron.d/audit-report'
    error = 'Fatal Error: logwatch will have to be configured manually'
    response = check_answer(question)
    check_attempt = 0
    if response:
        bar.auto('Installing auditd..', run_cmd, args=['apt install auditd -y'])
        status_ok_message('Audit Installed')
        output_message('Configuring Audit')
        run_cmd(f'wget -q https://raw.githubusercontent.com/Neo23x0/auditd/master/audit.rules -O {file_path}')
        task_status_ok()
        run_cmd('systemctl restart auditd')
        with open(file_path_1, 'w') as file:
            file.write(f'''
MAILTO={email}
1 0   * * *     root  /sbin/aureport -k -ts yesterday 00:00:00 -te yesterday 23:59:59
            ''')

def psad():
    global email, hostname
    # iptables Intrusion Detection And Prevention with
    question = 'Do you want to install and configure psad?'
    file_path = '/etc/psad/psad.conf'
    file_path_1 = '/etc/ufw/before.rules'
    file_path_2 = '/etc/ufw/before6.rules'
    error = 'Fatal Error: psad will have to be configured manually'
    response = check_answer(question)
    check_attempt = 0
    if response:
        while check_attempt < 2:
            bar.auto('Installing psad..', run_cmd, args=['apt install psad -y'])
            status_ok_message('Installed psad')

            if 'psad is already the newest version' in str(subprocess.check_output(['apt', 'install', 'psad'], stderr=subprocess.STDOUT)).strip("b'"):

                input_message('Type your Home net: ex(192.168.1.1/24) ')
                homenet = input(' ')

                output_message('Configuring psad')

                change_lines(file_path,
                             _1=[
                                 'EMAIL_ADDRESSES             root@localhost;',
                                 f'EMAIL_ADDRESSES             {email};\n'
                             ],
                             _2=[
                                 'HOSTNAME                     _CHANGEME_;',
                                 f'HOSTNAME                   {hostname};\n'
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

                task_status_ok()

                output_message_alone(f'''
These changes have been made to the config '/etc/psad/psad.conf'.
If u need more advanced options feel free to modify it.

    - EMAIL_ADDRESSES             {email};
    - HOSTNAME                   {hostname};
    - ENABLE_AUTO_IDS             Y;
    - HOME_NET                    {homenet};
    - PORT_RANGE_SCAN_THRESHOLD   2;
    - ENABLE_MAC_ADDR_REPORTING   Y;
    - ALERT_ALL                   N;
              
                ''')

                with open(file_path_1, 'r') as file:
                    lines = file.readlines()
                    text = file.read()
                    if not(check_lines_in_file(file_path_1,
                                               '# log all traffic so psad can analyze',
                                               '-A INPUT -j LOG --log-tcp-options --log-prefix "[IPTABLES]"',
                                               '-A FORWARD -j LOG --log-tcp-options --log-prefix "[IPTABLES]"')):

                        for index, line in enumerate(lines):
                            if line.strip() == "COMMIT":
                                lines.insert(index - 2, '# log all traffic so psad can analyze\n-A INPUT -j LOG --log-tcp-options --log-prefix "[IPTABLES]"\n-A FORWARD -j LOG --log-tcp-options --log-prefix "[IPTABLES]"')
                                break
                        with open(file_path_1, 'w') as file:
                            for line in lines:
                                file.write(line)

                with open(file_path_2, 'r') as file:
                    lines = file.readlines()
                    text = file.read()
                    if not (check_lines_in_file(file_path_1,
                                                '# log all traffic so psad can analyze',
                                                '-A INPUT -j LOG --log-tcp-options --log-prefix "[IPTABLES]"',
                                                '-A FORWARD -j LOG --log-tcp-options --log-prefix "[IPTABLES]"')):
                        for index, line in enumerate(lines):
                            if line.strip() == "COMMIT":
                                lines.insert(index - 2, '# log all traffic so psad can analyze\n-A INPUT -j LOG --log-tcp-options --log-prefix "[IPTABLES]"\n-A FORWARD -j LOG --log-tcp-options --log-prefix "[IPTABLES]"')
                                break
                        with open(file_path_2, 'w') as file:
                            for line in lines:
                                file.write(line)
                try:
                    if not 'Active' in str(subprocess.check_output(['service', 'ufw', 'status'], stderr=subprocess.STDOUT)):
                        run_cmd('ufw enable')
                except:
                    run_cmd('ufw enable')

                bar.text('Restarting psad..')
                bar.run()

                run_cmd('ufw reload')
                check_call(['psad', '-R'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                run_cmd('psad --sig-update')
                run_cmd('psad -H')

                bar.stop()

                break
            else:
                check_attempt += 1
                if check_attempt == 2:
                    print(colored(error, 'red'))


def alerts():
    global email
    # Automatic Security Updates and Alerts

    question = 'Do you want Automatic Security Updates and Alerts? (unattended-upgrades)'
    file_path = '/etc/apt/apt.conf.d/51myunattended-upgrades'
    file_path_1 = '/etc/apticron/apticron.conf'
    error = 'Fatal Error: psad will have to be configured manually'
    response = check_answer(question)
    check_attempt = 0
    if response:
            bar.auto('Installing Security Updates and Alerts..', run_cmd, args=['apt install unattended-upgrades apt-listchanges apticron -y'])
            output_message('Configuring Security Updates and Alerts..')
            with open(file_path, 'w') as file:
                    file.write('''
    // Enable the update/upgrade script (0=disable)
    APT::Periodic::Enable "1";
    
    // Do "apt-get update" automatically every n-days (0=disable)
    APT::Periodic::Update-Package-Lists "1";
    
    // Do "apt-get upgrade --download-only" every n-days (0=disable)
    APT::Periodic::Download-Upgradeable-Packages "1";
    
    // Do "apt-get autoclean" every n-days (0=disable)
    APT::Periodic::AutocleanInterval "7";
    
    // Send report mail to root
    //     0:  no report             (or null string)
    //     1:  progress report       (actually any string)
    //     2:  + command outputs     (remove -qq, remove 2>/dev/null, add -d)
    //     3:  + trace on    APT::Periodic::Verbose "2";
    APT::Periodic::Unattended-Upgrade "1";
    
    // Automatically upgrade packages from these
    Unattended-Upgrade::Origins-Pattern {
          "o=Debian,a=stable";
          "o=Debian,a=stable-updates";
          "origin=Debian,codename=${distro_codename},label=Debian-Security";
    };
    
    // You can specify your own packages to NOT automatically upgrade here
    Unattended-Upgrade::Package-Blacklist {
    };
    
    // Run dpkg --force-confold --configure -a if a unclean dpkg state is detected to true to ensure that updates get installed even when the system got interrupted during a previous run
    Unattended-Upgrade::AutoFixInterruptedDpkg "true";
    
    //Perform the upgrade when the machine is running because we wont be shutting our server down often
    Unattended-Upgrade::InstallOnShutdown "false";
    
    // Send an email to this address with information about the packages upgraded.
    Unattended-Upgrade::Mail "''' + email + '''";
    
    // Always send an e-mail
    Unattended-Upgrade::MailOnlyOnError "false";
    
    // Remove all unused dependencies after the upgrade has finished
    Unattended-Upgrade::Remove-Unused-Dependencies "true";
    
    // Remove any new unused dependencies after the upgrade has finished
    Unattended-Upgrade::Remove-New-Unused-Dependencies "true";
    
    // Automatically reboot WITHOUT CONFIRMATION if the file /var/run/reboot-required is found after the upgrade.
    Unattended-Upgrade::Automatic-Reboot "true";
    
    // Automatically reboot even if users are logged in.
    Unattended-Upgrade::Automatic-Reboot-WithUsers "true";
                    ''')

            with open(file_path_1, 'w') as file:
                file.write(f'''
    EMAIL="{email}"
    NOTIFY_NO_UPDATES="1"           
                ''')

            task_status_ok()
        

def lynis():
    question = 'Do you want install Lynis for upgrade your security level?'
    response = check_answer(question)
    if response:
        bar.auto('Installing lynis..', run_cmd, args=['apt install lynis -y'])
        bar.text('Running lynis scan ')
        bar.run()
        output = str(subprocess.check_output(['lynis', 'audit', 'system'], stderr=subprocess.STDOUT), 'utf-8')
        bar.stop()
        status_ok_message('Scan completed')
        output = remove_ansi_escape(output)

        lynis_output_sections = dict()

        output = output.split('[+]')

        for section in output:
            if ('------------------------------------') in section:
                section = section.split('------------------------------------')
                if section[0].strip() == 'Plugins (phase 2)':
                    section[1] = section[1].split(
                        '================================================================================')
                    lynis_output_sections[section[0].strip()] = section[1][0].strip()
                    section[1][1] = section[1][1].split('Suggestions')
                    section[1][1][1] = section[1][1][1].split('----------------------------')
                    lynis_output_sections['Suggestions'] = section[1][1][1][1]
                else:
                    lynis_output_sections[section[0].strip()] = section[1].strip()

        if ('Kernel Hardening' in lynis_output_sections):
            section = lynis_output_sections['Kernel Hardening']

            section = section.split('-')
            for line in section:
                line = line.strip()
                if '[ DIFFERENT ]' in line:
                    line = line.split()
                    for word in line:
                        if ')' in word:
                            word = word.strip('()exp: ')
                            if len(word) == 1:
                                word = word[0]
                            elif len(word) == 2:
                                word = word[1]
                            elif len(word) == 3:
                                word = word[2]
                            print(f'sysctl -w {line[0].strip()}={word}')
                            run_cmd(f'sysctl -w {line[0].strip()}={word}')

        print('\n\n\n')
        if ('Suggestions' in lynis_output_sections):
            suggestions = lynis_output_sections['Suggestions'].split('*')
            suggestions_list = []
            for suggestion in suggestions:
                suggestion = suggestion.split('\n')
                suggestions_list.append(suggestion[0].strip())

            if 'Protect rescue.service by using sulogin [BOOT-5260]' in suggestions_list:
                task = 'BOOT-5260'
                output_message_alone(f'Configuring {task}')
                with open('/usr/lib/systemd/system/rescue.service', 'r') as file:
                    lines = file.readlines()
                    for index, line in enumerate(lines):
                        if 'ExecStart' in line.strip().split('='):
                            lines[index] = 'ExecStart=-/usr/sbin/sulogin'

                with open('/usr/lib/systemd/system/rescue.service', 'w') as f_w:

                    for line in lines:
                        f_w.write(line)
                status_ok_message(f'{task}')

            if 'Determine priority for available kernel update [KRNL-5788]' in suggestions_list:

                # https://phoenixnap.com/kb/how-to-update-kernel-ubuntu

                task = 'KRNL-5788'
                output_message_alone(f'Configuring {task}')

                bar.auto('updating system', run_cmd, args=['apt-get update'])
                status_ok_message('System updated')
                bar.auto('updating kernel', run_cmd, args=['apt-get dist-upgrade'])
                status_ok_message(f'{task}')

            if 'Configure minimum password age in /etc/login.defs [AUTH-9286]' in suggestions_list or\
                    'Configure maximum password age in /etc/login.defs [AUTH-9286]' in suggestions_list or \
                    'Default umask in /etc/login.defs could be more strict like 027 [AUTH-9328]' in suggestions_list:
                task = 'AUTH-9286'
                change_lines('/etc/login.defs',
                             _1=['UMASK		022',
                                 'UMASK		027\n'],
                             _2=['PASS_MAX_DAYS	99999',
                                 'PASS_MAX_DAYS   30\n'],
                             _3=['PASS_MIN_DAYS	0',
                                 'PASS_MIN_DAYS   1\n'],
                             _4=['PASS_WARN_AGE   7',
                                 'PASS_WARN_AGE   7\n'],
                             )
                output_message_alone(f'Configuring {task}')
                status_ok_message(f'{task}')


        else:
            print('Something went wrong, cannot analize lynis scan output')


def start():

    # Checking if script runs as root
    output_message('Script is running as root ')

    if os.geteuid() != 0:
        error_message("You need to have root privileges to run this script.\nPlease try again, this time using 'sudo'. Exiting.")
        exit()

    task_status_ok()


    # Checking internet connection
    output_message('Checking Internet connection')
    internet_on()

    task_status_ok()
    # Update sys

    bar.auto('System Update..', run_cmd, args=['apt update -y'])
    status_ok_message('System update')

    bar.auto('System Upgrade..', run_cmd, args=['apt upgrade -y'])
    status_ok_message('System Upgraded')





sections = dict()

sections['section_1'] = 'Automated Email allerts'
sections['section_2'] = 'Securing User Accounts'
sections['section_3'] = 'Encrypting and SSH Hardening'
sections['section_4'] = 'Securing your box with a Firewall'
sections['section_5'] = 'Intrusion Detection And Prevention'
sections['section_6'] = 'Application Intrusion Detection And Prevention'
sections['section_7'] = 'File/Folder Integrity Monitoring'
sections['section_8'] = 'Automated Anti-Virus Scanning'
sections['section_9'] = 'Automated Rootkit Detection'
sections['section_10'] = 'system log analyzer and reporter'
sections['section_11'] = 'Misc'
sections['section_12'] = 'System & Kernel hardening'


color = 'green'

def print_ascii_art(text):
    print()
    print()
    print(colored(text, 'cyan'))
    print()

def print_section_1():
    print_ascii_art(sections['section_1'])

def print_section_2():
    print_ascii_art(sections['section_2'])

def print_section_3():
    print_ascii_art(sections['section_3'])

def print_section_4():
    print_ascii_art(sections['section_4'])

def print_section_5():
    print_ascii_art(sections['section_5'])

def print_section_6():
    print_ascii_art(sections['section_6'])

def print_section_7():
    print_ascii_art(sections['section_7'])

def print_section_8():
    print_ascii_art(sections['section_8'])

def print_section_9():
    print_ascii_art(sections['section_9'])

def print_section_10():
    print_ascii_art(sections['section_10'])

def print_section_11():
    print_ascii_art(sections['section_11'])

def print_section_12():
    print_ascii_art(sections['section_12'])


ask_for_email = '''\nTo receive notifications from the system and for the correct configuration of some tools, the email address of the admin is required.
Please enter the administrator email: '''
menu = f'''

Welcome to SSLock security tool. 
For run a task select a choice from the menu or run the Script using the flags. use -help or -h for see the aviable flags.

--- MENU ---

[+] Select '*' for run all the tasks

[1]  {sections['section_1']}
[2]  {sections['section_2']}
[3]  {sections['section_3']}
[4]  {sections['section_4']}
[5]  {sections['section_5']}
[6]  {sections['section_6']}
[7]  {sections['section_7']}
[8]  {sections['section_8']}
[9]  {sections['section_9']}
[10] {sections['section_10']}
[11] {sections['section_11']}
[12] {sections['section_12']}

'''
flags_help = f'''

-E   :    {sections['section_1']}  
-Su  :    {sections['section_2']}
-Ssh :    {sections['section_3']}
-Sf  :    {sections['section_4']}
-Idp :    {sections['section_5']}
-Aidp:    {sections['section_6']}
-Fim :    {sections['section_7']}     
-Avs :    {sections['section_8']}
-Rd  :    {sections['section_9']}
-Lar :    {sections['section_10']}
-M   :    {sections['section_11']}
-Skh :    {sections['section_12']}

'''
tool_sections = dict()
tool_sections['section_1'] = [print_section_1, autamated_email_allerts]
tool_sections['section_2'] = [print_section_2, securing_users_accounts]
tool_sections['section_3'] = [print_section_3, ssh]
tool_sections['section_4'] = [print_section_4, ufw]
tool_sections['section_5'] = [print_section_5, fail2ban, psad]
tool_sections['section_6'] = [print_section_6, ]
tool_sections['section_7'] = [print_section_7, aide]
tool_sections['section_8'] = [print_section_8, maldet, clamAv]
tool_sections['section_9'] = [print_section_9, rkhunter]
tool_sections['section_10'] = [print_section_10, logwatch, auditd]
tool_sections['section_11'] = [print_section_11, nvidia_drivers]
tool_sections['section_12'] = [print_section_12, ntp, proc, entropy_pool, alerts]

try:
    start()
except KeyboardInterrupt:
    print()
    exit()
except Exception as error:
    error_message(f'[ERROR] {str(error)}')

if len(sys.argv) > 1:

    flags = sys.argv[1:]
    if '-h' in flags or '-help' in flags:
        output_message_alone('Welcome to the SSLock help menu. The aviable flags are: \n' + flags_help)

    else:

        try:
            aviable_flags = {
                '-E': '1',
                '-Su': '2',
                '-Ssh': '3',
                '-Sf': '4',
                '-Idp': '5',
                '-Aidp': '6',
                '-Fim': '7',
                '-Avs': '8',
                '-Rd': '9',
                '-Lar': '10',
                '-M': '11',
                '-Skh': '12',
            }

            if '-Fim' in flags or \
                    '-Avs' in flags or \
                    '-Rd' in flags or \
                    '-Lar' in flags or \
                    '-Ssh' in flags or \
                    '-E' in flags:
                input_message(ask_for_email)
                email = input(' ')
                email = email.strip()

            for flag in aviable_flags:
                if flag in flags:
                    section = 'section_' + aviable_flags[flag]

                    if aviable_flags[flag] == '7':
                        end_cmds.append('aideinit -y -f')

                    for function in tool_sections[section]:
                        try:
                            function()
                        except KeyboardInterrupt:
                            print()
                            exit()
                        except Exception as error:
                            error_message(f'[ERROR] {str(error)}')

            for cmd in end_cmds:
                if cmd == 'aideinit -y -f':
                    response = check_answer(
                        'Aide, for work, needs to create a new database and install it, do it now! \nThis require time..')
                    if not response:
                        bar.auto('Running Aide tasks..', run_cmd, args=['aideinit -y -f'])
                        status_ok_message('Tasks completed')

                else:
                    run_cmd(cmd)

            exit()
        except SystemExit:
            print()
            exit()
        except KeyboardInterrupt:
            print()
            exit()
        except Exception as error:
            error_message(f'[ERROR] {str(error)}')




else:
    while True:
        try:
            output_message_alone(menu)
            input_message('\nchoice (note: press Q for quit correctly the script) :')
            choice = input(' ')

            aviable_choices = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', ]

            if choice in ['7', '8', '9', '10', '1', '*', '3']:
                if email == '':
                    input_message(ask_for_email)
                    email = input(' ')
                    email = email.strip()

            if choice in aviable_choices:
                section = 'section_' + choice

                if choice == '7':
                    end_cmds.append('aideinit -y -f')

                for function in tool_sections[section]:
                    try:
                        function()
                    except KeyboardInterrupt:
                        print()
                        exit()
                    except Exception as error:
                        error_message(f'[ERROR] {str(error)}')

            if choice == '*':
                functions = []

                for key in tool_sections:
                    functions += tool_sections[key]

                for function in functions:
                    try:
                        function()
                    except KeyboardInterrupt:
                        exit()
                    except Exception as error:
                        error_message(f'[ERROR] {str(error)}')

            if choice.upper() in ['Q', 'QUIT']:
                for cmd in end_cmds:
                    if cmd == 'aideinit -y -f':
                        response = check_answer("Are you sure you don't want to create a database for Aide?")
                        if not response:
                            bar.auto('Running Aide tasks..', run_cmd, args=['aideinit -y -f'])
                    else:
                        run_cmd(cmd)

                exit()
        except SystemExit:
            print()
            exit()
        except KeyboardInterrupt:
            print()
            exit()
        except Exception as error:
            error_message(f'[ERROR] {str(error)}')
