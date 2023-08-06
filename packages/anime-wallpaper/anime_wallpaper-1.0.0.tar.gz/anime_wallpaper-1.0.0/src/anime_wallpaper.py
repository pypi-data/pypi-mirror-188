import requests, random

def wallpaper():
    list = str(requests.get("https://gist.githubusercontent.com/Nowkzy/3b950f0dbad92d81edb449a7c6e0109c/raw").text)
    source_api = list.split()
    return random.choice(source_api)

def imageWebhook(Webhook):
    list = str(requests.get("https://gist.githubusercontent.com/Nowkzy/3b950f0dbad92d81edb449a7c6e0109c/raw/").text)
    source_api = list.split()
    img = random.choice(source_api)
    data = {
    "content" : f"{img}",
    "avatar_url": "https://media.cdnws.com/_i/136023/p%7B1000%7D-49506/3283/6/10-choses-savoir-monkey-luffy-blog-one-piece-10.jpeg",
    "username" : "Anime Wallpaper",
}
    result = requests.post(url=Webhook, json = data)
    print(result)