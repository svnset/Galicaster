# -*- coding:utf-8 -*-
# Galicaster, Multistream Recorder and Player
#
#       tests/core/context
#
# Copyright (c) 2011, Teltek Video Research <galicaster@teltek.es>
#
# This work is licensed under the Creative Commons Attribution-
# NonCommercial-ShareAlike 3.0 Unported License. To view a copy of 
# this license, visit http://creativecommons.org/licenses/by-nc-sa/3.0/ 
# or send a letter to Creative Commons, 171 Second Street, Suite 300, 
# San Francisco, California, 94105, USA.


"""
Functional tests for `galicaster.functional.module` module.
"""
from unittest import TestCase
from nose.plugins.attrib import attr
from galicaster.core.conf import Conf
from dogtail.config import config
from tests import get_resource
import datetime
import time
import shutil
import os
import re

@attr('nodefault', 'f_recording', 'functional')
class TestFunctional(TestCase):

    def setUp(self):
        """ Set up clear conf with a custom logger and repository folder.
        """
        self.conf_path = '/etc/galicaster/conf.ini'
        identifier = self.id().split('.')
        identifier.reverse()
        test_number = re.sub('\D','',identifier[0])
        self.test_path = '/tmp/test{}'.format(test_number)

        if os.path.exists(self.conf_path) and not os.path.exists('{}.old'.format(self.conf_path)):
            os.rename(self.conf_path,'{}.old'.format(self.conf_path))
        shutil.copyfile(get_resource('conf/functional_test.ini'),'/etc/galicaster/conf.ini')
        if not os.path.exists(self.test_path):
            os.makedirs('{}/logs/'.format(self.test_path))
        self.conf = Conf()

        self.conf.set('basic','repository','{}/Repository'.format(self.test_path))
        self.conf.set('logger','path','{}/logs/galicaster.log'.format(self.test_path))
        self.conf.update()

        config.load({'logDir':'{}/logs/'.format(self.test_path)})
        from . import recording

    def tearDown(self):
        os.rename(self.conf_path,'{}/conf.ini'.format(self.test_path))
        if os.path.exists('{}.old'.format(self.conf_path)):
            os.rename('{}.old'.format(self.conf_path),self.conf_path)
        recording.quit()
        del self.conf

    def test_136(self):
        """ Do 15 recordings of 10 minutes of duration
        with automatic ingest to Opencast
        """
        self.conf.set('ingest','manual','immediately')
        self.conf.set('ingest','active','true')
        self.conf.update()

        recording.start_galicaster()
        recording.rec(10*60, 15)

    def test_137(self):
        """ Check nightly ingest while recording is paused
        """
        self.conf.set('ingest','manual','nightly')
        self.conf.set('ingest','active','true')
        night = datetime.datetime.now() + datetime.timedelta(minutes=1)
        self.conf.set('heartbeat','night',night.strftime('%H:%M'))
        self.conf.update()

        recording.start_galicaster()
        recording.rec(5)
        recording.go_to_recorder()
        recording.start_recording()
        recording.pause_recording()
        remaining_sleep = night - datetime.datetime.now() 
        time.sleep(remaining_sleep.seconds)
        recording.rewind_recording()
        recording.stop_recording()
        recording.go_to_distrib()

