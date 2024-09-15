import os
import sys
import spotipy
import spotipy.util as util
from json.decoder import JSONDecodeError
from dotenv import load_dotenv
import pickle

# load the .env file variables
load_dotenv()

# Establecemos las variables de entorno
os.environ['SPOTIPY_CLIENT_ID'] = os.environ.get('CLIENT_ID')
os.environ['SPOTIPY_CLIENT_SECRET'] = os.environ.get('CLIENT_SECRET')
os.environ['SPOTIPY_REDIRECT_URI'] = os.environ.get('REDIRECT_URIS')

# User ID: 0f25087be45a4706
# Get username from terminal
username = sys.argv[1]
scope = 'user-library-read'

# Erase cache and prompt for user permission
try:
  token = util.prompt_for_user_token(username, scope) # add scope
except(AttributeError, JSONDecodeError):
  os.remove(f'.cache-{username}')
  token = util.prompt_for_user_token(username, scope) # add scope

# Create our spotify object with permission
spotifyObject = spotipy.Spotify(auth = token)

# Name of the artist that we want to search
artist_name = 'Queens of the stone age'

# Obtain top 10 songs
result = spotifyObject.search(q = artist_name, limit = 10)

# Inicializamos el diccionario con listas vacías
dict_band = {
  'Band_name': [],
  'Song_name': [],
  'Popularity': [],
  'Duration_min': []
}

# Recorremos los datos y los agregamos al diccionario
for track in result['tracks']['items']:
  # Detalles del artista/banda
  band_name = track['artists'][0]['name']
  song_name = track['name']
  popularity = track['popularity']
  duration_min = round(track['duration_ms'] / 60000, 2)  # Convertir milisegundos a minutos
    
  # Añadimos los detalles al diccionario
  dict_band['Band_name'].append(band_name)
  dict_band['Song_name'].append(song_name)
  dict_band['Popularity'].append(popularity)
  dict_band['Duration_min'].append(duration_min)

with open('banda_diccionario.pkl', 'wb') as f:
  pickle.dump(dict_band, f)

print(dict_band)