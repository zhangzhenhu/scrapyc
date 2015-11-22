# -*- coding: utf-8 -*-
"""
hbase

Authors: acmtiger@gmail.com
Date:    2015/11/16 9:42
"""
import sys
import happybase
from optparse import OptionParser

__version__ = '0.1'

__decode__ = "utf8"


def scan(table):
    for row_key, row_data in table.scan():
        for k, v in row_data.iteritems():
            print "%s\t%s\t%s" % (row_key, k, v)


def init_option():
    """
    初始化命令行参数项
    Returns:
        OptionParser 的parser对象
    """

    # OptionParser 自己的print_help()会导致乱码，这里禁用自带的help参数
    parser = OptionParser(add_help_option=False, version=__version__)
    parser.add_option("-s", dest="scan",
                      help=u"scan")
    parser.add_option("-t", dest="table",
                      help=u"table")
    parser.add_option("-c", "--column",
                      dest="column",
                      help=u"和-t参数配合使用，当从某个任务启动时，是否执行后续任务 ")
    parser.add_option("-H", "--host", default="localhost",
                      dest="host",
                      help=u"从上次断点恢复执行")
    parser.add_option("-P", "--port",
                      dest="port",
                      help=u"")
    parser.add_option("-d", "--debug", action="store_true", default=False,
                      dest="debug",
                      help=u"开启debug模式")
    parser.add_option("-h", "--help", action="store_true", dest="help", default=False,
                      help=u"打印帮助信息")
    return parser


if __name__ == "__main__":

    parser = init_option()
    (options, args) = parser.parse_args()

    if options.help:
        # OptionParser 自己的print_help()会导致乱码
        usage = parser.format_help()
        print usage.encode("utf8")
        quit()
    elif options.table:
        table = options.table
    conn = happybase.Connection("localhost")
    table = conn.table(table)
    scan(table)