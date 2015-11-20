# -*- coding: GB18030 -*-
#
# Copyright (c) 2015 Baidu.com, Inc. All Rights Reserved
#
"""
模块用途描述

Authors: zhangzhenhu@baidu.com
Date:    2015/11/20 17:21
"""
import os


def load_config():
    """加载配置类"""
    mode = os.environ.get('MODE')
    try:
        if mode == 'LOCAL':
            from .local import LocalConfig
            return LocalConfig
        elif mode == 'ONLINE':
            from .online import OnlineConfig
            return OnlineConfig
        else:
            from .default import Config
            return Config
    except ImportError, e:
        from .default import Config
        return Config
