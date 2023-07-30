from pySmartDL import SmartDL as dl
import requests
import os
import urllib.parse
def newest(path):
    '''Function to get latest file in given directory'''
    files = os.listdir(path)
    paths = [os.path.join(path, basename) for basename in files]
    return max(paths, key=os.path.getctime)

def song_data(name:str):
    '''Function to get info of given song from jiosavaan'''
    url="https://www.jiosaavn.com/api.php?__call=autocomplete.get&query="+name+"&_format=json&_marker=0&ctx=wap6dot0"
    info=requests.get(url)
    info=info.json()["songs"]["data"]
    return info

song = input('Enter song name : ')   # get song name from user and store useful info in some lists
a = song_data(song)
titles = []
description = []
urls = []
for i in a:
    titles.append(i['title'])
    urls.append(i['url'])
    description.append(i['description'])

print('Available results are : ')    # Show the available results to user and ask for user's choice
for i in range(len(titles)):
    print(f'{i+1}. {titles[i]} : {description[i]}')
n = int(input('\nEnter index of song to download : '))

song_url = urls[n-1]                 # Extract song id from link we got from user's choice
path = r'C:\Users\Ashir\Music'
song_id = song_url.split('/')[-1]    
title = song_url.split('/')[-2]

# Get direct download link of song from savaan server
url = f'https://www.jiosaavn.com/api.php?__call=webapi.get&api_version=4&_format=json&_marker=0&ctx=wap6dot0&token={song_id}&type=song'
r = requests.get(url)
response = r.json()
final_url = urllib.parse.quote(response['songs'][0]['more_info']['encrypted_media_url'])
dwn_url = f'https://www.jiosaavn.com/api.php?__call=song.generateAuthToken&url={final_url}&bitrate=320&api_version=4&_format=json&ctx=wap6dot0&_marker=0'
dwn_r = requests.get(dwn_url)
lnk = dwn_r.json()

obj=dl(lnk['auth_url'],path)        # Proceed to download song at given path
obj.start()

rename = newest(path)               # Find latest file in given path and properly rename it
os.rename(rename,f'{path}//{title}.m4a')