from __future__ import print_function
import pickle
import os.path
from os import listdir
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from apiclient.http import MediaFileUpload
from datetime import datetime
import time
from config import BASE_DIR, MODULE_DIR
import logging

class drive:
    def __init__(self):
        logging.getLogger('googleapiclient.discovery_cache').setLevel(logging.ERROR)
        
        SCOPES = ['https://www.googleapis.com/auth/drive']

        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('auth/token.pickle'):
            with open('auth/token.pickle', 'rb') as token:
                creds = pickle.load(token)
                print('已經取得creds認證')
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                print('未取得權限, 請登入google drive')
                try:
                    flow = InstalledAppFlow.from_client_secrets_file('auth/credentials.json', SCOPES)
                    creds = flow.run_local_server()
                except:
                    print('找不到 credentials.json 此檔案')
            
            # Save the credentials for the next run
            with open('auth/token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        self.service = build('drive', 'v3', credentials=creds)

    def backup(self):
        ### 備份 cgu_db ###
        # create folder
        nowTime = datetime.now().strftime("%Y-%m-%d") # 今天日期
        # nowTime = '2019-06-09'

        BACKUP_FOLDER_ID = '1o350E0O7ZQJyXmcgWggWVoPJWlZVg3lg' # 認知訓練之臨床應用>backup
        folder_metadata = {
            'name': nowTime,
            'mimeType': 'application/vnd.google-apps.folder',
            'parents': [BACKUP_FOLDER_ID]
        }
        folder = self.service.files().create(body=folder_metadata,
                                             fields='id').execute()
        print(time.strftime("%A, %d. %B %Y %I:%M:%S %p"), '成功在google drive創建資料夾')
        FOLDER_ID = folder.get('id') # 當下創建的folder id

        # 本地backup資料夾內的檔案
        local_backup_path = os.path.join(BASE_DIR, "backup", nowTime)
        files = listdir(local_backup_path)
        for f in files:
            fullpath = os.path.join(local_backup_path, f)

            # 檢查文件大小，除果0kb就不上傳
            fileSize = os.path.getsize(fullpath)
            if (fileSize>0):
                file_metadata = {
                    'name' : f,
                    'parents': [FOLDER_ID]
                }
                media = MediaFileUpload(fullpath,
                                        resumable=True)
                file = self.service.files().create(body=file_metadata,
                                                media_body=media,
                                                fields='id').execute()
                print('成功上傳', f, '到雲端')


        ### 備份 logs ###
        log_path = os.path.join(BASE_DIR, "logs")
        log_files = listdir(log_path)
        for f in log_files:
            fullpath = os.path.join(log_path, f)

            # 檢查文件大小，除果0kb就不上傳
            fileSize = os.path.getsize(fullpath)
            if (fileSize>0):
                file_metadata = {
                    'name' : f,
                    'parents': [FOLDER_ID]
                }
                media = MediaFileUpload(fullpath,
                                        resumable=True)
                file = self.service.files().create(body=file_metadata,
                                                media_body=media,
                                                fields='id').execute()
                print('成功上傳', f, '到雲端')
