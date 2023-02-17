from PyQt5.QtCore import QThread, pyqtSignal
import requests


class SendMessage(QThread):
    ret = pyqtSignal(dict)
    def __init__(self, proxy_sites, question):
        super().__init__()
        self.proxy_sites = proxy_sites
        self.question = question
        return
    
    def run(self):
        ret = {'result': None}
        for site in self.proxy_sites:
            try:
                req = getattr(requests, site['method'])(
                    site['url'], 
                    data=site['data'](self.question),
                    headers=site['headers'],
                    timeout=200
                    )
                if req.status_code == 200:
                    ret['result'] = req.json()
                    break
            except Exception as e:
                print(e)
        self.ret.emit(ret)
        return