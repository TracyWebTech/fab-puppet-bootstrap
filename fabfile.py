from fabric.api import local, sudo, settings, env


env.use_ssh_config = True


def set_hostname(host):
    """
    Change server hostname
    """
    sudo('echo -e "127.0.0.1\t'+host+'" >> /etc/hosts')
    sudo('hostname '+host)

def add_puppet_repository():
    """
    Add puppetlabs repository to apt
    """
    sudo('echo -e "deb http://apt.puppetlabs.com/ precise main\ndeb-src http://apt.puppetlabs.com/ precise main" > /etc/apt/sources.list.d/puppet.list')
    sudo('apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 4BD6EC30')
    sudo('apt-get update')

def agent_add_master_in_hosts(master):
    """
    Puppet agent set master in your hosts
    """
    sudo('echo -e "' + master + '\tpuppet puppetmaster" >> /etc/hosts')

def agent_connect_to_master(agent_host, master):
    """
    Puppet agent connect on master to send your keys
    """
    with settings(warn_only=True):
        sudo('puppet agent --test')
    #local('fab -H ' + master + ' master_accept_agent:' + agent_host) 

def agent_enable_autostart():
    """
    Enable Puppet agent autostart on boot
    """
    sudo('sed -i -re "s/START=no/START=yes/" /etc/default/puppet')
    sudo('service puppet start')

def puppet_agent_install(host, master):
    """
    Install Puppet agent and connect to Master to send your key
    """
    # set_hostname(host)
    add_puppet_repository()
    agent_add_master_in_hosts(master)
    sudo('apt-get install puppet')
    agent_connect_to_master(host, master)
    agent_enable_autostart()


def master_accept_agent(agent_host):
    """
    Puppet master accept key from agent
    """
    sudo('puppet cert sign ' + agent_host)


def master_accept_all():
    """
    Puppet master accept all requested keys
    """
    sudo('sudo puppet certo sign --all')

def puppet_master_install(host=None):
    """
    Install puppet master
    """
    # set_hostname(host)
    add_puppet_repository()
    
    sudo('apt-get install puppetmaster') 