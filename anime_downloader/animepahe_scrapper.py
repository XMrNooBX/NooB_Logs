import grequests as g
import requests as r
import re
from colorama import Fore
from tqdm import tqdm
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
    print(Fore.CYAN + f'{synopsis}',Fore.RESET)

def get_ep_id(id:str):
    link = f'https://animepahe.ru/api?m=release&id={id}&sort=episode_asc&page=1'
    response = r.get(link).json()['last_page']
    pages = [i for i in range(1,response+1)]
    urls = [f'https://animepahe.ru/api?m=release&id={id}&sort=episode_asc&page={i}' for i in pages]
    gresp = [g.get(url) for url in urls]
    data = [g.map(gresp)[i].json()['data'] for i in range(len(gresp))]
    eps = {}
    for i in data:
        for j in i:
            eps.update({j['episode'] : j['session']})
    return eps

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

def download_vid(url:str, title:str, ep:int):
    if os.path.isdir(f'{title}') == False:
        os.mkdir(title)
    url = url
    response = r.get(url, stream=True)
    total_size_in_bytes= int(response.headers.get('content-length', 0))
    block_size = 1024
    progress_bar = tqdm(total=total_size_in_bytes, unit='B', unit_scale=True)
    with open(f'{title}\\ep_{ep}.mp4', 'wb') as file:
        for data in response.iter_content(block_size):
            progress_bar.update(len(data))
            file.write(data)
    progress_bar.close()
    if total_size_in_bytes != 0 and progress_bar.n != total_size_in_bytes:
        print("ERROR, something went wrong")
