# -*- coding: UTF-8 -*-
#
# Juan Hernandez, 2013, 2014
#
#

from fabric.api import local, env, run, cd
from fabric.contrib.console import confirm

env.user = 'juan'
env.password = ''
env.hosts = ['dev']
local_path = '/opt/python/apps/'
remote_path = '/opt/python/apps/'
project_name = 'mihair_spree'


def rsync_servers():
    """Sync with test servers"""
    for x in env.hosts:
        rsync = 'rsync -avz %s%s %s@%s:%s' % (local_path,
                                              project_name,
                                              env.user,
                                              x,
                                              remote_path)
        local(rsync)

