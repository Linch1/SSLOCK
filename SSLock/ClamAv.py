from SSLock import General
from SSLock import UsersConfig
import os
import subprocess


def clamAv(EMAIL):
    # Anti-Virus Scanning With ClamAV

    f_clam_conf = '/etc/clamav/freshclam.conf'

    if not General.answer('Do you want to use ClamAV for Anti-virus Scanning with root permissions?'): return

    General.run_cmd('apt install clamav clamav-freshclam -y')
    General.change_lines(
        f_clam_conf,
        _1=[
            '# Check for new database 24 times a day',
            '# Check for new database 1 times a day\n'
        ],
        _2=[
            'Checks 24',
            'Checks 1\n'
        ]
    )
    General.run_cmd('freshclam -v')




    user = ''
    while True:
        user = General.input_message(
            "Using clamscan as root is dangerous because if a file is in fact a virus there is risk that it could use the root privileges.\n"
            "You can create another user by writing [U] \nPlease chose a user that can run clamscan"
        )
        if UsersConfig.user_exists(user): break
        if user.upper() == 'U':
            UsersConfig.create_users()
        else:
            General.error_message("User doesn't exists")
            General.output_message('For create a new user type [U]')


    dir_to_scan = ''
    all_directories_exists = False
    while not all_directories_exists:
        all_directories_exists = True
        dir_to_scan = General.input_message('Which direcotry should be scanned by clamAV? (ex. /var/www /var/vmail): ')
        for dir in dir_to_scan.split():
            if not os.path.exists(dir):
                General.error_message(f"The directory {dir} doesn't exists, select another path")
                all_directories_exists = False
    General.output_message('Configuration Anti-virus Scanning tools..')

    f_clam_daily = f'/home/{user}/clamscan_daily.sh'

    with open(f_clam_daily, 'w') as file:
        file.write(f'''
    #!/bin/bash
    LOGFILE="/var/log/clamav/clamav-$(date +'%Y-%m-%d').log";
    EMAIL_MSG="Please see the log file attached.";
    EMAIL_FROM="''' + EMAIL + '''";
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

    General.run_cmd('chmod 0755 /root/clamscan_daily.sh')
    General.run_cmd('ln /root/clamscan_daily.sh /etc/cron.daily/clamscan_daily')
    General.run_cmd('service clamav-freshclam start')
    if not General.answer("Do you want to run the virus scan on the given directories now? This can take some time"): return
    General.output_message('Running first scan for check if all is ok')
    subprocess.run(['clamscan', '-r', dir_to_scan])