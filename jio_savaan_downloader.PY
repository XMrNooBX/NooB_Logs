import requests as r
import os
import urllib.parse
from tqdm import tqdm
import re
def newest(path):
    '''Function to get latest file in given directory'''
    files = os.listdir(path)
    paths = [os.path.join(path, basename) for basename in files]
    return max(paths, key=os.path.getctime)

def song_data(name:str):
    '''Function to get info of given song from jiosavaan'''
    url="https://www.jiosaavn.com/api.php?__call=autocomplete.get&query="+name+"&_format=json&_marker=0&ctx=wap6dot0"
    info=r.get(url)
    info=info.json()["songs"]["data"]
    return info

def download_song(url:str):
    url = url
    response = r.get(url, stream=True)
    total_size_in_bytes= int(response.headers.get('content-length', 0))
    block_size = 1024
    progress_bar = tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True)
    with open('test.mp3', 'wb') as file:
        for data in response.iter_content(block_size):
            progress_bar.update(len(data))
            file.write(data)
    progress_bar.close()
    if total_size_in_bytes != 0 and progress_bar.n != total_size_in_bytes:
        print("ERROR, something went wrong")

song = input('Enter song name : ')   # Get song name from user and store useful info in some lists
path = r'C:\Users\Ashir\Music'
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
n = (input('\nEnter index of song to download(press "y" To get youtube results) : '))

if n!='y':
    n = int(n)
    song_url = urls[n-1]                 # Extract song id from link we got from user's choice
    song_id = song_url.split('/')[-1]    
    title = song_url.split('/')[-2]

    # Get direct download link of song from savaan server
    url = f'https://www.jiosaavn.com/api.php?__call=webapi.get&api_version=4&_format=json&_marker=0&ctx=wap6dot0&token={song_id}&type=song'
    resp = r.get(url)
    response = resp.json()
    final_url = urllib.parse.quote(response['songs'][0]['more_info']['encrypted_media_url'])
    dwn_url = f'https://www.jiosaavn.com/api.php?__call=song.generateAuthToken&url={final_url}&bitrate=320&api_version=4&_format=json&ctx=wap6dot0&_marker=0'
    dwn_r = r.get(dwn_url)
    dl_lnk = re.findall(r"(.+?(?=Expires))",dwn_r.json()['auth_url'])[0].replace('.cf.','.').replace('?','').replace('ac','aac')
    download_song(dl_lnk)
    os.rename(f"{os.getcwd()}\\test.mp3",f"{path}\\{title}.mp3")

elif n=='y':
    import re
    from pytube import YouTube as yt
    def progress_function(chunk, file_handle, bytes_remaining):
        file_size = chc.filesize
        current = ((file_size - bytes_remaining)/file_size)
        percent = ('{0:.1f}').format(current*100)
        progress = int(50*current)
        status = '█' * progress + '-' * (50 - progress)
        print('\r'+' ↳ |{bar}| {percent}%  ({x}Mb)'.format(bar=status, percent=percent, x=round((file_size)/(1024*1024),2)),end='')

    query = song.replace(' ','+')
    url = f'https://www.youtube.com/results?search_query={query}'
    response = r.get(url).text
    resp = re.findall(r'videoId\":\"(.*?)\"',response)
    v_ids = [resp[0]]
    for i in resp:
        if i not in v_ids:
            v_ids.append(i)
    result = [v_ids[j] for j in range(5)]
    names = []
    ur = []
    for i in result:
        lnk = f'https://www.youtube.com/watch?v={i}'
        if yt(lnk).length > 60:
            names.append(yt(lnk).title)
            ur.append(lnk)
    for i in range(len(names)):
       print(f'{i+1}. {names[i]}')
    c = int(input('Select your choice : '))-1
    chc = yt(ur[c], on_progress_callback=progress_function).streams.filter(only_audio=True)[-1]
    chc.download()
    fil = newest(os.getcwd())
    name=names[c].replace('|',' ').replace(':', " ")
    os.rename(fil,f"{path}\\{name}.mp3")
