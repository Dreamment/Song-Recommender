import numpy as np
from scipy.stats import pearsonr
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotipy.oauth2 import SpotifyClientCredentials
import os
import api_informations

priorities = []
datas = [[] for _ in range(19)]


def get_data():
    global datas
    datas.clear()
    datas = [[] for _ in range(19)]
    current_dir = os.path.dirname(__file__)
    icon_path = os.path.join(current_dir, "data.csv")
    with open(icon_path, "r", encoding="ISO-8859-1") as f:
        for index1, line in enumerate(f):
            if index1 == 0:
                continue
            line = line.replace("\n", "")
            for index2, data in enumerate(line.split(";")):
                try:
                    data = float(data)
                except ValueError:
                    pass
                datas[index2].append(data)


def get_correlation_coefficients():
    subjects = {
        "valence": 0,
        "year": 1,
        "acousticness": 2,
        "danceability": 4,
        "energy": 6,
        "explicit": 7,
        "instrumentalness": 9,
        "key": 10,
        "liveness": 11,
        "loudness": 12,
        "mode": 13,
        "popularity": 15,
        "speechiness": 17,
        "tempo": 18,
    }

    subject_name = "popularity"
    change_subject = datas[subjects[subject_name]]

    corr_valence, _ = pearsonr(change_subject, datas[0])
    corr_year, _ = pearsonr(change_subject, datas[1])
    corr_acousticness, _ = pearsonr(change_subject, datas[2])
    corr_danceability, _ = pearsonr(change_subject, datas[4])
    corr_energy, _ = pearsonr(change_subject, datas[6])
    corr_explicit, _ = pearsonr(change_subject, datas[7])
    corr_instrumentalness, _ = pearsonr(change_subject, datas[9])
    corr_key, _ = pearsonr(change_subject, datas[10])
    corr_liveness, _ = pearsonr(change_subject, datas[11])
    corr_loudness, _ = pearsonr(change_subject, datas[12])
    corr_mode, _ = pearsonr(change_subject, datas[13])
    corr_popularity, _ = pearsonr(change_subject, datas[15])
    corr_speechiness, _ = pearsonr(change_subject, datas[17])
    corr_tempo, _ = pearsonr(change_subject, datas[18])

    values = np.array([corr_valence, corr_year, corr_acousticness, corr_danceability,
                       corr_energy, corr_explicit, corr_instrumentalness, corr_key,
                       corr_liveness, corr_loudness, corr_mode, corr_popularity,
                       corr_speechiness, corr_tempo])
    return values


def get_history():
    client_id = api_informations.id
    client_secret = api_informations.secret
    client_credentials_manager = SpotifyClientCredentials(client_id, client_secret)

    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=f"{client_id}",
                                                   client_secret=f"{client_secret}",
                                                   redirect_uri="http://localhost:8000/callback",
                                                   scope="user-read-recently-played"))

    sp2 = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    results = sp.current_user_recently_played(limit=10)

    links = []
    for item in results['items']:
        link = {'url': item['track']['external_urls']['spotify']}
        links.append(link)

    song_infos = []
    for i, item in enumerate(links):
        track_info = sp2.track(item['url'])
        audio_features = sp2.audio_features([track_info['id']][0])
        audio_features[0]['popularity'] = track_info['popularity']
        audio_features[0]['name'] = track_info['name']
        audio_features[0]['year'] = int(track_info['album']['release_date'][:4])
        if track_info['explicit']:
            audio_features[0]['explicit'] = 1
        else:
            audio_features[0]['explicit'] = 0

        for j, items in enumerate(results['items'][i]['track']['artists']):
            if j != 0:
                audio_features[0]['artist_name'] += ", " + items['name']
            else:
                audio_features[0]['artist_name'] = items['name']
        song_infos.append(audio_features)
    return song_infos


def calculate_priorities():
    global priorities
    priorities.clear()
    priorities = []
    values = get_correlation_coefficients()
    for column in zip(*datas):
        priority = values[0] * column[0] + \
                   values[1] * column[1] + \
                   values[2] * column[2] + \
                   values[3] * column[4] + \
                   values[4] * column[6] + \
                   values[5] * column[7] + \
                   values[6] * column[9] + \
                   values[7] * column[10] + \
                   values[8] * column[11] + \
                   values[9] * column[12] + \
                   values[10] * column[13] + \
                   values[11] * column[15] + \
                   values[12] * column[17] + \
                   values[13] * column[18]
        priorities.append(priority)


def calculate_average_priority():
    values = get_correlation_coefficients()
    song_infos = get_history()
    average_priority = 0
    for item in song_infos:
        priority = item[0]['valence'] * values[0] + \
                   item[0]['year'] * values[1] + \
                   item[0]['acousticness'] * values[2] + \
                   item[0]['danceability'] * values[3] + \
                   item[0]['energy'] * values[4] + \
                   item[0]['explicit'] * values[5] + \
                   item[0]['instrumentalness'] * values[6] + \
                   item[0]['key'] * values[7] + \
                   item[0]['liveness'] * values[8] + \
                   item[0]['loudness'] * values[9] + \
                   item[0]['mode'] * values[10] + \
                   item[0]['popularity'] * values[11] + \
                   item[0]['speechiness'] * values[12] + \
                   item[0]['tempo'] * values[13]
        average_priority += priority
    average_priority = average_priority / len(song_infos)
    return average_priority


def find_nearest_index(array, value):
    array = np.asarray(array)
    distances = np.abs(array - value)
    sorted_indices = np.argsort(distances)
    return sorted_indices[:5]


def recommend():
    get_data()
    calculate_priorities()
    value = calculate_average_priority()
    song_urls = []
    idx = find_nearest_index(priorities, value)
    for i in range(len(idx)):
        index = idx[i]
        song_url = f'https://open.spotify.com/track/{datas[8][index]}'
        song_urls.append(song_url)
    return song_urls


def get_image_of_songs(urls):
    images = []
    client_id = api_informations.id
    client_secret = api_informations.secret
    client_credentials_manager = SpotifyClientCredentials(client_id, client_secret)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    for url in urls:
        song_id = url.split('/')[4]
        song = sp.track(song_id)
        image = song['album']['images'][0]['url']
        images.append(image)
    return images


def get_name_of_songs(urls):
    names = []
    client_id = api_informations.id
    client_secret = api_informations.secret
    client_credentials_manager = SpotifyClientCredentials(client_id, client_secret)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    for url in urls:
        song_id = url.split('/')[4]
        song = sp.track(song_id)
        name = song['name']
        names.append(name)
    return names


def get_artist_of_songs(urls):
    names = []
    client_id = api_informations.id
    client_secret = api_informations.secret
    client_credentials_manager = SpotifyClientCredentials(client_id, client_secret)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    for url in urls:
        song_id = url.split('/')[4]
        song = sp.track(song_id)
        artists_number = len(song['artists'])
        name = ''
        for i in range(artists_number):
            name += song['artists'][i]['name']
            if i != artists_number - 1:
                name += ' & '
        names.append(name)
    return names


def return_infos():
    urls = recommend()
    images = get_image_of_songs(urls)
    names = get_name_of_songs(urls)
    artists = get_artist_of_songs(urls)

    for i, name in enumerate(names):
        temp = name.title()
        names[i] = temp

    infos = {}
    for i in range(len(urls)):
        info = {"name": names[i], "artists": artists[i], "url": urls[i], "image": images[i] }
        infos[i] = info
    return infos

