
import re

from fabric import colors
from fabric.api import sudo
from fabric.decorators import task, roles, parallel
from fabric.context_managers import settings
from fabric.contrib.files import append, comment, exists, contains


try:
    from config import *
except ImportError:
    pass

IP_RE = re.compile(r'inet addr:(\d{1,3}\.\d{1,3}\.\d{1,3}.\d{1,3})')


def get_node():
    node = PUPPETNODES.get(env.host_string)

    if not node:
        err_msg = 'Node {} not found in PUPPETNODES.'.format(env.host_string)
        print(colors.red(err_msg))

    return node


def set_hostname():
    """
    Change server hostname
    """
    node = get_node()
    if contains('/etc/hosts', node.get('fqdn')):
        return

    interface = 'eth1'
    ifconfig_line = sudo('ifconfig {} | grep "inet addr"'.format(interface),
                          warn_only=True)
    ip_search = IP_RE.search(ifconfig_line)
    if ip_search:
        ip = ip_search.groups()[0]
    else:
        print(colors.red('No IP found for interface {}'.format(interface)))
        return

    hosts_line = '{ip}\t{fqdn}'.format(ip=ip, fqdn=node['fqdn'])
    append('/etc/hosts', hosts_line, use_sudo=True)


def add_puppet_repository():
    """
    Add puppetlabs repository to apt
    """
    if not exists('/etc/apt/sources.list.d/puppetlabs.list'):
        sudo('wget https://apt.puppetlabs.com/puppetlabs-release-precise.deb')
        sudo('dpkg -i puppetlabs-release-precise.deb')
        sudo('apt-get update')


def agent_add_master_in_hosts():
    """
    Puppet agent set master in your hosts
    """
    hosts_line = '{}\tpuppet'.format(PUPPETMASTER)
    append('/etc/hosts', hosts_line, use_sudo=True)


@task
@roles('puppet')
def puppet_run():
    """
    Force Puppet agent execution on node
    """
    with settings(warn_only=True):
        sudo('puppet agent --test --waitforcert=5')


def agent_enable_autostart():
    """
    Enable Puppet agent autostart on boot
    """

    if contains('/etc/default/puppet', 'START=no'):
        sudo('sed -i -re "s/START=no/START=yes/" /etc/default/puppet')

    if sudo('service puppet status', quiet=True).failed:
        sudo('service puppet restart')


@task
@parallel
@roles('puppet')
def puppet_install():
    """
    Install Puppet agent and connect to Master to send your key
    """
    set_hostname()
    add_puppet_repository()
    agent_add_master_in_hosts()
    if not exists('/usr/bin/puppet'):
        sudo('apt-get -y install puppet')
    agent_enable_autostart()
    puppet_run()


@task
@roles('puppetmaster')
def puppetmaster_sign(agent_host):
    """
    Puppet master accept key from agent
    """
    sudo('puppet cert sign ' + agent_host)


@task
@roles('puppetmaster')
def puppetmaster_sign_all():
    """
    Puppet master accept all requested keys
    """
    sudo('sudo puppet cert sign --all')
