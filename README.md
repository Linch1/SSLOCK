<pre><p align="center">
    
         .:+shdmNMMMMMMNmdhs+:.         
     -MMNMMMMMMMMMMMMMMMMMMMMMMNMM-     
    `MMMMMMMMMMMMMMMMMMMMMMMMMMMMMM     
    `MMMMMMMMMMMNMMMMMMNMMMMMMMMMMM     
    `MMMMMMMMMy`-SSLock-`yMMMMMMMMM     
    `MMMMMMMMMN .MMMMMM. NMMMMMMMMM     
    `MMMMMMMMMm :MMMMMM: mMMMMMMMMM     
    `MMMMMMMMMN+yMMMMMMy+NMMMMMMMMM     
    `MMMMMMMN-............-NMMMMMMM     
    `MMMMMMMm              mMMMMMMM     
    `MMMMMMMm              mMMMMMMM     
     dMMMMMMm              mMMMMMMd     
     .NMMMMMm              mMMMMMN.     
      .mMMMMN-............-NMMMMm.      
       `sMMMMMMMMMMMMMMMMMMMMMMs`       
         -dMMMMMMMMMMMMMMMMMMd-         
           :mMMMMMMMMMMMMMMm:           
             :dMMMMMMMMMMd:             
               -yMMMMMMy-               
                 `+mm+`                 

</pre></p>

<p align="center">
Although this tool is written to automate the hardening process on linux systems, we must not ignore the real need for constant study and updating in order to reduce and / or identify the attacks we can receive.
</p>


<p align="center">
Automated Security Hardening For Linux Whit
</p>
<h2><p align="center">
SSLock
</p></h2> 


SSLock is a hardening suite equipped whit the most common Linux security pratice, and enhanted whit the power of python automation.

## Main Features

* Automated Email allerts
* Securing User Accounts
* Securing your box with a Firewall
* Encrypting and SSH Hardening
* Intrusion Detection And Prevention
* Application Intrusion Detection And Prevention
* File/Folder Integrity Monitoring
* Automated Anti-Virus Scanning
* Automated Rootkit Detection
* system log analyzer and reporter
* System & Kernel hardening

## To do

* Custom Jails for Fail2ban
* MAC (Mandatory Access Control) and Linux Security Modules (LSMs) -- Security-Enhanced Linux / SELinux  or AppArmor --
* CIS-CAT 
* debsums 
* nftables 
* Improve Kernel Hardening
* Lynis Score Check

## FAQ
Why it's need to run it as ROOT ?
there are some things that not work whit sudo, like, bash shell internal commands or injecting kernel values into the /proc filesystem. For task such as these, a person would have to go to the root command prompt.
when the tool has ended the job, you are invited to disable the root account. "sudo passwd -l root"


## Contribution, Credits & License

Ways to contribute

   * Suggest a feature
   * Report a bug
   * Fix something and open a pull request
   * Create a browser extension
   * Create a burp suite/zaproxy plugin
   * Help me document the code
   * Spread the word
