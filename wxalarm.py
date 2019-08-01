#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys
from wxalarmlib import application, config, utils


if __name__ == '__main__':
    # avoid throw [UnicodeEncodeError: 'ascii' codec can't encode characters]
    _unicode = None
    if sys.version_info < (3, 0):
        _unicode = unicode
        from imp import reload

        reload(sys)
        sys.setdefaultencoding('utf-8')

    else:
        _unicode = str

    # config
    root_dir = utils.absdir(__file__)
    process_id = os.getpid()
    config = config.Config(root_dir, process_id)
    store = application.WxAlarmDataStore(config)

    # application
    app = application.WxAlarmApp(store)
    app.StartMain()

