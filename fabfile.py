#!/usr/bin/env python
# coding: utf-8
import MySQLdb
import ConfigParser
from fabric.api import run, env, execute, task, show, with_settings
from fabric.state import output
from fabric.colors import red, white
from os.path import expanduser

# suppress output
output.running = False
output.stdout = False
output.status = False
output.warnings = False
# import ssh aliases
env.use_ssh_config = True


# tasks here
@task
def get_hosts():
    """Get list of servers with upgrades available"""
    print(', '.join(_get_hosts()))


@task
def do_upgrades():
    """Run `apt-get dist-upgrade -y` on all servers"""
    if env.hosts:
        execute(_do_upgrades, hosts=env.host_string)
    else:
        hostlist = _get_hosts()
        if hostlist:
            execute(_do_upgrades, hosts=hostlist)
        else:
            print('No hosts with upgrades.')


@task
def list_upgrades():
    """Get all servers and the available upgrades"""
    if env.hosts:
        execute(_list_upgrades, hosts=env.host_string)
    else:
        hostlist = _get_hosts()
        if hostlist:
            execute(_list_upgrades, hosts=hostlist)
        else:
            print('No hosts with upgrades.')


# helper functions
@with_settings(warn_only=True)
def _list_upgrades():
    result = run('apt-get --simulate --verbose-versions dist-upgrade \
                 | grep "  "')
    host = red(env.host_string, bold=True)
    print('[{}]'.format(host))
    if result:
        # clean up return values, prettier arrows!
        result = [x.lstrip().replace('=>', '→') for x in result.split("\n")]
        for package in result:
            package = white(package, bold=True)
            print('Update for {}'.format(package))
    else:
        print('No updates.')


def _do_upgrades():
    with show('stdout'):
        run('apt-get --quiet --assume-yes dist-upgrade \
            | grep --invert-match "(Reading database"')


def _get_hosts():
    config = ConfigParser.ConfigParser()
    config.read(expanduser('~/.remoteaptrc'))
    db = MySQLdb.connect(host=config.get('icinga', 'host'),
                         user=config.get('icinga', 'user'),
                         passwd=config.get('icinga', 'passwd'),
                         db=config.get('icinga', 'db'))
    cur = db.cursor()
    cur.execute('SELECT objects.name1 FROM icinga_servicestatus AS status \
                JOIN icinga_objects AS objects ON \
                (status.service_object_id = objects.object_id) \
                WHERE status.current_state != 0 AND \
                objects.name2 LIKE "APT status";')
    hosts = []
    for row in cur.fetchall():
        # data from rows
        hosts.append(str(row[0]).lower())
    # clean up
    cur.close()
    db.close()
    return hosts


# if called directly, list all upgrades
if __name__ == '__main__':
    list_upgrades()
