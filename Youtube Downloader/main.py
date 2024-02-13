#In order to use pytube open a command prompt as administrator and run : python -m pip install git+https://github.com/pytube/pytube
from pytube import YouTube
import sys
import shutil

print(r"""
                      __        __                __                    __                __         
   __  ______  __  __/ /___  __/ /_  ___     ____/ /___ _      ______  / /___  ____ _____/ /__  _____
  / / / / __ \/ / / / __/ / / / __ \/ _ \   / __  / __ \ | /| / / __ \/ / __ \/ __ `/ __  / _ \/ ___/
 / /_/ / /_/ / /_/ / /_/ /_/ / /_/ /  __/  / /_/ / /_/ / |/ |/ / / / / / /_/ / /_/ / /_/ /  __/ /    
 \__, /\____/\__,_/\__/\__,_/_.___/\___/   \__,_/\____/|__/|__/_/ /_/_/\____/\__,_/\__,_/\___/_/     
/____/                                                                                               
""")

list = []

#Editer le chemin source
chemin = "C:/Users/user/PycharmProjects/test2/"

def definir_progression(stream, chunk, bytes_remaining):
    bytes_downloaded = stream.filesize - bytes_remaining
    percent = bytes_downloaded * 100 / stream.filesize
    sys.stdout.write("\r" + f"Progression du téléchargement: {int(percent)}%")
    sys.stdout.flush()

def trouver_itag(p_stream):
    itag_index = p_stream.find('itag="') + len('itag="')
    itag_end_index = p_stream.find('"', itag_index)
    itag_value = p_stream[itag_index:itag_end_index]
    return itag_value

def trouver_extension(p_stream):
    extension_start_index = p_stream.find('mime_type="') + len('mime_type="')
    extension_end_index = p_stream.find('"', extension_start_index)
    extension_value = p_stream[extension_start_index:extension_end_index]
    return extension_value.split("/")[-1]

def valider_choix(p_choix, p_list):
    for itag, ext in p_list:
        if p_choix == itag:
            return True
    return False

def trouver_extension_par_itag(p_choix, p_list):
    for itag, ext in p_list:
        if p_choix == itag:
            return ext
    return None

def poser_question(p_question):
    reponse = ""
    while reponse == "":
        reponse = input(p_question)
    return reponse

def convertir_secondes_en_duree(secondes):
    heures = secondes // 3600
    minutes = (secondes % 3600) // 60
    secondes_restantes = secondes % 60
    return f"{heures:02d}:{minutes:02d}:{secondes_restantes:02d}"

url = poser_question("Entrer l'URL de la video: ")
youtube_video = YouTube(url)
youtube_video.register_on_progress_callback(definir_progression)

duree = convertir_secondes_en_duree(youtube_video.length)
print(f"TITRE: {youtube_video.title}")
print(f"Auteur: {youtube_video.author} | Nb de vues: {youtube_video.views} | Duree: {duree}")
print("")
print("STREAMS:")
for stream in youtube_video.streams.fmt_streams:
    print(stream)
    itag = trouver_itag(str(stream))
    extension = trouver_extension(str(stream))
    list.append((itag,extension))

print("")

while True:
    choix = poser_question("Choisir le itag : ")
    validation = valider_choix(choix, list)

    if validation:
        ext = trouver_extension_par_itag(choix, list)
        stream = youtube_video.streams.get_by_itag(choix)
        print("Téléchargement en cours...")
        stream.download()
        print("\nOK")
        break
    else:
        print("Erreur: itag invalide.")

#Transfert du fichier vers le dossier telechargements
source = f'{chemin}{youtube_video.title}.{ext}'
destination = f'C:/Users/user/Downloads/{youtube_video.title}.{ext}'
shutil.move(source, destination)