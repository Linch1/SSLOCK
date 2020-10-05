from SSLock import General
import subprocess

"""
INCREASE WORDPRESS UPLOAD SIZE: https://www.cloudways.com/blog/increase-media-file-maximum-upload-size-in-wordpress/
"""


def setup(EMAIL):
    f_apache2_dir_conf = '/etc/apache2/mods-enabled/dir.conf'
    if not General.answer('Do you want to setup a wordpress server?'): return
    General.output_message("-- Starting LMAP Stack SETUP --")
    # Download LAMP Stack LINUX - APACHE - MYSQL - PHP

    # APACHE DOWNLOAD
    General.run_cmd('apt install apache2 -y')
    General.run_cmd('ufw allow in "Apache Full"')

    # MYSQL DOWNLOAD
    General.run_cmd('apt install mysql-server -y')
    # run mysql_secure_installation ( automated )
    General.output_message("\n-- MYSQL SETUP --")
    MYSQL_ROOT_PASS = General.sensitive_input_message("[MYSQL] Set root password")

    # Make sure that NOBODY can access the server without a password
    # Kill the anonymous users
    # Because our hostname varies we'll use some Bash magic here.
    # Kill off the demo database
    # Make our changes take effect
    # Any subsequent tries to run queries this way will get access denied because lack of usr/pwd param

    General.run_cmd(
        f""" mysql -e " ALTER USER 'root'@'localhost' IDENTIFIED BY '{MYSQL_ROOT_PASS}'; " """,
        """ mysql -e " DELETE FROM mysql.user WHERE user='' AND host='localhost'; " """,
        """ mysql -e " DROP USER ''@'$(hostname)'; " """,
        """ mysql -e " DROP DATABASE test; " """,
        """ mysql -e " FLUSH PRIVILEGES; " """
    )

    # PHP DOWNLOAD
    # php.ini : /etc/php/7.4/apache2/php.ini
    General.output_message("\n-- PHP SETUP --")
    General.run_cmd("apt install php libapache2-mod-php php-mysql -y")
    with open(f_apache2_dir_conf, 'w') as file:
        file.write(
"""
<IfModule mod_dir.c>
    DirectoryIndex index.php index.html index.cgi index.pl index.xhtml index.htm
</IfModule>
"""
)
    General.run_cmd("sudo apt update -y")
    General.run_cmd("sudo apt install php-curl php-gd php-mbstring php-xml php-xmlrpc php-soap php-intl php-zip -y")
    General.run_cmd("sudo systemctl restart apache2")
    General.run_cmd("systemctl restart apache2")

    # WORDPRESS DOWNLOAD
    General.output_message("\n-- WORDPRESS DOWNLOAD --")
    General.run_cmd("wget -P /tmp 'https://wordpress.org/latest.tar.gz' ")
    General.run_cmd("tar -C /tmp -zxvf /tmp/latest.tar.gz")
    General.run_cmd("touch /tmp/wordpress/.htaccess")
    General.run_cmd("cp /tmp/wordpress/wp-config-sample.php /tmp/wordpress/wp-config.php")
    General.run_cmd("mkdir /tmp/wordpress/wp-content/upgrade")

