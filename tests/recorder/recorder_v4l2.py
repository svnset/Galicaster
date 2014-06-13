# -*- coding:utf-8 -*-
# Galicaster, Multistream Recorder and Player
#
#       tests/recorder/recorder
#
# Copyright (c) 2011, Teltek Video Research <galicaster@teltek.es>
#
# This work is licensed under the Creative Commons Attribution-
# NonCommercial-ShareAlike 3.0 Unported License. To view a copy of 
# this license, visit http://creativecommons.org/licenses/by-nc-sa/3.0/ 
# or send a letter to Creative Commons, 171 Second Street, Suite 300, 
# San Francisco, California, 94105, USA.

"""
Tests for `galicaster.recorder.recorder` modules.
"""

from os import path
import time
import gtk
from shutil import rmtree
from tempfile import mkdtemp
from unittest import TestCase
from galicaster.utils.mediainfo import get_duration
from galicaster.recorder.recorder import Recorder

gtk.gdk.threads_init()


class TestFunctions(TestCase):
    def setUp(self):
        self.tmppath = mkdtemp()
        self.default_bins = [{'name': 'Bars', 
                              'pattern': '0',
                              'caps': 'video/x-raw-yuv,framerate=25/1,width=640,height=480',
                              'color1': '4294967295',
                              'color2': '4278190080',
                              'location': 'default',
                              'file': 'CAMERA.avi',
                              'device': 'videotest',
                              'flavor': 'presenter',
                              'path': self.tmppath},
                             {'name': 'Static',
                              'device': 'videotest',
                              'location': 'default',
                              'file': 'SCREEN.avi',
                              'flavor': 'presentation',
                              'caps': 'video/x-raw-yuv,framerate=25/1,width=640,height=480',
                              'pattern': '1',
                              'color1': '4294967295',
                              'color2': '4278190080',
                              'path': self.tmppath},
                             {'name': 'Noise',
                              'device': 'audiotest',
                              'location': 'default',
                              'file': 'sound.mp3',
                              'flavor': 'presenter',
                              'pattern': 'pink-noise',
                              'frequency': '440',
                              'volume': '0.3',
                              'player': 'True',
                              'vumeter': 'True',
                              'amplification': '1.0',
                              'path': self.tmppath}]
                             

    def tearDown(self):
        rmtree(self.tmppath)


    def test_constructor(self):
        self.assertRaises(TypeError, Recorder)
        self.assertRaises(TypeError, Recorder, [])
        self.assertRaises(NameError, Recorder, [{'name': 'name'}])
        self.assertRaises(KeyError, Recorder, [{'type': 'v4l2', 'caps': 'raw'}])
        self.assertRaises(KeyError, Recorder, [{'device': 'v4l2', 'caps': 'raw'}])

        #valid
        Recorder([{'name': 'test', 'device': 'v4l2', 'path': self.tmppath}])
        Recorder(self.default_bins)


    def test_get_display_areas_info(self):
        recorder = Recorder(self.default_bins)
        self.assertEqual(recorder.get_display_areas_info(), ['sink-Bars', 'sink-Static'])
        recorder = Recorder([{'name': '1', 'device': 'v4l2', 'caps': 'image/jpeg,framerate=30/1,width=1280,height=720', 'path': self.tmppath}, 
                             {'name': '2', 'device': 'videotest', 'path': self.tmppath}])
        self.assertEqual(recorder.get_display_areas_info(), ['sink-1', 'sink-2'])


    def test_get_bins_info(self):
        recorder = Recorder([{'name': 'name', 'device': 'v4l2', 'caps': 'image/jpeg,framerate=30/1,width=1280,height=720', 'path': self.tmppath}])
        info = recorder.get_bins_info()
        self.assertEqual(info[0]['name'], 'name')
        self.assertEqual(info[0]['path'], self.tmppath)


    def test_preview(self):
        recorder = Recorder([{'name': 'name', 'device': 'v4l2', 'caps': 'image/jpeg,framerate=30/1,width=1280,height=720', 'path': self.tmppath, 'file': '1.avi'}])
        recorder.preview()
        time.sleep(2)
        recorder.stop()
        self.assertEqual(recorder.get_recorded_time(), 0)
        self.assertEqual(path.getsize(path.join(self.tmppath, '1.avi')), 0)


    def test_preview_multi(self):
        recorder = Recorder([{'name': '1', 'device': 'v4l2', 'caps': 'image/jpeg,framerate=30/1,width=1280,height=720', 'path': self.tmppath, 'file': '1.avi', 'pattern': '1'},
                             {'name': '2', 'device': 'videotest', 'path': self.tmppath, 'file': '2.avi'},
                             {'name': '3', 'device': 'pulse', 'path': self.tmppath, 'file': '3.mp3'}])
        recorder.preview()
        time.sleep(4)
        recorder.stop()
        self.assertEqual(recorder.get_recorded_time(), 0)
        self.assertEqual(path.getsize(path.join(self.tmppath, '1.avi')), 0)
        self.assertEqual(path.getsize(path.join(self.tmppath, '2.avi')), 0)
        self.assertEqual(path.getsize(path.join(self.tmppath, '3.mp3')), 0)


    def test_preview_and_record(self):
        recorder = Recorder([{'name': 'name', 'device': 'v4l2', 'caps': 'image/jpeg,framerate=30/1,width=1280,height=720', 'path': self.tmppath, 'file': '1.avi'}])
        recorder.preview_and_record()
        time.sleep(2)
        recorder.stop()
        self.assertTrue(recorder.get_recorded_time() > 0)
        self.assertTrue(path.getsize(path.join(self.tmppath, '1.avi')) > 0)


    def test_preview_and_record_multi(self):
        recorder = Recorder([{'name': '1', 'device': 'v4l2', 'caps': 'image/jpeg,framerate=30/1,width=1280,height=720', 'path': self.tmppath, 'file': '1.avi', 'pattern': '1'},
                             {'name': '2', 'device': 'videotest', 'path': self.tmppath, 'file': '2.avi'},
                             {'name': '3', 'device': 'pulse', 'path': self.tmppath, 'file': '3.mp3'}])
        recorder.preview_and_record()
        time.sleep(4)
        recorder.stop()
        self.assertTrue(recorder.get_recorded_time() > 0)
        self.assertTrue(path.getsize(path.join(self.tmppath, '1.avi')) > 0)
        self.assertTrue(path.getsize(path.join(self.tmppath, '2.avi')) > 0)
        self.assertTrue(path.getsize(path.join(self.tmppath, '3.mp3')) > 0)


    def test_record(self):
        recorder = Recorder([{'name': 'name', 'device': 'v4l2', 'caps': 'image/jpeg,framerate=30/1,width=1280,height=720', 'path': self.tmppath, 'file': '1.avi'}])
        recorder.preview()
        time.sleep(2)
        rec_time = recorder.get_recorded_time()
        #self.assertEqual(rec_time, 0)
        recorder.record()
        time.sleep(2)
        recorder.stop()
        self.assertTrue(recorder.get_recorded_time() > 0)
        self.assertTrue(path.getsize(path.join(self.tmppath, '1.avi')) > 0)
        self.assertEqual(get_duration(path.join(self.tmppath, '1.avi')), 2)


    def test_record_multi(self):
        recorder = Recorder([{'name': '1', 'device': 'v4l2', 'caps': 'image/jpeg,framerate=30/1,width=1280,height=720', 'path': self.tmppath, 'file': '1.avi', 'pattern': '1'},
                             {'name': '2', 'device': 'videotest', 'path': self.tmppath, 'file': '2.avi'},
                             {'name': '3', 'device': 'pulse', 'path': self.tmppath, 'file': '3.mp3'}])
        recorder.preview()
        time.sleep(4)
        rec_time = recorder.get_recorded_time()
        #self.assertEqual(rec_time, 0)
        recorder.record()
        time.sleep(4)
        recorder.stop()
        self.assertTrue(recorder.get_recorded_time() > 0)
        self.assertTrue(path.getsize(path.join(self.tmppath, '1.avi')) > 0)
        self.assertTrue(path.getsize(path.join(self.tmppath, '2.avi')) > 0)
        self.assertTrue(path.getsize(path.join(self.tmppath, '3.mp3')) > 0)
        self.assertEqual(get_duration(path.join(self.tmppath, '1.avi')), 4)
        self.assertEqual(get_duration(path.join(self.tmppath, '2.avi')), 4)
        self.assertEqual(get_duration(path.join(self.tmppath, '3.mp3')), 4)