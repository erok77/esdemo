
# %%
###
# todo: >> enable the ssm as optional, include script to populate ssm from env, json, etc
#       >> clean up app config
#


import boto3
import os
import sys

from logging import getLogger
logger = getLogger(__name__)

from utils import cached_property



__all__ = ['AppConfigContext', 'ConfigContext']

class AppConfigContext(object):

    @cached_property
    def code(self):
        return os.getenv('CODE') if os.getenv('CODE') else 'xhs'

    @cached_property
    def build_version(self):
        return os.getenv('BUILD_VERSION') if os.getenv('BUILD_VERSION') else 'v0.77'

    @cached_property
    def git_branch(self):
        return os.getenv('GIT_BRANCH') if os.getenv('GIT_BRANCH') else 'master'

    @cached_property
    def git_commit(self):
        return os.getenv('GIT_COMMIT') if os.getenv('GIT_COMMIT') else '11293'

    @cached_property
    def name(self):
        return os.getenv('NAME') if os.getenv('NAME') else '72Kings - k72'

    @cached_property
    def stage(self):
        return os.getenv('STAGE') if os.getenv('STAGE') else 'dev'

    @cached_property
    def service(self):
        return os.getenv('SERVICE') if os.getenv('SERVICE') else 'service'

    @cached_property
    def loglevel(self):
        return os.getenv('LOGLEVEL') if os.getenv('LOGLEVEL') else logging.INFO

class ConfigContext:
    app = AppConfigContext()
    stage = app.stage
    service = app.service
    ssm_path = '/k72-%s/%s/' % (stage, service)
#    ssm = boto3.client('ssm')

    def __init__(self):
        pass

    def __iter__(self):
        pass


    '''
    def _get_ssm(self, key):
        try:
            logger.debug('{key}:: >> TRYING SSM FOR KEY'.format(key=key))
            params = self.ssm.get_parameter(
                Name=self.ssm_path+key, WithDecryption=True)
            logger.debug(params)
            if params['Parameter']['Name'] == self.ssm_path+key.lower():
                key, value = key, params['Parameter']['Value']
                logger.debug(
                    '{key}:: >> FOUND K/V PAIR IN SSM {key}::{val}'.format(key=key, val=value))
                object.__setattr__(self, key, value)
                logger.debug('{key}::{value} >> SETATTR SUCCESSFUL'.format(
                    key=key, value=value))
                return value
            else:
                logger.debug('{key}:: >> SSM FAILED'.format(key=key))
                return False
        except Exception as e:
            logger.debug('{key}:: >> SSM FAILED WITH EXCEPTION, {e}'.format(key=key, e=e))
    '''
    def _get_environ(self, key):
        logger.debug('{key}:: >> TRYING OS.ENVIRON FOR KEY'.format(key=key))
        """ get env vars """
        if key in os.environ:
            key, value = key, os.environ[key]
            logger.debug(
                '{key}:: >> FOUND K/V PAIR IN OS.ENVIRON {key}::{val}'.format(key=key, val=value))
            object.__setattr__(self, key, value)
            logger.debug('{key}::{value} >> SETATTR SUCCESSFUL'.format(
                key=key, value=value))
            return value
        else:
            logger.debug('{key}:: >> FAILED OS.ENVIRON FOR KEY'.format(key=key))
            return False

    def _get_local(self, key):
        logger.debug('{key}:: >> TRYING LOCAL FOR KEY'.format(key=key))
        if key in self.__dict__:
            logger.debug('{key}:: >> FOUND KEY IN LOCAL __DICT__'.format(key=key))
            return object.__getattribute__(key)
        else:
            logger.debug('{key}:: >> LOCAL __DICT__ FAILED'.format(key=key))
            return False

    def __getattr__(self, key):
#        value = self._get_local(key.upper())
#        if value is not False:
#            return value
#        else:
#            logger.debug('{key} NOT IN LOCAL __DICT__'.format(key=key.upper()))
        value = self._get_environ(key.upper())
        if value is not False:
            return value
        else:
            logger.debug('{key} FAILED OS.ENVIRON'.format(key=key.upper()))
#        value = self._get_ssm(key.upper())
        if value is not False:
            return value
        else:
            logger.debug('Issue finding key {key}'.format(key=key.upper()))

    def __setattr__(self, key, value):
        try:
            object.__setattr__(self, key.upper(), value)
            logger.debug('{key}::{value} >> SETATTR SUCCESSFUL'.format(
                key=key.upper(), value=value))
        except Exception as e:
            logger.debug('__setattr__ failed::' + e)
