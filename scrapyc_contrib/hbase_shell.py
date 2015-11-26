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


def scan(table, options):

    count = 0
    for row_key, row_data in table.scan(row_start=options.start, row_stop=options.end, columns=options.columns, sorted_columns=False):

        for k in sorted(row_data.keys()):
            v = row_data[k]
            print "%s\t%s\t%s" % (row_key, k, v)
        count += 1
    print >>sys.stderr, "Rows:", count


def get(table, options):

    row_data = table.row(options.start,options.columns)
    for k in sorted(row_data.keys()):
        v = row_data[k]
        print "%s\t%s" % (k, v)
def init_option():
    """
    初始化命令行参数项
    Returns:
        OptionParser 的parser对象
    """

    # OptionParser 自己的print_help()会导致乱码，这里禁用自带的help参数
    parser = OptionParser(add_help_option=False, version=__version__)
    parser.add_option("-s", "--scan", action="store_true", dest="scan", default=False,
                      help=u"scan")
    parser.add_option("-g", "--get", action="store_true", dest="get", default=False,
                      help=u"get one")


    parser.add_option("-t", "--table", dest="table",
                      help=u"table")
    parser.add_option("-S", "--start", dest="start",
                      help=u"row start")
    parser.add_option("-E", "--end", dest="end",
                      help=u"row end")

    parser.add_option("-c", "--columns",
                      dest="columns",
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
    if options.columns:
        options.columns = options.columns.split(",")
    conn = happybase.Connection("localhost")
    # import pdb
    # pdb.set_trace()
    table = conn.table(table)
    if options.scan:
        scan(table, options)
    elif options.get:
        get(table, options)
