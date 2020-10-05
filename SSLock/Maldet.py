from SSLock import General
import subprocess
from os import listdir

def maldet(EMAIL):
    # Anti-Virus Scanning With Maldet

    dir_path = '/usr/local/src/'

    if not General.answer('Do you want to use Maldet for Anti-virus Scanning?'): return

    General.run_cmd(f'wget -q http://www.rfxn.com/downloads/maldetect-current.tar.gz -P {dir_path}')
    General.output_message("Maldet Downloaded")
    tarfile = '/usr/local/src/maldetect-current.tar.gz'
    path = '/usr/local/src/'
    retcode = subprocess.call(['tar', '-xvf', tarfile, '-C', path], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    for elem in listdir(dir_path):
        if ('maldetect-' in elem) and (not 'maldetect-current' in elem):
            maldect_path = dir_path + elem
            file_path = f'{maldect_path}/files/conf.maldet'
            General.run_cmd(f'sh {maldect_path}/install.sh')
            General.output_message('Maldet Installed')
            General.output_message('Configuring Maldet..')
            General.change_lines(
                file_path,
                _1=[
                    'email_alert="0"',
                    'email_alert="1"\n'],
                _2=[
                    'email_addr="you@domain.com"',
                    f'email_alert="{EMAIL}"\n'],
                _3=[
                    'email_ignore_clean="1"',
                    'email_ignore_clean="0"\n']
            )
            break
