requirements = []
try:
    from bs4 import BeautifulSoup
except:
    requirements.append("bs4")
try:
    import requests
except:
    requirements.append("requests")
try:
    import eyed3
except:
    requirements.append("eyed3")
import time
try:
    from eyed3.id3.frames import ImageFrame
except:
    pass
import os
try:
    from pytube import YouTube
except:
    requirements.append("pytube")
try:
    from moviepy.editor import AudioFileClip
except:
    requirements.append("moviepy")
try:
    import music_tag
except:
    requirements.append("music_tag")

if requirements != []:
    print(f"You need to install the following packages with pip:", *requirements)
    print("\ntab will close in 10s")
    time.sleep(10)
    exit()

songs = []
cover = False

try:
    open(f"{os.path.dirname(os.path.abspath(__file__))}\\cover.jpg","x")
    print("DO NOT CLOSE THIS TAB DURING SETUP!! *VERY IMPORTANT*")
    if "y" in input("Do you want song covers added to the files (has lots more extra steps probably not worth it)? (y/n) >> ").lower():
        open(f"{os.path.dirname(os.path.abspath(__file__))}\\DO NOT DELETE.txt","a").write(f'y\n{input("Enter Google API key: ")}\n{input("Enter Google Programable Search Engine ID: ")}')
    else:
        open(f"{os.path.dirname(os.path.abspath(__file__))}\\DO NOT DELETE.txt","a").write('n')
    os.mkdir(f"{os.path.dirname(os.path.abspath(__file__))}\\songs")
    print("Setup complete.\n\n--------------------------------------------\n")
except:
    pass

if open(f"{os.path.dirname(os.path.abspath(__file__))}\\DO NOT DELETE.txt","r").read()[0] == "y":
    cover = True
    key = open(f"{os.path.dirname(os.path.abspath(__file__))}\\DO NOT DELETE.txt","r").readlines()[1].replace("\n","")
    engine = open(f"{os.path.dirname(os.path.abspath(__file__))}\\DO NOT DELETE.txt","r").readlines()[2].replace("\n","")


print("Enter song (e.g. Radioactive, Imagine Dragons) *Leave empty if you've listed all the songs you want.*")
while True:
    try:
        name,artist = input(" - ").split(", ")
    except Exception as e:
        print("Starting to download...")
        break
    songs.append([name,artist])


for song in songs:
    try:
        search = f'{song[0]} by {song[1]} youtube.com lyrics video'
        url = 'https://www.google.com/search'

        headers = {
            'Accept' : '*/*',
            'Accept-Language': 'en-US,en;q=0.5',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82',
        }
        parameters = {'q': search}

        content = requests.get(url, headers = headers, params = parameters).text
        soup = BeautifulSoup(content, 'html.parser')

        search = soup.find(id = 'search')
        first_link = search.find('a')
        video_url = first_link['href']
        video = YouTube(video_url, use_oauth=True, allow_oauth_cache=True)
        ys = video.streams.get_highest_resolution()
        t = video.streams.filter(only_audio=True).all()
        out_file = t[0].download(f"{os.path.dirname(os.path.abspath(__file__))}\\songs",filename="song.mp4")


        def MP4ToMP3(mp4, mp3):
            FILETOCONVERT = AudioFileClip(mp4)
            FILETOCONVERT.write_audiofile(mp3)
            FILETOCONVERT.close()
        VIDEO_FILE_PATH = f"{out_file}"
        AUDIO_FILE_PATH = f"{out_file.replace('mp4','mp3')}"

        MP4ToMP3(VIDEO_FILE_PATH, AUDIO_FILE_PATH)

        os.remove(f"{out_file}")


        query = f"{song[0]} by {song[1]} album cover spotify"


        def search_images(query):
            url = 'https://www.googleapis.com/customsearch/v1'
            params = {
                'key': key,
                'cx': engine,
                'q': query,
                'searchType': 'image'
            }

            response = requests.get(url, params=params)
            data = response.json()
            if 'items' in data:
                for item in data['items']:
                    return item['link']
                    break
            else:
                print(data)
                print('No images found for this song.')
                return "https://cdn.shopify.com/s/files/1/0432/9868/5091/products/MrNoodles_Chicken_Pollo_Kimchi_86g_XX_1024x1024.jpg?v=1632607484"
        if cover:
            img_data = requests.get(search_images(query)).content
            with open(f"{os.path.dirname(os.path.abspath(__file__))}\\cover.jpg", 'wb') as handler:
                handler.write(img_data)

            
            audiofile = eyed3.load(f"{os.path.dirname(os.path.abspath(__file__))}\\songs\\song.mp3")
            if (audiofile.tag == None):
                audiofile.initTag()

            audiofile.tag.images.set(ImageFrame.FRONT_COVER, open(f"{os.path.dirname(os.path.abspath(__file__))}\\cover.jpg",'rb').read(), 'image/jpeg')
            audiofile.tag.save()

        f = music_tag.load_file(f"{os.path.dirname(os.path.abspath(__file__))}\\songs\\song.mp3")
        f['title'] = song[0].title()
        f["artist"] = song[1].title()
        f["album"] = song[0].title()
        f.save()
        try:
            os.rename(f"{os.path.dirname(os.path.abspath(__file__))}\\songs\\song.mp3",f"{os.path.dirname(os.path.abspath(__file__))}\\songs\\{song[0].title()}.mp3")
            print(f"                        *Downloaded {song[0].title()}*")
        except:
            try:
                os.rename(f"{os.path.dirname(os.path.abspath(__file__))}\\songs\\song.mp3",f"{os.path.dirname(os.path.abspath(__file__))}\\songs\\{song[0].title()} by {song[1].title()}.mp3")
                print(f"Already a song called that so had to rename it to {song[0].title()} by {song[1].title()}")
                print(f"                        *Downloaded {song[0].title()}*")
            except:
                print(f"                        *DUPLICATE SONG FOUND CAN'T DOWNLOAD {song[0].title()}*")
    except Exception as error:
        print(f"{error} *WITH {song[0].upper()}*")
print("DONE")
print("tab will close in 10s")
time.sleep(10)
