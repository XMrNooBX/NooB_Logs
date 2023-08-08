import animepahe_scrapper as scrapper
from colorama import Fore
from kwik_token import get_dl_link
from pySmartDL import SmartDL as dl
import os

''' Bulk or indivisual anime downloader from Animepahe By Ashi and SeD'''
#yeaaaaaahhhhhhh SeD 

name = input('Enter anime name : ')
path = r"C:\Users\Ashir\Videos\Captures"
query = name.replace(' ', '%20')
results = scrapper.get_query(query)
ids = scrapper.show_results_get_id(results)
n = int(input('\nPick your poison : ')) - 1
anime_id = ids[n]
title = [i for i in results.keys()][n]
print(Fore.LIGHTYELLOW_EX+'Would you like to see synopsis of chosen Anime?',Fore.LIGHTGREEN_EX+'Y',Fore.WHITE+'/',Fore.LIGHTRED_EX+'N',Fore.WHITE+' : ',Fore.RESET, end='')
a = input()
if a.lower() == 'y':
    scrapper.show_synopsis(anime_id)
else:
    print("Ok Then let's proceed to downloading.")

eps = input('\nEnter all the episodes to download(seperated by single space) : ').split(' ')

for i in eps:
    ep = int(i)
    ep_id = scrapper.get_ep_id(anime_id, ep)
    ep_links = scrapper.get_ep_link(anime_id, ep_id)
    links = scrapper.show_dlopts_get_link(ep_links)
    c = int(input('choose download option : ')) - 1
    stream = scrapper.get_stream(links[c])
    dl_link = get_dl_link(stream)
    obj=dl(dl_link,path)
    obj.start()
    rename = scrapper.newest(path)               # Find latest file in given path and properly rename it
    os.rename(rename,f'{path}//{title}.mp4')