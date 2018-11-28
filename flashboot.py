#!/usr/bin/env python
# coding=utf-8

import sys
import logging
import dhcpserver
import tftpserver
import optparse
import socket
import os
import thread


def main():
    usage = "Usage: %prog [options] <interface> <boot-file>"
    parser = optparse.OptionParser(usage=usage)
    parser.add_option("-v", "--verbose", dest="loglevel", action="store_const",
                      const=logging.INFO, help="Output messages.", default=logging.WARNING)

    (options, args) = parser.parse_args()

    if len(args) != 2:
        parser.print_help()
        return 1

    iface, bootfile = args
    logging.basicConfig(stream=sys.stdout, level=options.loglevel,
                        format='%(levelname)s(%(name)s): %(message)s')

    try:
        bootFullName = os.path.abspath(bootfile)
        bootDir = os.path.dirname(bootFullName)
        bootFile = os.path.basename(bootFullName)

        thread.start_new_thread(dhcpserver.main_work,
                                (iface, bootFile, options.loglevel))
        thread.start_new_thread(tftpserver.main_work,
                                (iface, bootDir, options.loglevel))

        raw_input("")

    except:
        return 1

    return 0


if __name__ == '__main__':
    main()
