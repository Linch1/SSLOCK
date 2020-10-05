from SSLock import General

def entropy_pool():
    # More Secure Random Entropy Pool (WIP)
    response = General.answer('Do you want More Secure Random Entropy Pool (WIP)?')
    check_attempt = 0
    if not response: return
    General.run_cmd('apt install rng-tools -y')
    General.run_cmd('echo "HRNGDEVICE=/dev/urandom" >> /etc/default/rng-tools')
    General.run_cmd('systemctl start rng-tools')