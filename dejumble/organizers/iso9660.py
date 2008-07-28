import os
import os.path
import math
import re
import logging

from ..organizer import Organizer

iso9660_increase_regex = re.compile('^(.*)~(\d+)$')

logger = logging.getLogger('dejumble.Organizer')


class ISO9660Organizer(Organizer):
    def generatepaths(self, realpath):
        parts = pathparts(removeroot(realpath, self.cache.filter.root))

        if len(parts) <= 1:
            yield addtrailingslash(self.convertpath(parts[0]))
        else:
            currentpath = os.sep
            currentrealpath = self.cache.filter.root

            for part in parts[:-1]:
                currentrealpath = os.path.join(currentrealpath, part)
                part = list(self.paths(currentrealpath))[0]
                currentpath = os.path.join(currentpath, part)

            yield os.path.join(currentpath, self.convertpath(parts[-1:][0]))

    def increasefilename(self, filename):
        root, ext = os.path.splitext(filename)
    
        num = 1
        matches = iso9660_increase_regex.match(root)
    
        if not matches is None:
            num = int(matches.group(2)) + 1
            root = matches.group(1)

        return self.convertpath("%s%s" % (root, ext), num)

    def convertpath(self, filename, num=0):
        root, ext = os.path.splitext(filename)

        # TODO: exclude all non valid characters
        root = root.replace(' ', '')
        root = root.replace('+', '_')

        size = int(6 - math.log10(len(str(num))))
        
        if len(root) > size or num > 0:
            if num == 0:
                num = 1
            return "%s~%s%s" % (root.upper()[0:size], num, ext.upper()[0:4])
        else:
            return "%s%s" % (root.upper(), ext.upper()[0:4])

