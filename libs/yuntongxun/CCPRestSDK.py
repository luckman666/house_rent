
import hashlib
import base64
import datetime
import urllib.request, urllib.error, urllib.parse
import json
from .xmltojson import xmltojson
from xml.dom import minidom 

class REST():
    
    AccountSid=''
    AccountToken=''
    AppId=''
    SubAccountSid=''
    SubAccountToken=''
    ServerIP=''
    ServerPort=''
    SoftVersion=''
    
    def __init__(self,ServerIP,ServerPort,SoftVersion):

        self.ServerIP = ServerIP;
        self.ServerPort = ServerPort;
        self.SoftVersion = SoftVersion;
    
    
    
    def setAccount(self,AccountSid,AccountToken):
      self.AccountSid = AccountSid;
      self.AccountToken = AccountToken;   
    

 
    def setSubAccount(self,SubAccountSid,SubAccountToken):
      self.SubAccountSid = SubAccountSid;
      self.SubAccountToken = SubAccountToken;    


    def setAppId(self,AppId):
       self.AppId = AppId; 
    
    def log(self,url,body,data):
        print('这是请求的URL：')
        print (url);
        print('这是请求包体:')
        print (body);
        print('这是响应包体:')
        print (data);
        print('********************************')
    

    def CreateSubAccount(self, friendlyName):
        
        self.accAuth()
        nowdate = datetime.datetime.now()
        self.Batch = nowdate.strftime("%Y%m%d%H%M%S")
        signature = self.AccountSid + self.AccountToken + self.Batch;
        sig = hashlib.sha256(signature).hexdigest().upper()

        url = "https://"+self.ServerIP + ":" + str(self.ServerPort) + "/" + self.SoftVersion + "/Accounts/" + self.AccountSid + "/SubAccounts?sig=" + sig
        src = self.AccountSid + ":" + self.Batch;
        auth = base64.b64encode(src.encode(encoding='utf-8')).strip()
        req = urllib.request.Request(url)
        self.setHttpHeader(req)
        req.add_header("Authorization", auth)
        body ='''<?xml version="1.0" encoding="utf-8"?><SubAccount><appId>%s</appId>\
            <friendlyName>%s</friendlyName>\
            </SubAccount>\
            '''%(self.AppId, friendlyName)
        
        if self.BodyType == 'json': 
            body = '''{"friendlyName": "%s", "appId": "%s"}'''%(friendlyName,self.AppId)
        data=''
        req.add_data(body)
        try:
            res = urllib.request.urlopen(req);
            data = res.read()
            res.close()
        
            if self.BodyType=='json':
                locations = json.loads(data)
            else:
                xtj=xmltojson()
                locations=xtj.main(data)
            if self.Iflog:
                self.log(url,body,data)
            return locations
        except Exception as error:
            if self.Iflog:
                self.log(url,body,data)
            return {'172001':'网络错误'}
    
    def getSubAccounts(self, startNo,offset):

        self.accAuth()
        nowdate = datetime.datetime.now()
        self.Batch = nowdate.strftime("%Y%m%d%H%M%S")
        signature = self.AccountSid + self.AccountToken + self.Batch;
        sig = hashlib.sha256(signature).hexdigest().upper()

        url = "https://"+self.ServerIP + ":" + str(self.ServerPort) + "/" + self.SoftVersion + "/Accounts/" + self.AccountSid + "/GetSubAccounts?sig=" + sig
        src = self.AccountSid + ":" + self.Batch;
        auth = base64.b64encode(src.encode(encoding='utf-8')).strip()
        req = urllib.request.Request(url)
        self.setHttpHeader(req)
        req.add_header("Authorization", auth)
        body ='''<?xml version="1.0" encoding="utf-8"?><SubAccount><appId>%s</appId>\
            <startNo>%s</startNo><offset>%s</offset>\
            </SubAccount>\
            '''%(self.AppId, startNo, offset)
        
        if self.BodyType == 'json':   
            body = '''{"appId": "%s", "startNo": "%s", "offset": "%s"}'''%(self.AppId,startNo,offset)
        data=''
        req.add_data(body)
        try:
            res = urllib.request.urlopen(req);
            data = res.read()
            res.close()
        
            if self.BodyType=='json':
                locations = json.loads(data)
            else:
                xtj=xmltojson()
                locations=xtj.main(data)
            if self.Iflog:
                self.log(url,body,data)
            return locations
        except Exception as error:
            if self.Iflog:
                self.log(url,body,data)
            return {'172001':'网络错误'}


    def querySubAccount(self, friendlyName):

        self.accAuth()
        nowdate = datetime.datetime.now()
        self.Batch = nowdate.strftime("%Y%m%d%H%M%S")
        signature = self.AccountSid + self.AccountToken + self.Batch;
        sig = hashlib.sha256(signature).hexdigest().upper()
        url = "https://"+self.ServerIP + ":" + str(self.ServerPort) + "/" + self.SoftVersion + "/Accounts/" + self.AccountSid + "/QuerySubAccountByName?sig=" + sig
        src = self.AccountSid + ":" + self.Batch;
        auth = base64.b64encode(src.encode(encoding='utf-8')).strip()
        req = urllib.request.Request(url)
        self.setHttpHeader(req)
        
        req.add_header("Authorization", auth)
        
        body ='''<?xml version="1.0" encoding="utf-8"?><SubAccount><appId>%s</appId>\
            <friendlyName>%s</friendlyName>\
            </SubAccount>\
            '''%(self.AppId, friendlyName)
        if self.BodyType == 'json':   
            
            body = '''{"friendlyName": "%s", "appId": "%s"}'''%(friendlyName,self.AppId)
        data=''
        req.add_data(body)
        try:
            res = urllib.request.urlopen(req);
            data = res.read()
            res.close()
        
            if self.BodyType=='json':
                locations = json.loads(data)
            else:
                xtj=xmltojson()
                locations=xtj.main(data)
            if self.Iflog:
                self.log(url,body,data)
            return locations
        except Exception as error:
            if self.Iflog:
                self.log(url,body,data)
            return {'172001':'网络错误'}
        
    def sendTemplateSMS(self, to,datas,tempId):

        self.accAuth()
        nowdate = datetime.datetime.now()
        self.Batch = nowdate.strftime("%Y%m%d%H%M%S")
        signature = self.AccountSid + self.AccountToken + self.Batch;
        sig = hashlib.sha256(signature.encode('utf-8')).hexdigest().upper()
        url = "https://"+self.ServerIP + ":" + str(self.ServerPort) + "/" + self.SoftVersion + "/Accounts/" + self.AccountSid + "/SMS/TemplateSMS?sig=" + sig
        src = self.AccountSid + ":" + self.Batch;
        auth = base64.b64encode(src.encode(encoding='utf-8')).strip()
        req = urllib.request.Request(url)
        self.setHttpHeader(req)
        req.add_header("Authorization", auth)
        b=''
        for a in datas:
            b+='<data>%s</data>'%(a)
        
        body ='<?xml version="1.0" encoding="utf-8"?><SubAccount><datas>'+b+'</datas><to>%s</to><templateId>%s</templateId><appId>%s</appId>\
            </SubAccount>\
            '%(to, tempId,self.AppId)
        if self.BodyType == 'json':   
            b='['
            for a in datas:
                b+='"%s",'%(a) 
            b+=']'
            body = '''{"to": "%s", "datas": %s, "templateId": "%s", "appId": "%s"}''' % (to,b,tempId,self.AppId)
        req.add_data(body)
        data=''
        try:
            res = urllib.request.urlopen(req);
            data = res.read()
            res.close()
        
            if self.BodyType=='json':
                locations = json.loads(data)
            else:
                xtj=xmltojson()
                locations=xtj.main(data)
            if self.Iflog:
                self.log(url,body,data)
            return locations
        except Exception as error:
            if self.Iflog:
                self.log(url,body,data)
            return {'172001':'网络错误'}

        

    def landingCall(self,to,mediaName,mediaTxt,displayNum,playTimes,respUrl,userData,maxCallTime,speed,volume,pitch,bgsound):

        self.accAuth()
        nowdate = datetime.datetime.now()
        self.Batch = nowdate.strftime("%Y%m%d%H%M%S")
        signature = self.AccountSid + self.AccountToken + self.Batch;
        sig = hashlib.sha256(signature.encode('utf-8')).hexdigest().upper()
        url = "https://"+self.ServerIP + ":" + str(self.ServerPort) + "/" + self.SoftVersion + "/Accounts/" + self.AccountSid + "/Calls/LandingCalls?sig=" + sig
        src = self.AccountSid + ":" + self.Batch;
        auth = base64.b64encode(src.encode(encoding='utf-8')).strip()
        req = urllib.request.Request(url)
        self.setHttpHeader(req)
        req.add_header("Authorization", auth)
        
        body ='''<?xml version="1.0" encoding="utf-8"?><LandingCall>\
            <to>%s</to><mediaName>%s</mediaName><mediaTxt>%s</mediaTxt><appId>%s</appId><displayNum>%s</displayNum>\
            <playTimes>%s</playTimes><respUrl>%s</respUrl><userData>%s</userData><maxCallTime>%s</maxCallTime><speed>%s</speed>
            <volume>%s</volume><pitch>%s</pitch><bgsound>%s</bgsound></LandingCall>\
            '''%(to, mediaName,mediaTxt,self.AppId,displayNum,playTimes,respUrl,userData,maxCallTime,speed,volume,pitch,bgsound)
        if self.BodyType == 'json':   
            body = '''{"to": "%s", "mediaName": "%s","mediaTxt": "%s","appId": "%s","displayNum": "%s","playTimes": "%s","respUrl": "%s","userData": "%s","maxCallTime": "%s","speed": "%s","volume": "%s","pitch": "%s","bgsound": "%s"}'''%(to, mediaName,mediaTxt,self.AppId,displayNum,playTimes,respUrl,userData,maxCallTime,speed,volume,pitch,bgsound)
        req.add_data(body)
        data=''
        try:
            res = urllib.request.urlopen(req);
            data = res.read()
            res.close()
        
            if self.BodyType=='json':
                locations = json.loads(data)
            else:
                xtj=xmltojson()
                locations=xtj.main(data)
            if self.Iflog:
                self.log(url,body,data)
            return locations
        except Exception as error:
            if self.Iflog:
                self.log(url,body,data)
            return {'172001':'网络错误'}
    

    def voiceVerify(self,verifyCode,playTimes,to,displayNum,respUrl,lang,userData):

        self.accAuth()
        nowdate = datetime.datetime.now()
        self.Batch = nowdate.strftime("%Y%m%d%H%M%S")
        signature = self.AccountSid + self.AccountToken + self.Batch;
        sig = hashlib.sha256(signature.encode('utf-8')).hexdigest().upper()
        url = "https://"+self.ServerIP + ":" + str(self.ServerPort) + "/" + self.SoftVersion + "/Accounts/" + self.AccountSid + "/Calls/VoiceVerify?sig=" + sig
        src = self.AccountSid + ":" + self.Batch;
        auth = base64.b64encode(src.encode(encoding='utf-8')).strip()
        req = urllib.request.Request(url)
        self.setHttpHeader(req)
        
        req.add_header("Authorization", auth)
        
        body ='''<?xml version="1.0" encoding="utf-8"?><VoiceVerify>\
            <appId>%s</appId><verifyCode>%s</verifyCode><playTimes>%s</playTimes><to>%s</to><respUrl>%s</respUrl>\
            <displayNum>%s</displayNum><lang>%s</lang><userData>%s</userData></VoiceVerify>\
            '''%(self.AppId,verifyCode,playTimes,to,respUrl,displayNum,lang,userData)
        if self.BodyType == 'json':   
            body = '''{"appId": "%s", "verifyCode": "%s","playTimes": "%s","to": "%s","respUrl": "%s","displayNum": "%s","lang": "%s","userData": "%s"}'''%(self.AppId,verifyCode,playTimes,to,respUrl,displayNum,lang,userData)
        req.add_data(body)
        data=''
        try:
            res = urllib.request.urlopen(req);
            data = res.read()
            res.close()
        
            if self.BodyType=='json':
                locations = json.loads(data)
            else:
                xtj=xmltojson()
                locations=xtj.main(data)
            if self.Iflog:
                self.log(url,body,data)
            return locations
        except Exception as error:
            if self.Iflog:
                self.log(url,body,data)
            return {'172001':'网络错误'}
    

    def ivrDial(self,number,userdata,record):

        self.accAuth()
        nowdate = datetime.datetime.now()
        self.Batch = nowdate.strftime("%Y%m%d%H%M%S")
        signature = self.AccountSid + self.AccountToken + self.Batch;
        sig = hashlib.sha256(signature).hexdigest().upper()
        url = "https://"+self.ServerIP + ":" + str(self.ServerPort) + "/" + self.SoftVersion + "/Accounts/" + self.AccountSid + "/ivr/dial?sig=" + sig
        src = self.AccountSid + ":" + self.Batch;
        auth = base64.b64encode(src.encode(encoding='utf-8')).strip()
        req = urllib.request.Request(url)
        req.add_header("Accept", "application/xml")
        req.add_header("Content-Type", "application/xml;charset=utf-8")
        req.add_header("Authorization", auth)
        
        body ='''<?xml version="1.0" encoding="utf-8"?>
                <Request>
                    <Appid>%s</Appid>
                    <Dial number="%s"  userdata="%s" record="%s"></Dial>
                </Request>
            '''%(self.AppId,number,userdata,record)
        req.add_data(body)
        data=''
        try:
            res = urllib.request.urlopen(req);
            data = res.read()
            res.close()
            xtj=xmltojson()
            locations=xtj.main(data)
            if self.Iflog:
                self.log(url,body,data)
            return locations
        except Exception as error:
            if self.Iflog:
                self.log(url,body,data)
            return {'172001':'网络错误'}
        
    
    def billRecords(self,date,keywords):

        self.accAuth()
        nowdate = datetime.datetime.now()
        self.Batch = nowdate.strftime("%Y%m%d%H%M%S")
        signature = self.AccountSid + self.AccountToken + self.Batch;
        sig = hashlib.sha256(signature).hexdigest().upper()
        url = "https://"+self.ServerIP + ":" + str(self.ServerPort) + "/" + self.SoftVersion + "/Accounts/" + self.AccountSid + "/BillRecords?sig=" + sig
        src = self.AccountSid + ":" + self.Batch;
        auth = base64.b64encode(src.encode(encoding='utf-8')).strip()
        req = urllib.request.Request(url)
        self.setHttpHeader(req)
        req.add_header("Authorization", auth)
        
        body ='''<?xml version="1.0" encoding="utf-8"?><BillRecords>\
            <appId>%s</appId><date>%s</date><keywords>%s</keywords>\
            </BillRecords>\
            '''%(self.AppId,date,keywords)
        if self.BodyType == 'json':   
            body = '''{"appId": "%s", "date": "%s","keywords": "%s"}'''%(self.AppId,date,keywords)
        req.add_data(body)
        data=''
        try:
            res = urllib.request.urlopen(req);
            data = res.read()
            
            res.close()
        
            if self.BodyType=='json':
                locations = json.loads(data)
            else:
                xtj=xmltojson()
                locations=xtj.main(data)
            if self.Iflog:
                self.log(url,body,data)
            return locations
        except Exception as error:
            if self.Iflog:
                self.log(url,body,data)
            return {'172001':'网络错误'}
    

    def queryAccountInfo(self):

        self.accAuth()
        nowdate = datetime.datetime.now()
        self.Batch = nowdate.strftime("%Y%m%d%H%M%S")
        signature = self.AccountSid + self.AccountToken + self.Batch;
        sig = hashlib.sha256(signature).hexdigest().upper()
        url = "https://"+self.ServerIP + ":" + str(self.ServerPort) + "/" + self.SoftVersion + "/Accounts/" + self.AccountSid + "/AccountInfo?sig=" + sig
        src = self.AccountSid + ":" + self.Batch;
        auth = base64.b64encode(src.encode(encoding='utf-8')).strip()
        req = urllib.request.Request(url)
        self.setHttpHeader(req)
        body=''
        req.add_header("Authorization", auth)
        data=''
        try:
            res = urllib.request.urlopen(req);
            data = res.read()
            res.close()
        
            if self.BodyType=='json':
                locations = json.loads(data)
            else:
                xtj=xmltojson()
                locations=xtj.main(data)
            if self.Iflog:
                self.log(url,body,data)
            return locations
        except Exception as error:
            if self.Iflog:
                self.log(url,body,data)
            return {'172001':'网络错误'}
        

    def QuerySMSTemplate(self,templateId):

        self.accAuth()
        nowdate = datetime.datetime.now()
        self.Batch = nowdate.strftime("%Y%m%d%H%M%S")
        signature = self.AccountSid + self.AccountToken + self.Batch;
        sig = hashlib.sha256(signature).hexdigest().upper()
        url = "https://"+self.ServerIP + ":" + str(self.ServerPort) + "/" + self.SoftVersion + "/Accounts/" + self.AccountSid + "/SMS/QuerySMSTemplate?sig=" + sig
        src = self.AccountSid + ":" + self.Batch;
        auth = base64.b64encode(src.encode(encoding='utf-8')).strip()
        req = urllib.request.Request(url)
        self.setHttpHeader(req)
        
        req.add_header("Authorization", auth)
        
        body ='''<?xml version="1.0" encoding="utf-8"?><Request>\
            <appId>%s</appId><templateId>%s</templateId></Request>
            '''%(self.AppId,templateId)
        if self.BodyType == 'json':   
            body = '''{"appId": "%s", "templateId": "%s"}'''%(self.AppId,templateId)
        req.add_data(body)
        data=''
        try:
            res = urllib.request.urlopen(req);
            data = res.read()
            res.close()
        
            if self.BodyType=='json':
                locations = json.loads(data)
            else:
                xtj=xmltojson()
                locations=xtj.main2(data)
            if self.Iflog:
                self.log(url,body,data)
            return locations
        except Exception as error:
            if self.Iflog:
                self.log(url,body,data)
            return {'172001':'网络错误'}
        
    

    def CallResult(self,callSid):

        self.accAuth()
        nowdate = datetime.datetime.now()
        self.Batch = nowdate.strftime("%Y%m%d%H%M%S")
        signature = self.AccountSid + self.AccountToken + self.Batch;
        sig = hashlib.sha256(signature).hexdigest().upper()
        url = "https://"+self.ServerIP + ":" + str(self.ServerPort) + "/" + self.SoftVersion + "/Accounts/" + self.AccountSid + "/CallResult?sig=" + sig + "&callsid=" + callSid
        src = self.AccountSid + ":" + self.Batch;
        auth = base64.b64encode(src.encode(encoding='utf-8')).strip()
        req = urllib.request.Request(url)
        self.setHttpHeader(req)
        body=''
        req.add_header("Authorization", auth)
        data=''
        try:
            res = urllib.request.urlopen(req);
            data = res.read()
            res.close()
        
            if self.BodyType=='json':
                locations = json.loads(data)
            else:
                xtj=xmltojson()
                locations=xtj.main(data)
            if self.Iflog:
                self.log(url,body,data)
            return locations
        except Exception as error:
            if self.Iflog:
                self.log(url,body,data)
            return {'172001':'网络错误'}
        
    def QueryCallState (self,callid,action):

        self.accAuth()
        nowdate = datetime.datetime.now()
        self.Batch = nowdate.strftime("%Y%m%d%H%M%S")
        signature = self.AccountSid + self.AccountToken + self.Batch;
        sig = hashlib.sha256(signature).hexdigest().upper()
        url = "https://"+self.ServerIP + ":" + str(self.ServerPort) + "/" + self.SoftVersion + "/Accounts/" + self.AccountSid + "/ivr/call?sig=" + sig + "&callid=" + callid
        src = self.AccountSid + ":" + self.Batch;
        auth = base64.b64encode(src.encode(encoding='utf-8')).strip()
        req = urllib.request.Request(url)
        self.setHttpHeader(req)
        req.add_header("Authorization", auth)
        
        body ='''<?xml version="1.0" encoding="utf-8"?><Request>\
            <Appid>%s</Appid><QueryCallState callid="%s" action="%s"/>\
            </Request>\
            '''%(self.AppId,callid,action)
        if self.BodyType == 'json':   
            body = '''{"Appid":"%s","QueryCallState":{"callid":"%s","action":"%s"}}'''%(self.AppId,callid,action)
        req.add_data(body)
        data=''
        try:
            res = urllib.request.urlopen(req);
            data = res.read()
            
            res.close()
        
            if self.BodyType=='json':
                locations = json.loads(data)
            else:
                xtj=xmltojson()
                locations=xtj.main(data)
            if self.Iflog:
                self.log(url,body,data)
            return locations
        except Exception as error:
            if self.Iflog:
                self.log(url,body,data)
            return {'172001':'网络错误'}
    
    def MediaFileUpload (self,filename,body):

        self.accAuth()
        nowdate = datetime.datetime.now()
        self.Batch = nowdate.strftime("%Y%m%d%H%M%S")
        signature = self.AccountSid + self.AccountToken + self.Batch;
        sig = hashlib.sha256(signature).hexdigest().upper()
        url = "https://"+self.ServerIP + ":" + str(self.ServerPort) + "/" + self.SoftVersion + "/Accounts/" + self.AccountSid + "/Calls/MediaFileUpload?sig=" + sig + "&appid=" + self.AppId + "&filename=" + filename
        src = self.AccountSid + ":" + self.Batch;
        auth = base64.b64encode(src.encode(encoding='utf-8')).strip()
        req = urllib.request.Request(url)
        req.add_header("Authorization", auth)
        if self.BodyType == 'json':
            req.add_header("Accept", "application/json")
            req.add_header("Content-Type", "application/octet-stream")
            
        else:
            req.add_header("Accept", "application/xml")
            req.add_header("Content-Type", "application/octet-stream")

        
        req.add_data(body)


        try:
            res = urllib.request.urlopen(req);
            data = res.read()
            
            res.close()
        
            if self.BodyType=='json':
                locations = json.loads(data)
            else:
                xtj=xmltojson()
                locations=xtj.main(data)
            if self.Iflog:
                self.log(url,body,data)
            return locations
        except Exception as error:
            if self.Iflog:
                self.log(url,body,data)
            return {'172001':'网络错误'}
    
    def subAuth(self):
        if(self.ServerIP==""):
            print('172004');
            print('IP为空');
        
        if(str(self.ServerPort)<=0):
            print('172005');
            print('端口错误（小于等于0）');
        
        if(self.SoftVersion==""):
            print('172013');
            print('版本号为空');
        
        if(self.SubAccountSid==""):
            print('172008');
            print('子帐号为空');
        
        if(self.SubAccountToken==""):
            print('172009');
            print('子帐号令牌为空');
        
        if(self.AppId==""):
            print('172012');
            print('应用ID为空');
    
    def accAuth(self):
        if(self.ServerIP==""):
            print('172004');
            print('IP为空');
        
        if(self.ServerPort)<=0:
            print('172005');
            print('端口错误（小于等于0）');
        
        if(self.SoftVersion==""):
            print('172013');
            print('版本号为空');
        
        if(self.AccountSid==""):
            print('172006');
            print('主帐号为空');
        
        if(self.AccountToken==""):
            print('172007');
            print('主帐号令牌为空');
        
        if(self.AppId==""):
            print('172012');
            print('应用ID为空');



    def setHttpHeader(self,req):
        if self.BodyType == 'json':
            req.add_header("Accept", "application/json")
            req.add_header("Content-Type", "application/json;charset=utf-8")
            
        else:
            req.add_header("Accept", "application/xml")
            req.add_header("Content-Type", "application/xml;charset=utf-8")
    