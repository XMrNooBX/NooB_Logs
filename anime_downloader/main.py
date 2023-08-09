import animepahe_scrapper as scrapper
from colorama import Fore
from kwik_token import get_dl_link
import os

''' Bulk or indivisual anime downloader from Animepahe By Ashi and SeD''' 

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
print(Fore.GREEN+'\nPlease wait while we are getting downloads ready....',Fore.RESET)
Episodes = scrapper.get_ep_id(anime_id)
print ('\nAvailable Episodes are : ',Fore.LIGHTMAGENTA_EX,[i for i in Episodes.keys()], Fore.RESET)
ep_in = input("Enter all the episodes to download(seperated by single space) or Press 'a' to download All: ").split(' ')
if len(ep_in) == 1 and ep_in[0].lower() == 'a':
    eps = [i for i in Episodes.keys()]
else:
    eps = [int(i) for i in ep_in]
dl_links = {}
for i in eps:
    session = Episodes[i]
    ep_links = scrapper.get_ep_link(anime_id, session)
    print(Fore.LIGHTGREEN_EX + f"\nAvailable download options for Ep - {i}")
    links = scrapper.show_dlopts_get_link(ep_links)
    c = int(input(f'Choose download option : ')) - 1
    stream = scrapper.get_stream(links[c])
    dl_links.update({i : get_dl_link(stream)})

for i in dl_links.keys():
    print (f'Downloading Ep-{i}...')
    scrapper.download_vid(dl_links[i])
    os.rename(f"{os.getcwd()}\\test.mp4",f"{path}\\{title}_ep-{i}.mp4")
