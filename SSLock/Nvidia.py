from SSLock import General


def nvidia_drivers():
    # Installation invidia driver
    response = General.answer('Do you need nvidia drivers?')
    if not response: return
    General.output_message('Since the nvidia-driver package in Debian is proprietary, we need to enable contrib and non-free component in /etc/apt/sources.list file')
    General.run_cmd('apt install software-properties-common')
    General.run_cmd('add-apt-repository contrib')
    General.run_cmd('add-apt-repository non-free')
    General.run_cmd('apt update -y')
    General.run_cmd('apt install nvidia-driver -y')