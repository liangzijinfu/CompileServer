# -*- coding: UTF-8 -*-
import tornado.web
import time

from Compile import *
import Config

class CompilePyHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("compile.html")

    def post(self):
        result = {}

        files = self.request.files.get('pyFile')
        if files:
            uploadFileName = files[0].get('filename')
            str = uploadFileName.split('.')
            fileName = str[0]
            fileExtension = '.' + str[1]

        targetDir = os.path.join(Config.workingDir, fileName + '_' + time.strftime('_%Y%m%d%H%M%S', time.localtime()))
        saveFile(targetDir, fileName + fileExtension, files[0].body)

        if fileExtension == '.py':
            result = compilePyFile(targetDir, fileName + fileExtension)
            if not result:
                self.set_header('Content-Type', 'application/octet-stream')
                self.set_header('Content-Disposition', 'attachment; filename=' + fileName + '.so')

                soFilePath = os.path.join(targetDir, fileName + '.so')
                with open(soFilePath, 'rb') as f:
                    while True:
                        data = f.read(4096)
                        if not data:
                            break
                        self.write(data)
            else:
                self.set_status(500)
                self.write(result)
        else:
            self.set_status(400)
            self.write('unsupported file ' + uploadFileName)

        self.finish()
