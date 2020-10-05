from SSLock import General


def alerts(EMAIL):
    # Automatic Security Updates and Alerts

    f_alerts_upgrades = '/etc/apt/apt.conf.d/51myunattended-upgrades'
    f_alerts_conf = '/etc/apticron/apticron.conf'

    if not General.answer('Do you want Automatic Security Updates and Alerts? (unattended-upgrades)'): return

    General.run_cmd('apt install unattended-upgrades apt-listchanges apticron -y')

    General.output_message('Configuring Security Updates and Alerts..')
    with open(f_alerts_upgrades, 'w') as file:
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
    Unattended-Upgrade::Mail "''' + EMAIL + '''";

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

    with open(f_alerts_conf, 'w') as file:
        file.write(f'''
    EMAIL="{EMAIL}"
    NOTIFY_NO_UPDATES="1"           
                ''')
