# -*- coding: UTF-8 -*-

import Handler
import json
import tornado.options
from Handler.UploadPyFileHandler import UploadPyFileHandler
from Handler.CompilePyHandler import CompilePyHandler
from Handler.TestHandler import TestHandler

_config = {}

if __name__ == "__main__":
    from sys import argv
    from tornado.log import LogFormatter
    import logging

    tornado.options.options.logging = "debug"
    tornado.options.parse_command_line()
    datefmt = '%Y-%m-%d %H:%M:%S'
    fmt = '%(color)s[%(levelname)1.1s %(asctime)s] %(message)s%(end_color)s'
    formatter = LogFormatter(color=True, datefmt=datefmt, fmt=fmt)
    root_log = logging.getLogger()
    for logHandler in root_log.handlers:
        logHandler.setFormatter(formatter)

    if len(argv) != 2:
        print 'usage: StrategyCompiler.py {config file name}'
    else:
        with open(argv[1]) as configFile:
            _config = json.load(configFile)

        Handler.UploadPyFileHandler.workingDir = _config['workingDir']
        Handler.UploadPyFileHandler.forwardUrl = _config['forwardUrl']
        crtPath = _config['crtPath']
        keyPath = _config['keyPath']

        application = tornado.web.Application([
            (r"/", UploadPyFileHandler),
            (r"/test.do", TestHandler),
            (r"/compile.do", CompilePyHandler),
        ])

        http_server = tornado.httpserver.HTTPServer(application, ssl_options={
            "certfile": crtPath,
            "keyfile": keyPath,
        }, decompress_request=True)
        http_server.listen(_config['port'])

        root_log.info("staring strategy compiler.")

        tornado.ioloop.IOLoop.instance().start()
