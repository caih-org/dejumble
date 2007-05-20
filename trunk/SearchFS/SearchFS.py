#!/usr/bin/env python

#    Copyright (C) 2006  Cesar Izurieta  <cesar@ecuarock.net>
#
#    This program can be distributed under the terms of the GNU LGPL.
#    See the file COPYING.
#

import os
import stat
import errno
import commands

import fuse
from fuse import Fuse

fuse.fuse_python_api = (0, 2)

def filenamepart(path):
    return path.split('/')[-1]

def log(message):
        commands.getoutput('echo `date` "' + message + '" >> ~/.searchfs.log')

def flag2mode(flags):
    md = {os.O_RDONLY: 'r', os.O_WRONLY: 'w', os.O_RDWR: 'w+'}
    m = md[flags & (os.O_RDONLY | os.O_WRONLY | os.O_RDWR)]

    if flags | os.O_APPEND:
        m = m.replace('w', 'a', 1)

    return m


class SearchFS(Fuse):
    def main(self, *a, **kw):
        log('main');
        self.file_class = self.SearchResultFile
        self.executequery();
        return Fuse.main(self, *a, **kw)

    def executequery(self):
        log('executequery: ' + self.query);
        self.files = { '..': '..', '.': '.' }
        filenames = commands.getoutput(self.query).splitlines()
        for r in filenames:
            self.files['/' + filenamepart(r)] = r

    def getattr(self, path):
        st = self.SearchFSStat()
        if path == '/':
            st.st_mode = stat.S_IFDIR | 0755
            st.st_nlink = 2
            return st
        else:
            return os.lstat(self.files[path])

    def readdir(self, path, offset):
        for filename, path in self.files.iteritems():
            yield fuse.Direntry(filename[1:])

    def readlink(self, path):
        return os.readlink(self.files[path])

    def unlink(self, path):
        os.unlink(self.files[path])

    def chmod(self, path, mode):
        os.chmod(self.files[path], mode)

    def chown(self, path, user, group):
        os.chown(self.files[path], user, group)

    def truncate(self, path, len):
        f = open(self.files[path], "a")
        f.truncate(len)
        f.close()

    def utime(self, path, times):
        os.utime(self.files[path], times)

    def access(self, path, mode):
        if not os.access(self.files[path], mode):
            return -EACCES

    class SearchFSStat(fuse.Stat):
        def __init__(self):
            self.st_mode = 0
            self.st_ino = 0
            self.st_dev = 0
            self.st_nlink = 0
            self.st_uid = 0
            self.st_gid = 0
            self.st_size = 0
            self.st_atime = 0
            self.st_mtime = 0
            self.st_ctime = 0

    class SearchResultFile(object):
        def __init__(self, path, flags, *mode):
            self.file = os.fdopen(os.open(server.files[path], flags, *mode), 
                                  flag2mode(flags))
            self.fd = self.file.fileno()

        def read(self, length, offset):
            self.file.seek(offset)
            return self.file.read(length)

        def write(self, buf, offset):
            self.file.seek(offset)
            self.file.write(buf)
            return len(buf)

        def release(self, flags):
            self.file.close()

        def _fflush(self):
            if 'w' in self.file.mode or 'a' in self.file.mode:
                self.file.flush()

        def fsync(self, isfsyncfile):
            self._fflush()
            if isfsyncfile and hasattr(os, 'fdatasync'):
                os.fdatasync(self.fd)
            else:
                os.fsync(self.fd)

        def flush(self):
            self._fflush()
            os.close(os.dup(self.fd))

        def fgetattr(self):
            return os.fstat(self.fd)

        def ftruncate(self, len):
            self.file.truncate(len)


def main():
    global server

    usage = """
SearchFS: mounts a directory with the results of a query.

""" + Fuse.fusage

    server = SearchFS(version="%prog " + fuse.__version__, 
                     usage=usage, 
                     dash_s_do='setsingle')

    server.parser.add_option(mountopt="query", metavar="QUERY", default='locate *.mp3',
                             help="execute QUERY [default: %default]")
    server.parse(values=server, errex=1)

    server.main()

if __name__ == '__main__':
    main()
