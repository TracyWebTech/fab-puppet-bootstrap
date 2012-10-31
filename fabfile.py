from fabric.api import local, run, put, sudo

def set_hostname(host):
    sudo('echo -e "127.0.0.1\t'+host+'" >> /etc/hosts')
    sudo('hostname '+host)

def set_puppet_master_host(master):
    sudo('echo -e "' + master + '\tpuppet" >> /etc/hosts')

def add_puppet_repo():
    sudo('echo -e "deb http://apt.puppetlabs.com/ precise main\ndeb-src http://apt.puppetlabs.com/ precise main" >> /etc/apt/sources.list.d/puppet.list')
    sudo('apt-key adv --keyserver keyserver.ubuntu.com --recv 4BD6EC30')
    sudo('apt-get update')

def connect_to_master():
    sudo('puppet agent --test')

def install_puppet(host, master):

    set_hostname(host)
    add_puppet_repo()
    set_puppet_master_host(master)

    sudo('apt-get install puppet')

    connect_to_master()

def install_puppet_master(host):

    set_hostname(host)
    add_puppet_repo()
    
    sudo('apt-get install puppetmaster') 