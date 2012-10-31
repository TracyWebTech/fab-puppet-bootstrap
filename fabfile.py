from fabric.api import local, sudo, settings

def set_hostname(host):
    sudo('echo -e "127.0.0.1\t'+host+'" >> /etc/hosts')
    sudo('hostname '+host)

def add_puppet_repository():
    sudo('echo -e "deb http://apt.puppetlabs.com/ precise main\ndeb-src http://apt.puppetlabs.com/ precise main" >> /etc/apt/sources.list.d/puppet.list')
    sudo('apt-key adv --keyserver keyserver.ubuntu.com --recv 4BD6EC30')
    sudo('apt-get update')

def agent_add_master_in_hosts(master):
    sudo('echo -e "' + master + '\tpuppet" >> /etc/hosts')

def agent_connect_to_master(agent_host, master):
    with settings(warn_only=True):
        sudo('puppet agent --test')
    local('fab -H ' + master + ' master_accept_agent:' + agent_host) 

def agent_enable_autostart():
    sudo('sed -i -re "s/START=no/START=yes/" /etc/default/puppet')
    sudo('service puppet start')

def puppet_agent_install(host, master):

    set_hostname(host)
    add_puppet_repository()
    agent_add_master_in_hosts(master)
    sudo('apt-get install puppet')
    agent_connect_to_master(host, master)
    agent_enable_autostart()


def master_accept_agent(agent_host):
    sudo('puppet cert sign ' + agent_host)

def puppet_master_install(host):

    set_hostname(host)
    add_puppet_repository()
    
    sudo('apt-get install puppetmaster') 