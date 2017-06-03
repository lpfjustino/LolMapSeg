import requests
import shutil

def fetch_images(champion_names):
    for champion_name in champion_names:
        url = "http://ddragon.leagueoflegends.com/cdn/7.11.1/img/champion/"+champion_name+".png"
        response = requests.get(url, stream=True)
        with open(champion_name+'.png', 'wb') as out_file:
            shutil.copyfileobj(response.raw, out_file)


def fetch_champions():
    url = "https://br1.api.riotgames.com/lol/static-data/v3/champions?api_key=RGAPI-b3a0e588-5085-43cc-8778-bb2394a4541d"
    headers = {
        "Origin": "https://developer.riotgames.com",
        "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
        "X-Riot-Token": "RGAPI-b3a0e588-5085-43cc-8778-bb2394a4541d",
        "Accept-Language": "pt-BR,pt;q=0.8,en-US;q=0.6,en;q=0.4",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
    }

    r = requests.get(url, headers=headers)
    champs = dict(r.json()['data'])
    champ_names = []
    for champ in champs:
        champ_names.append(champs[champ]['key'])

    return champ_names

