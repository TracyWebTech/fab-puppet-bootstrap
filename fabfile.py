from fabric.api import local, run, put, sudo

# set(
#     project = 'project_name',
 
#     package     = '$(project).zip',
 
#     # Remote servers
#     fab_user    = 'usuario_ssh',
#     fab_hosts   = ['servidor1.com', 'servidor2.com'],
# )
 

def set_hostname(host):
    sudo('echo -e '+host+' > /etc/hostname')
    sudo('echo -e "127.0.0.1\t'+host+'" >> /etc/hosts')
    
def add_puppet_repo():
    sudo('echo -e "deb http://apt.puppetlabs.com/ precise main\ndeb-src http://apt.puppetlabs.com/ precise main" >> /etc/apt/sources.list.d/puppet.list')

    sudo('apt-key adv --keyserver keyserver.ubuntu.com --recv 4BD6EC30')

    sudo('apt-get update')