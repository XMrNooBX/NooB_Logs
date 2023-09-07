import animepahe_scrapper as scrapper
from colorama import Fore
from kwik_token import get_dl_link
import requests as r
import asyncio

''' Bulk or indivisual anime downloader from Animepahe By Ashi and SeD''' 

name = input('Enter anime name : ')
query = name.replace(' ', '%20')
results = scrapper.get_query(query)
ids = scrapper.show_results_get_id(results)
n = int(input('\nPick your poison : ')) - 1
anime_id = ids[n]
last = r.get(f'https://animepahe.ru/api?m=release&id={anime_id}&sort=episode_asc&page=1').json()["last_page"]
title = [i for i in results.keys()][n]
print(Fore.GREEN+'\nPlease wait while we are getting downloads ready....',Fore.RESET)

eps = asyncio.run(scrapper.main(anime_id, last))
raw_in = input("Enter all the episodes to download(seperated by single space or by '-' to give range) : ").split(' ')
ep_in = []
for i in raw_in:
    if '-' in i:
        num = i.split('-')
        for j in range(int(num[0]), int(num[-1])+1):
            ep_in.append(j)
    else:
        ep_in.append(int(i))

dl_links = {}
for i in ep_in:
    session = eps[i]
    ep_links = scrapper.get_ep_link(anime_id, session)
    print(Fore.LIGHTGREEN_EX + f"\nAvailable download options for Ep - {i}")
    links = scrapper.show_dlopts_get_link(ep_links)
    c = int(input(f'Choose download option : ')) - 1
    stream = scrapper.get_stream(links[c])
    dl_links.update({i : get_dl_link(stream)})

for i in dl_links.keys():
    print (f'Downloading Ep-{i}...')
    scrapper.download_vid(dl_links[i], title, i)
