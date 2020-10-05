from SSLock import General
import subprocess
import time


def rkhunter(EMAIL):

    # Rootkit Detection With Rkhunter
    f_rkhunter_conf = '/etc/rkhunter.conf'
    if not General.answer('Do you want to install and configure rkhunter?'): return

    General.run_cmd('apt install rkhunter -y')
    General.error_message('[ALERT] If this is the first installation select yes to the three questions you will be asked to answer ')
    time.sleep(5)
    General.output_message('Configuring rkhunter..')
    General.change_lines(
         f_rkhunter_conf,
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
             f'MAIL-ON-WARNING={EMAIL}\n'
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
    subprocess.check_call(['dpkg-reconfigure', 'rkhunter'], stderr=subprocess.STDOUT)
    General.run_cmd('rkhunter --propupd', 'rkhunter --update')
    General.output_message('Rkhunter Done')
