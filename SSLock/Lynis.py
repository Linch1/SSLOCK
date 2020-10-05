from SSLock import General
import subprocess


def lynis():

    if not General.answer('Do you want install Lynis for upgrade your security level?'): return

    General.run_cmd('git clone https://github.com/CISOfy/lynis /opt/lynis')
    General.output_message('Lynis installed in > /opt/lynis')
    General.output_message('Running lynis scan..')
    output = str(subprocess.check_output(['./lynis', 'audit', 'system', '-Q'], cwd="/opt/lynis", stderr=subprocess.STDOUT), 'utf-8')
    General.output_message('Scan completed')
    output = General.remove_ansi_escape(output)
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
                        General.run_cmd(f'sysctl -w {line[0].strip()}={word}')

    print('\n\n\n')
    if ('Suggestions' in lynis_output_sections):
        suggestions = lynis_output_sections['Suggestions'].split('*')
        suggestions_list = []
        for suggestion in suggestions:
            suggestion = suggestion.split('\n')
            suggestions_list.append(suggestion[0].strip())

        if 'Protect rescue.service by using sulogin [BOOT-5260]' in suggestions_list:
            task = 'BOOT-5260'
            General.output_message(f'Configuring {task}')
            with open('/usr/lib/systemd/system/rescue.service', 'r') as file:
                lines = file.readlines()
                for index, line in enumerate(lines):
                    if 'ExecStart' in line.strip().split('='):
                        lines[index] = 'ExecStart=-/usr/sbin/sulogin'

            with open('/usr/lib/systemd/system/rescue.service', 'w') as f_w:

                for line in lines:
                    f_w.write(line)
            General.output_message(f'{task}')

        if 'Determine priority for available kernel update [KRNL-5788]' in suggestions_list:

            # https://phoenixnap.com/kb/how-to-update-kernel-ubuntu

            task = 'KRNL-5788'
            General.output_message(f'Configuring {task}')
            General.run_cmd('apt-get update')
            General.output_message('System updated')
            General.run_cmd('apt-get dist-upgrade')

        if 'Configure minimum password age in /etc/login.defs [AUTH-9286]' in suggestions_list or\
                'Configure maximum password age in /etc/login.defs [AUTH-9286]' in suggestions_list or \
                'Default umask in /etc/login.defs could be more strict like 027 [AUTH-9328]' in suggestions_list:
            task = 'AUTH-9286'
            General.change_lines(
                 '/etc/login.defs',
                 _1=['UMASK		022',
                     'UMASK		027\n'],
                 _2=['PASS_MAX_DAYS	99999',
                     'PASS_MAX_DAYS   30\n'],
                 _3=['PASS_MIN_DAYS	0',
                     'PASS_MIN_DAYS   1\n'],
                 _4=['PASS_WARN_AGE   7',
                     'PASS_WARN_AGE   7\n'],
            )
            General.output_message(f'Configuring {task}')
        else:
            General.error_message('Something went wrong, cannot analize lynis scan output')