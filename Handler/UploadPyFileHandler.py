# -*- coding: UTF-8 -*-
import tornado.web
import time
import requests

from Handler.Compile import *
import Config

class UploadPyFileHandler(tornado.web.RequestHandler):
    def post(self):
        result = {}
        #result['msg'] = 'ok'

        strategyId = self.request.headers.get('strategyId')
        fileName = self.request.headers.get('fileName')
        fileExtension = self.request.headers.get('fileExtension').lower()
        access_token = self.request.headers.get('access_token')

        targetDir = os.path.join(Config.workingDir, strategyId + '_' + time.strftime('_%Y%m%d%H%M%S', time.localtime()))
        if fileExtension == '.py':
            fileName = 'STR' + strategyId

        saveFile(targetDir, fileName + fileExtension, self.request.body)

        if fileExtension == '.py':
            result = compilePyFile(targetDir, fileName + fileExtension)
            if not result:
                result = self._forward(targetDir, strategyId, 'STR' + strategyId, '.so', access_token)
        elif fileExtension == '.so':
            result = self._forward(targetDir, strategyId, fileName, fileExtension, access_token)
        elif fileExtension == '.zip':
            result = compileMFile(targetDir, strategyId, fileName + fileExtension)
            if not result:
                result = self._forward(targetDir, strategyId, 'STR' + strategyId, '.zip', access_token)
        else:
            result = 'unsupported file type ' + fileExtension

        self.write(result)
        self.flush()

    def _forward(self, path, strategyId, fileName, fileExtension, access_token):
        headers = {'fileName':fileName, 'fileExtension': fileExtension, 'strategyId': strategyId, 'access_token': access_token}
        filePathName = ''
        if(sys.version_info.major >= 3){
            filePathName = os.path.join(path, fileName + '.cpython-37m-x86_64-linux-gnu' + fileExtension)
        }else{
            filePathName = os.path.join(path, fileName + fileExtension)
        }
        with open(filePathName, 'rb') as data:
            res = requests.post(Config.forwardUrl, headers=headers, data=data)
            if res.status_code == 200 :
                 #result = json.dumps({"msg" : "success", "status" : 200})
                 result = res.content
            else:
                 result = '{"msg" : "upload error", "status" :"'+ str(res.status_code) +'"}'
            return result
