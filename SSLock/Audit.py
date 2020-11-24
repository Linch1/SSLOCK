from SSLock import General

def auditd(EMAIL):

    f_audit_rules = '/etc/audit/audit.rules'
    f_audit_report = '/etc/cron.d/audit-report'

    if not General.answer('Do you want to install and configure auditd?'): return

    General.run_cmd('apt install auditd -y')
    General.output_message('Configuring Audit')
    General.run_cmd(f'wget -q https://raw.githubusercontent.com/Neo23x0/auditd/master/audit.rules -O {f_audit_rules}')
    General.run_cmd('systemctl restart auditd')
    with open(f_audit_report, 'w') as file:
        file.write(f'''
        MAILTO={EMAIL}
        1 0   * * *     root  /sbin/aureport -k -ts yesterday 00:00:00 -te yesterday 23:59:59
                    ''')