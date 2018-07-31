# -*- coding: UTF-8 -*-
from __future__ import print_function

import os
import json
import logging
from sys import argv

import tornado.options
from tornado.log import LogFormatter

from Handler.UploadPyFileHandler import UploadPyFileHandler
from Handler.CompilePyHandler import CompilePyHandler
from Handler.TestHandler import TestHandler

import Config

if __name__ == "__main__":
    tornado.options.options.logging = "debug"
    tornado.options.parse_command_line()
    datefmt = '%Y-%m-%d %H:%M:%S'
    fmt = '%(color)s[%(levelname)1.1s %(asctime)s] %(message)s%(end_color)s'
    formatter = LogFormatter(color=True, datefmt=datefmt, fmt=fmt)
    root_log = logging.getLogger()
    for logHandler in root_log.handlers:
        logHandler.setFormatter(formatter)

    if len(argv) != 2:
        print('usage: StrategyCompiler.py {config file name}')
    else:
        with open(argv[1]) as configFile:
            _config = json.load(configFile)

        Config.workingDir = _config['workingDir']
        Config.forwardUrl = _config['forwardUrl']
        crtPath = _config['crtPath']
        keyPath = _config['keyPath']

        application = tornado.web.Application(handlers=[
            (r"/", UploadPyFileHandler),
            (r"/upload.do", UploadPyFileHandler),
            (r"/test.do", TestHandler),
            (r"/compile.do", CompilePyHandler)],
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static")
        )

        http_server = tornado.httpserver.HTTPServer(application, ssl_options={
            "certfile": crtPath,
            "keyfile": keyPath,
        }, decompress_request=True)
        http_server.listen(_config['port'])

        root_log.info("staring strategy compiler.")

        tornado.ioloop.IOLoop.instance().start()
