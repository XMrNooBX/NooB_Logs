import requests as r
import re
from colorama import Fore
import os 
def get_query(query:str):
    url = f'https://animepahe.ru/api?m=search&q={query}'
    response = r.get(url).json()
    results = {}
    for i in response['data']:
        l = []
        l.append(i['status'])
        l.append(i['episodes'])
        l.append(i['score'])
        l.append(i['session'])
        results.update({i['title'] : l})
    return results

def show_results_get_id(results:dict):
    print('Available results are : ')
    n = 1
    ids = []
    for i in results.keys():
        if results[i][0] == 'Currently Airing':
            print(Fore.MAGENTA + f'{n}.',Fore.CYAN + f'{i}',Fore.WHITE +' :- Status ->',Fore.RED + f'{results[i][0]}',Fore.WHITE +'; Rating ->',Fore.LIGHTRED_EX+ f'{results[i][2]}',Fore.RESET)
            n=n+1
            ids.append(results[i][3])
        else:
            print(Fore.MAGENTA + f'{n}.',Fore.CYAN + f'{i}',Fore.WHITE +' :- Status ->',Fore.GREEN + f'{results[i][0]}',Fore.WHITE +'Episodes ->',Fore.LIGHTYELLOW_EX +f'{results[i][1]}',Fore.WHITE +'; Rating ->',Fore.LIGHTRED_EX + f'{results[i][2]}',Fore.RESET)
            n = n+1
            ids.append(results[i][3])
    return ids

def show_synopsis(anime_id:str):
    url = f'https://animepahe.ru/anime/{anime_id}'
    response = r.get(url).text
    synopsis = re.findall(r'anime-synopsis">(.*)<', response)[0].replace('<br>', '')
    print(Fore.CYAN + f'{synopsis}')

def get_ep_id(anime_id:str, episode:int):
    page = 0
    if episode%30 == 0:
        page = int(episode/30)
    else:
        page = int(episode/30)+1
    url = f'https://animepahe.ru/api?m=release&id={anime_id}&sort=episode_asc&page={page}'
    response = r.get(url).json()['data']
    for i in response:
        if i['episode'] == episode:
            return i['session']

def get_ep_link(anime_id:str, ep_id:str):
    url = f'https://animepahe.ru/play/{anime_id}/{ep_id}'
    response = r.get(url).text
    raw_res = re.findall(r'aria-labelledby="downloadMenu">\n<a(.*)', response)[0]
    links = re.findall(r'href="(?:([^\"]+)" target="_blank" class="dropdown-item">(?:[^\&]+)&middot; ([^\<]+))(?:<span class="badge badge-primary">(?:[^\&]+)</span> <span class="badge badge-warning text-capitalize">([^\<]+))?',raw_res)
    return links

def show_dlopts_get_link(links:list):
    n = 1
    link = []
    for i in links:
        if i[2] == '':
            print(Fore.MAGENTA+f'{n}.', Fore.LIGHTBLUE_EX + f'{i[1]} Sub', Fore.RESET)
            n=n+1
            link.append(i[0])
        else:
            print(Fore.MAGENTA+f'{n}.', Fore.LIGHTGREEN_EX+ f'{i[1]} Dub',Fore.RESET)
            n=n+1
            link.append(i[0])  
    return link

def get_stream(url:str):
    response = r.get(url).text
    stream_lnk = re.findall(r'(https://kwik\.cx/[^"]*)',response)[0]
    return stream_lnk

def newest(path):
    '''Function to get latest file in given directory'''
    files = os.listdir(path)
    paths = [os.path.join(path, basename) for basename in files]
    return max(paths, key=os.path.getctime)