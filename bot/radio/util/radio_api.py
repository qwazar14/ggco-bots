import json

import requests


async def get_current_song():
    url = "https://air.radioulitka.ru:8083/api/live-info/"
    # url = "https://ghostbin.com/V6FSn/raw"
    r = requests.get(url)
    string = r.text
    json_string = json.dumps(string, ensure_ascii=False)
    # regexed_json = re.sub(r"^\S+\bulitka_playlist_callback.",'', aa)
    regexed_json = str(json_string[26:])
    sliced_json = str(regexed_json[:-2])

    final_json = sliced_json.replace('\\', '')
    print(final_json)

    data = json.loads(final_json)

    current_song = data["current"]["name"]

    print(current_song)
    print(f'[INFO] current_song: {current_song}')
    return current_song
