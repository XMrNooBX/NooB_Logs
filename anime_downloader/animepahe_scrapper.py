import requests as r
import re
from colorama import Fore
import asyncio
import aiohttp
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

async def send_web_request(url):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url) as response:
                response.raise_for_status()
                return await response.text()
        except aiohttp.ClientError as e:
            print(f"Request error: {e}")
            return None

async def send_multiple_web_requests(urls):
    tasks = []
    for url in urls:
        tasks.append(send_web_request(url))

    responses = await asyncio.gather(*tasks)
    return responses

async def main(id:str, last:int):
    pages = [i for i in range(1,last+1)]
    urls = [f'https://animepahe.ru/api?m=release&id={id}&sort=episode_asc&page={i}' for i in pages]
    responses = await send_multiple_web_requests(urls)
    eps = {}
    for i in responses:
        ans = re.findall(r'id.*?\"episode\":(.*?),.*?\"session\":\"(.*?)\"',i)
        for j in ans:
            eps.update({int(j[0]) : j[1]})
    l = [i for i in eps.keys()]
    print ('\nAvailable Episodes are : ',Fore.LIGHTMAGENTA_EX,f'{l[0]} - {l[-1]}', Fore.RESET)
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

def download_vid(url:str, title:str, ep):
    if ep < 10:
        ep = f"0{ep}"
    a=title.replace(':','')
    b=a.replace('*','')
    c=b.replace('?','')
    d=c.replace('<','')
    e=d.replace('>','')
    title=e.replace('|','')
    if os.path.isdir(f'{title}') == False:
        os.mkdir(title)
    url = url
    response = r.get(url, stream=True)
    total_size_in_bytes= int(response.headers.get('content-length', 0))
    block_size = 1024
    progress_bar = tqdm(total=total_size_in_bytes, unit='B', unit_scale=True)
    with open(f'{title}\\{title} ep_{ep}.mp4', 'wb') as file:
        for data in response.iter_content(block_size):
            progress_bar.update(len(data))
            file.write(data)
    progress_bar.close()
    if total_size_in_bytes != 0 and progress_bar.n != total_size_in_bytes:
        print("ERROR, something went wrong")
