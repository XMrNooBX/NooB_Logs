import requests as r
import re
from kwik_token import get_dl_link
from pySmartDL import SmartDL as dl
def get_ep(episode,id):
    page = 0
    if episode%30 == 0:
        page = int(episode/30)
    else:
        page = int(episode/30)+1
    url_ep = f'https://animepahe.ru/api?m=release&id={id}&sort=episode_asc&page={page}'
    response = r.get(url_ep).json()['data']
    return response

def get_stream(url):
    response = r.get(url).text
    dl_lnk = re.findall(r'(https://kwik\.cx/[^"]*)',response)[0]
    return dl_lnk

name = input('Enter anime name : ')
query = name .replace(' ', '%20')
path = r"C:\Users\Ashir\Videos\Captures"

url_n = f'https://animepahe.ru/api?m=search&q={query}'
response = r.get(url_n).json()
results = []
ids = []
status = []
length = []
score = []
for i in response['data']:
    results.append(i['title'])
    ids.append(i['session'])
    status.append(i['status'])
    length.append(i['episodes'])
    score.append(i['score'])
print('Available results are : ')
for i in range(len(results)):
    print(f'{i+1}. {results[i]} :- Episodes : {length[i]}; Status : {status[i]}; Rating : {score[i]}')
n = int(input('\nSelect your choice : ')) - 1
anime_id = ids[n]
desc_url = f'https://animepahe.ru/anime/{ids[n]}'
desc_resp = r.get(desc_url).text
desc_temp = re.findall(r'anime-synopsis">(.*)<', desc_resp)[0].replace('<br>', '')
print(f'Synopsis of {results[n]} : {desc_temp}')
s_m = '\nEnter all the episodes to download(seperated by single space) : '
ep = input(s_m).split(' ')
eps = {}
dl_eps = {}
for j in ep:
    episode = int(j)
    response_2 = get_ep(episode, anime_id)
    for i in response_2:
        if i['episode'] == episode:
            eps.update({int(f'{i["episode"]}'):f'{i["session"]}'})

    url_2 = f'https://animepahe.ru/play/{anime_id}/{eps[episode]}'
    dwn_resp = r.get(url_2).text
    raw_res = re.findall(r'aria-labelledby="downloadMenu">\n<a(.*)', dwn_resp)[0]
    links = re.findall(r'href="(?:([^\"]+)" target="_blank" class="dropdown-item">(?:[^\&]+)&middot; ([^\<]+))(?:<span class="badge badge-primary">(?:[^\&]+)</span> <span class="badge badge-warning text-capitalize">([^\<]+))?',raw_res)

    dl_opts = {}
    for i in links:
        if i[2] == '':
            dl_opts.update({f'{i[1]}Sub' : i[0]})
        else:
            dl_opts.update({f'{i[1]}Dub(Eng)' : i[0]})
    dl_eps.update({episode : dl_opts})

for i in dl_eps.keys():
    print(f'\nAvailable options for Ep {i} are : ')
    d = dl_eps[i]
    l = []
    for dw_q in d.keys():
        l.append(dw_q)
    for num in range(len(l)):
        print(f'{num+1}. {l[num]}')
    q = int(input('Choose download options : '))-1
    kwik_link = get_stream(d[l[q]])
    dl_link = get_dl_link(kwik_link)
    obj=dl(dl_link,path)
    obj.start()