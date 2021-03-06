import xbmc, sys
#import pycurl
import StringIO
import os
import res
import re
import vplayCommon

class Login:
    __settings__ = sys.modules[ "__main__" ].__settings__
    __language__ = sys.modules[ "__main__" ].__language__
    __plugin__ = sys.modules[ "__main__" ].__plugin__
    __dbg__ = sys.modules[ "__main__" ].__dbg__
    login_url = res.urls['login']
    
    def __init__(self):
        self.http_lib = vplayCommon.Http()
        self.session = None
        self.username = None
        self.pwd = None
    
    
    def login(self, display=False, login=False):
        self.username   = self.__settings__.getSetting( "username" )
        self.pwd        = self.__settings__.getSetting( "pwd" )
        self.session    = self.__settings__.getSetting( "session" )
        if display == True:
            self.__settings__.openSettings()
            return 0
            
        if not self.username or not self.pwd:
            self.__settings__.openSettings()
    
        if not self.session:
            print "Session not found"
            return self._httpLogin(self.username, self.pwd)

        if login == True:
            print "Login forced !!!!!" 
            return self._httpLogin(self.username, self.pwd)
            
        if self._httpCheckSession(self.session) != True:
            return self._httpLogin(self.username, self.pwd)
        
        return 0

    def getSession(self):
        r = re.compile('^$|^#')
        try:
            data = open(self.http_lib.cookie)
        except:
            raise IOError('Failed to read cokie file')
        
        while 1:
            line = data.readline()
            if not line:
                break
                
            line = line.rstrip('\n')
            if r.match(line):
                continue
               
            cols = line.split()
            if len(cols) != 7:
                continue
            if cols[5] == 'PHPSESSID':
                return cols[6]
        raise ValueError('Could not find session ID')
            
    def _httpCheckSession(self, cookie):
        req = self.http_lib._get(res.urls['serials'], cookie);
        
        if req['httpcode'] != 200:
            return False;
        if hasattr(req, 'status') and req['status'] != 200:
            return False;
        
        return True;
    
    def _httpLogin(self, usr, pwd):
        print "Login started"

        cookie = self.http_lib._get(res.urls['login'])['cookie']
        postData = { "usr_vplay": usr, "pwd": pwd, "rbm": "1", "login": "Conectare" }
        ret = self.http_lib._post(self.login_url, postData, cookie)
        if ret['httpcode'] != 302:
            raise Exception('Failed to login' + str(ret['httpcode']))

        print "Login ok"
        self.session = cookie
        print cookie
        self.__settings__.setSetting('session', str(self.session))
        
        return True
