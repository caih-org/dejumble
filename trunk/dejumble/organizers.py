#!/usr/bin/env python

import logging
import os.path
import time

import dejumble.providers
from dejumble.providers import *
import dejumble.util
from dejumble.util import *

logger = logging.getLogger('dejumble')

def getorganizer(name, provider, query):
    logger.info('provider = ' + provider + 'FileListProvider(' + query + ')')

    provider = {
        'Null': NullFileListProvider,
        'Shell': ShellFileListProvider,
        'Beagle': BeagleFileListProvider,
        'OriginalDirectory': OriginalDirectoryFileListProvider
    }[provider](query)

    logger.info('organizer = ' + name + "Organizer")

    organizer = {
        'Flat': FlatOrganizer,
        'Documents': DocumentsOrganizer,
        'Date': DateOrganizer
    }[name](provider)

    return organizer


class Organizer:
    def __init__(self, provider):
        self.provider = provider
        self.expirecache()

    def isdir(self, path):
        return self._isdir(path)

    def realpath(self, path):
        self.refreshcache()
        if path == '/':
            return ORIGINAL_DIR
        elif path == addtrailingslash(ORIGINAL_DIR):
            return '.'
        elif pathparts(path)[0] == ORIGINAL_DIR:
            return os.path.join('.', '/'.join(pathparts(path)[1:]))
        else:
            filename = os.path.basename(path)
            return self.provider.realpath(addtrailingslash(filename))

    def filelist(self, path):
        self.refreshcache()
        if path == addtrailingslash(ORIGINAL_DIR):
            return getbasefilelist() + os.listdir('.')
        elif pathparts(path)[0] == ORIGINAL_DIR:
            return getbasefilelist() + os.listdir(self.realpath(path))
        else:
            return self._filelist(path)

    def expirecache(self):
        self.expiretime = time.time()

    def refreshcache(self):
        if self.expiretime < time.time():
            self.expiretime = time.time() + 60
            self.provider.refreshfilelist()
            self._refreshcache()

    def _isdir(self, path):
        None

    def _refreshcache(self):
        None


class FlatOrganizer(Organizer):
    def _filelist(self, path):
        return self.provider.filelist()


class DocumentsOrganizer(Organizer):
    def __init__(self, provider):
        Organizer.__init__(self, provider)
        self.filetypes = readconfig('filetypes')

    def _filelist(self, path):
        if path == '/':
            return self.provider.storage.taglist('extension')
        else:
            return self.provider.storage.filelistbytag('extension', path[1:])

    def _isdir(self, path):
        return len(pathparts(path)) == 1

    def _refreshcache(self):
        for filename in self.provider.filelist():
            hastag = False
            for filetype in self.filetypes.keys():
                extensions = self.filetypes[filetype]
                for extension in extensions.split(','):
                    reg = re.compile('%s$' % extension);
                    if not reg.search(filename) == None:
                        self.provider.storage.tag(filename, 'extension', filetype)
                        hastag = True
            if not hastag:
                self.provider.storage.tag(filename, 'extension', 'Other')



class DateOrganizer(Organizer):
    def _filelist(self, path):
        if path == '/':
            return self.provider.storage.taglist('date')
        else:
            return self.provider.storage.filelistbytag('date', path[1:])

    def _isdir(self, path):
        return len(pathparts(path)) == 1

    def _refreshcache(self):
        for filename in filter(isnotdot, self.provider.filelist()):
            stats = os.stat(self.provider.realpath(addtrailingslash(filename)))
            lastmod = time.localtime(stats[8])
            today = time.localtime()
            self.provider.storage.tag(filename, 'date', time.strftime('%Y %B', lastmod))
            if time.strftime('%x', today) == time.strftime('%x', lastmod):
                self.provider.storage.tag(filename, 'date', 'Today')
            if time.strftime('%Y%W', today) == time.strftime('%Y%W', lastmod):
                self.provider.storage.tag(filename, 'date', 'This Week')
            lastweek = time.localtime(time.time() - 7 * 24 * 60 * 60)
            if time.strftime('%Y%W', lastweek) == time.strftime('%Y%W', lastmod):
                self.provider.storage.tag(filename, 'date', 'Last Week')



