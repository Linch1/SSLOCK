from SSLock import General
import subprocess
import os.path
import time


def wpVirtualHost(EMAIL):

    ####################################################
    # SETUP APACHE VIRTUALHOST ( FOR MULTIPLE WEBSITES )
    ####################################################

    General.output_message("-- Creation of apache2 Virtual Host --")
    DOMAIN_FULL = General.input_message("Insert a domain[ domain.(com/.it/.org/etc..) ] ")
    DOMAIN = '.'.join(DOMAIN_FULL.split(".")[:-1]) if len(DOMAIN_FULL.split(".")) > 2 else DOMAIN_FULL.split(".")[0]
    General.run_cmd(f"mkdir /var/www/{DOMAIN}")  # create a directory for the virtual host
    General.run_cmd(f"chown -R $USER:$USER /var/www/{DOMAIN}")  # assign the directory to $USER
    General.run_cmd(f"chmod -R 755 /var/www/{DOMAIN}")  # be sure that permissions are correct

    f_apache_domain_conf = f'/etc/apache2/sites-available/{DOMAIN}.conf'
    with open(f_apache_domain_conf, 'w') as file:
        file.write(
"""
<VirtualHost *:80>
    ServerAdmin """ + EMAIL + """
    ServerName """ + DOMAIN_FULL + """
    ServerAlias www.""" + DOMAIN_FULL + """
    DocumentRoot /var/www/""" + DOMAIN + """
    ErrorLog ${APACHE_LOG_DIR}/error.log
    CustomLog ${APACHE_LOG_DIR}/access.log combined
</VirtualHost> 
<Directory /var/www/""" + DOMAIN + """/>
    AllowOverride All
</Directory>
""")

    General.run_cmd(f"sudo a2ensite {DOMAIN}.conf")  # Enable the new configuration ( you can enable as many different configs as you want )
    General.run_cmd(f"sudo a2dissite 000-default.conf")  # Disable the default configuration
    General.run_cmd("sudo a2enmod rewrite")
    General.run_cmd("sudo systemctl restart apache2")  # restart apache
    # Test apache configs
    # sudo apachectl -t -D DUMP_VHOSTS
    # sudo apachectl configtest

    # Add SSL to apache virtualhost
    General.run_cmd("apt install certbot python3-certbot-apache -y")
    General.run_cmd("mkdir /var/lib/letsencrypt")
    General.run_cmd("chmod -R 755 /var/lib/letsencrypt")
    General.output_message("""
-- Certbot configuration --
If questions are promp type the following answers:
> Terms of service: A
> Share mail address: N
> redirect HTTP traffic to HTTPS: 2
> If the validation of the domain go wrong just exit the script and investigate on the problem.
  You can restart the script on the same domain and it will work correctly""")
    General.run_cmd_interactive(f"sudo certbot --apache -d {DOMAIN_FULL} -d www.{DOMAIN_FULL}") # runs interactive certbot configuration

    # wordpress virtualhost setup
    General.output_message("-- Configuring wordpress Db --")
    DB_NAME = General.input_message("Database Name ")
    DB_USER = General.input_message("Database User Name ")

    DB_USER_PASS = General.sensitive_input_message("Database User Password ")

    General.run_cmd(
        f""" mysql -e " CREATE DATABASE {DB_NAME} DEFAULT CHARACTER SET utf8 COLLATE utf8_unicode_ci; " """,
        f""" mysql -e " CREATE USER '{DB_USER}'@'localhost' IDENTIFIED BY '{DB_USER_PASS}'; " """,
        f""" mysql -e " GRANT ALL PRIVILEGES ON {DB_NAME}.* TO '{DB_USER}'@'localhost'; " """,
        """ mysql -e " FLUSH PRIVILEGES; " """
    )

    if(not os.path.exists('/tmp/wordpress')):
        General.output_message("\n-- WORDPRESS DOWNLOAD --")
        General.run_cmd("wget -P /tmp 'https://wordpress.org/latest.tar.gz' ")
        General.run_cmd("tar -C /tmp -zxvf /tmp/latest.tar.gz")
        General.run_cmd("touch /tmp/wordpress/.htaccess")
        General.run_cmd("cp /tmp/wordpress/wp-config-sample.php /tmp/wordpress/wp-config.php")
        General.run_cmd("mkdir /tmp/wordpress/wp-content/upgrade")

    General.run_cmd(f"cp -a /tmp/wordpress/. /var/www/{DOMAIN}")
    General.run_cmd(f"chown -R www-data:www-data /var/www/{DOMAIN}")
    General.run_cmd("find /var/www/" + DOMAIN + "/ -type d -exec chmod 750 {} \;")
    General.run_cmd("find /var/www/" + DOMAIN + "/ -type f -exec chmod 640 {} \;")
    f_wp_domain_config = f"/var/www/{DOMAIN}/wp-config.php"

    General.run_cmd("apt install curl -y")

    OUTPUT_KEYS = General.output_run_cmd("curl -s https://api.wordpress.org/secret-key/1.1/salt/").decode(
        "utf-8").split("');")
    for key in OUTPUT_KEYS:
        if key.strip() == '': OUTPUT_KEYS.remove(key)
    OUTPUT_KEYS_DICT = dict()
    for index, key in enumerate(OUTPUT_KEYS):
        index += 1
        OUTPUT_KEYS_DICT["_" + str(index)] = [
            '( '.join(key.split(",")[0].split('(')).strip() + ',',
            key.strip() + "');\n"
        ]
    General.change_lines(
        f_wp_domain_config,
        **OUTPUT_KEYS_DICT
    )
    General.change_lines(
        f_wp_domain_config,
        _1=["define( 'DB_NAME',", f"define( 'DB_NAME', '{DB_NAME}');"],
        _2=["define( 'DB_USER',", f"define( 'DB_USER', '{DB_USER}');"],
        _3=["define( 'DB_PASSWORD',", f"define( 'DB_PASSWORD', '{DB_USER_PASS}');"],
    )
    General.insert_lines(
        f_wp_domain_config,
        "define( 'FS_METHOD', 'direct');",
        index_surplus=1,
        anchor_line=f"define( 'DB_PASSWORD', 'DB_USER_PASS');"
    )


    General.output_message('-- INFO --')
    General.output_message(f" > Finish the WP GUI installation going to https://{DOMAIN}")
    General.output_message(" > We did a setup for SSL certificate with Let’s Encrypt CERTBOT, THis Certificate expire")
    General.output_message("   after 90 days, A Bot that automatic does the renewal is also installed, Check that ")
    General.output_message("   it is working by typing 'sudo systemctl status certbot.timer' ")
    General.output_message(" > For check that PHP was installed sucesfully and it is working correctly do this steps: ")
    General.output_message(f"    - sudo nano /var/www/{DOMAIN}/info.php")
    General.output_message("    - Add the following line to the file '<?php phpinfo(); ?>' ")
    General.output_message(f"    - Visit this link 'http://{DOMAIN_FULL}/info.php'")
    General.output_message(f"    If a table with php information was displayed and nothing went wrong remove the file\n"
                           f"    previously created 'sudo rm /var/www/{DOMAIN}/info.php'")
    time.sleep(5)
