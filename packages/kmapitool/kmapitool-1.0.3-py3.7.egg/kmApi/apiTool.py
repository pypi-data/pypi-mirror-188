#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests
import hashlib
form_header = {
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
}


class openApi():

    @staticmethod
    def getAuth(self, host, userName, passWord):
        pwd = hashlib.md5(passWord.encode())
        req_data = {
            "account": userName,
            "passwd": pwd.hexdigest()
        }
        host = host + "/annotationPermit/permit/login"
        try:
            response = requests.post(url=host, data=req_data, headers=form_header)
            res = response.json()
            return res['result']['token']
        except Exception as e:
            print(str(e))
            return None
#
# if __name__ =='__main__':
