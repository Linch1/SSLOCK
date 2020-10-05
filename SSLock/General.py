

import subprocess
from urllib.error import *
from urllib.request import urlopen
import re
import time
import getpass
import socket

USER = getpass.getuser()
HOSTNAME = socket.gethostname()
INPUT_COLOR = 'yellow'
OUTPUT_COLOR = 'blue'
ERROR_COLOR = 'red'
WARNING_COLOR = 'magenta'
INSTALLED_COLOR_PACKAGES = False


def output_message(text, tag=True):
    if tag: text = '* [SSLOCK] ' + text
    custom_print(text + '\n', OUTPUT_COLOR)


def error_message(text, tag=True):
    if tag: text = '* [SSLOCK] ' + text
    custom_print(text + '\n', ERROR_COLOR)


def warning_message(text, tag=True):
    if tag: text = '* [SSLOCK] ' + text
    custom_print(text, WARNING_COLOR)


def input_message(text, tag=True):
    if tag: text = '* [SSLOCK] ' + text
    custom_print(text, INPUT_COLOR)
    return input(': ')


def sensitive_input_message(text, tag=True):
    while True:
        repeat = 'Please Type it again: '
        if tag:
            text = '* [SSLOCK] ' + text
            repeat = '* [SSLOCK] ' + repeat
        data = getpass.getpass(prompt=text + ': ')
        data_repeat = getpass.getpass(prompt=repeat)
        if data == data_repeat: break
        else: error_message('The inserted inputs are different')
    return data


def run_cmd(*cmds):
    for cmd in cmds:
        output_message(f"Executing: {cmd}")
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        output, errors = p.communicate()
        if not errors is None:
            print(errors)


def run_cmd_interactive(cmd):
    output_message(f"Executing: {cmd}")
    subprocess.call(cmd.split())


def output_run_cmd(cmd):
    output_message(f"Executing: {cmd}")
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    output, errors = p.communicate()
    if not errors is None:
        print(errors)
    return output


def remove_ansi_escape(line):
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    return ansi_escape.sub('', line)


def answer(question, tag=True):
    while True:
        if tag: question = '* [SSLOCK] ' + question
        custom_print(question, INPUT_COLOR)
        warning_message(' [Y/N]', tag=False)
        response = input(' ')
        response = response.upper().strip()
        if response in ['Y', 'YES', 'N', 'NO']: break
    if response in ['Y', 'YES']:
        return True
    elif response in ['N', 'NO']:
        return False


# Check if a file contains some specific lines
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


# Insert some lines to a given file after a given anchor-line
def insert_lines(file_path, *lines, index_surplus=1, anchor_line=None):
    new_lines = '\n'
    for line in lines:
        new_lines += line + '\n'

    status = check_lines_in_file(file_path, *lines)
    if status: return
    with open(file_path, 'r') as file:
        lines = file.readlines()
        for index, line in enumerate(lines):
            if set(line.strip().split()) == set(anchor_line.strip().split()):
                lines.insert(index + index_surplus, new_lines)

    with open(file_path, 'w') as file:
        for line in lines:
            file.write(line)


# Edit some given file lines
def change_lines(file_path, **lines):
    lines_to_change = dict()
    # Create a dict of the passed lines that
    # has as key the old line and as value the new line
    for index, lines in lines.items():
        previous_line = lines[0]
        new_line = lines[1]
        previous_line = frozenset(previous_line.strip().split())
        lines_to_change[previous_line] = new_line

    # Read the file lines and create a dict of the whole file that
    # has as key the line-number and as value the line
    with open(file_path, 'r') as file:
        file_lines = file.readlines()
        for index, line in enumerate(file_lines):
            file_lines[index] = frozenset(line.split())

    # Compara le linee da modificare con quelle del file
    # e se ne trova una da modificare sostituisce la nuova all'indice di quella vecchia
    with open(file_path, 'r') as file:
        file_lines_to_change = file.readlines()
        for line_to_change in lines_to_change:
            for index_to_change, file_line in enumerate(file_lines):
                if line_to_change.issubset(file_line):
                    file_lines_to_change[index_to_change] = lines_to_change[line_to_change]

    # riscrivee le righe
    with open(file_path, 'w') as file:
        for line in file_lines_to_change:
            file.write(line)


def internet_on():
    try:
        urlopen('https://www.google.com/', timeout=1)
    except URLError:
        exit('No internet connection')
    return True


def custom_print(question, INPUT_COLOR):
    if INSTALLED_COLOR_PACKAGES:
        print(colored(question, INPUT_COLOR), end="")
    else:
        print(question, end="")


print("""
-- INFO --

* Before run the script *
> sudo apt update
> sudo apt upgrade 

* During the script *
During the script execution are going to appear some INFO messages,
follow them for the correct installation of some tools

----------
""")
time.sleep(5)
output_message(
"""Checking system update  
This may take a while if wasn't done before  
""")
run_cmd_interactive("apt update")
run_cmd_interactive("apt upgrade -y")
output_message("System up-to-date")

try:
    from termcolor import colored, cprint
    from pyfiglet import figlet_format
    from colorama import Fore, Back, Style

    INSTALLED_COLOR_PACKAGES = True
except:

    install_packages = answer(
"""Could not detect some python packages.
This package are needed for print colored text in the terminal
Install them (Recommended) ? """)

    if install_packages:
        run_cmd('apt install python3-pip -y')
        run_cmd('pip3 install termcolor')
        run_cmd('pip3 install pyfiglet')
        run_cmd('pip3 install colorama')
        from termcolor import colored, cprint
        from colorama import Fore, Back, Style
        from pyfiglet import figlet_format

        INSTALLED_COLOR_PACKAGES = True
    else:
        INSTALLED_COLOR_PACKAGES = False




# -----------------
# USERS CONFIG
# -----------------
# -----------------
# EXIM4 MAIL
# -----------------
# -----------------
# SSH CONFIG
# -----------------
# -----------------
# NVIDIA DRIVERS
# -----------------
# -----------------
# NTP CONFIG
# -----------------
# -----------------
# PROC CONFIG
# -----------------
# -----------------
# ENTROPY POOL ( RNG TOOLS )
# -----------------
# -----------------
# UFW CONFIG
# -----------------
# -----------------
# FAIL2BAN
# -----------------
# -----------------
# AIDE
# -----------------
# -----------------
# CLAMAV
# -----------------
# -----------------
# MALDET
# -----------------
# -----------------
# RKHUNTER
# -----------------
# -----------------
# LOGWATCH
# -----------------
# -----------------
# AUDIT
# -----------------
# -----------------
# PSAD
# -----------------
# -----------------
# ALERTS
# -----------------
# -----------------
# LYNIS
# -----------------
