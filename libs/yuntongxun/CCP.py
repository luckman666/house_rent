from .CCPRestSDK import REST

_accountSid = '8aaf07086541761801655005c05d070c'
_accountToken = '9e9f2e409bae4f68854704cce486ec48'
_aapId='8aaf07086541761801655005c0b20712'
_serverIP='sandboxapp.cloopen.com'
_serverPort= 8883
_softVersion="2013-12-26"

class _CCP(object):

    def __init__(self):
        self.rest = REST(_serverIP, _serverPort, _softVersion)
        self.rest.setAccount(_accountSid,_accountToken)
        self.rest.setAppId(_aapId)

    @classmethod
    def instance(cls):
        if not hasattr(cls, "_instance"):
            cls._instance =cls()
        return cls._instance

    def sendTemplateSMS(self, to, datas, tempId):
        return self.rest.sendTemplateSMS(to, datas, tempId)

ccp = _CCP.instance()

if __name__ == "__main__":
    ccp.sendTemplateSMS('18500451512', ['1234',5], 1)


