#!/usr/bin/env python
import os
import sys

gae_path = '/usr/local/google_appengine'

current_path = os.path.abspath(os.path.dirname(__file__))
tests_path = os.path.join(current_path, 'tests')
test_app_path = os.path.join(current_path, 'tests', 'app')
restler_path = os.path.join(current_path, 'restler')
lib_path = os.path.join(current_path, 'lib')

sys.path[0:0] = [
    current_path,
    tests_path,
    test_app_path,
    restler_path,
    lib_path,
    gae_path,
    # SDK libs.
    os.path.join(gae_path, 'lib', 'django_0_96'),
    os.path.join(gae_path, 'lib', 'yaml', 'lib'),
    os.path.join(gae_path, 'lib', 'protorpc'),
    os.path.join(gae_path, 'lib', 'simplejson'),
    os.path.join(gae_path, 'lib', 'fancy_urllib'),
    os.path.join(gae_path, 'lib', 'antlr3'),
    os.path.join(gae_path, 'lib', 'whoosh'),
    os.path.join(gae_path, 'lib', 'WebOb'),
    os.path.join(gae_path, 'lib', 'ipaddr'),
]

import unittest2

import logging
import tempfile

from google.appengine.api import yaml_errors
from google.appengine.tools import dev_appserver
from google.appengine.tools import dev_appserver_main


__unittest = True
from unittest2.main import main_


config = matcher = None

try:
    config, matcher = dev_appserver.LoadAppConfig("tests/app", {})
except yaml_errors.EventListenerError, e:
    logging.error('Fatal error when loading application configuration:\n' + str(e))
except dev_appserver.InvalidAppConfigError, e:
    logging.error('Application configuration file invalid:\n%s', e)

#Configure our dev_appserver setup args
args = dev_appserver_main.DEFAULT_ARGS.copy()
args[dev_appserver_main.ARG_CLEAR_DATASTORE] = True
args[dev_appserver_main.ARG_BLOBSTORE_PATH] = os.path.join(
        tempfile.gettempdir(), 'dev_appserver.test.blobstore')
args[dev_appserver_main.ARG_DATASTORE_PATH] = os.path.join(
        tempfile.gettempdir(), 'dev_appserver.test.datastore')
args[dev_appserver_main.ARG_PROSPECTIVE_SEARCH_PATH] = os.path.join(
        tempfile.gettempdir(), 'dev_appserver.test.matcher')
args[dev_appserver_main.ARG_HISTORY_PATH] = os.path.join(
        tempfile.gettempdir(), 'dev_appserver.test.datastore.history')

from google.appengine.api import app_identity
dev_appserver.SetupStubs(config.application, **args)
os.environ['APPLICATION_ID'] = 'dev~%s' % app_identity.get_application_id()


if __name__ == "__main__":
    sys.argv = ['unit2', 'discover', '--start-directory', 'tests']
    main_()
