# -*- coding: UTF-8 -*-
import tornado.web
import time
import requests

from Compile import *

workingDir = ''
forwardUrl = ''

class CompilePyHandler(tornado.web.RequestHandler):
    def get(self):
        with open("", 'rb') as f:
            while True:
                data = f.read(4096)
                if not data:
                    break
                self.write(data)

    def post(self):
        result = {}

        fileName = self.request.headers.get('fileName')
        fileExtension = self.request.headers.get('fileExtension').lower()

        targetDir = os.path.join(workingDir, fileName + '_' + time.strftime('_%Y%m%d%H%M%S', time.localtime()))
        saveFile(targetDir, fileName, self.request.body)

        if fileExtension == '.py':
            result = compilePyFile(targetDir, fileName + fileExtension)
            if not result:
                self.set_header('Content-Type', 'application/octet-stream')
                self.set_header('Content-Disposition', 'attachment; filename=' + fileName + '.so')

                with open(result, 'rb') as f:
                    while True:
                        data = f.read(4096)
                        if not data:
                            break
                        self.write(data)
        else:
            result = "unsupported file extension " + fileExtension
            self.write(result)

        self.finish()
