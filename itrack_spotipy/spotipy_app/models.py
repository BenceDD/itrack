from django.db import models

from SPARQLWrapper import SPARQLWrapper, JSON
from wikidata.client import Client
from wikidata.entity import EntityId

import difflib

import bleach

# Create your models here.

def wikidata_query_artist(artist_name,spotify_id):
    sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
    sparql.setQuery("""
    SELECT ?artist ?artistSpotifyId
    WHERE
    {{
      ?artist wdt:P31/wdt:P279* wd:Q2088357.
      ?artist rdfs:label ?artistLabel.
      FILTER(LANG(?artistLabel) = "en").
      FILTER REGEX(?artistLabel,"{0}","i").
      OPTIONAL
      {{
        ?artist wdt:P1902 ?artistSpotifyId.
        FILTER REGEX(?artistSpotifyId,"{1}").
      }}.
    }}
    ORDER BY DESC(?artistSpotifyId)
    LIMIT 1
    """.format(artist_name,spotify_id)
    )
    sparql.setReturnFormat(JSON)
    return sparql.query().convert();

def wikidata_serverside_filter(result,spotify_id_key,label_key,label):
    if result["results"]["bindings"][0].get(spotify_id_key) is not None:
        result["results"]["bindings"] = [result["results"]["bindings"][0]]
    else:
        maximum = ({},0.0)
        found = False
        for binding in result["results"]["bindings"]:
            ratio = difflib.SequenceMatcher(None,label,binding[label_key]["value"]).ratio()
            if ratio > maximum[1]:
                maximum = (binding,ratio)
                found = True
        if not found:
            result["results"]["bindings"] = []
        else:
            result["results"]["bindings"] = [maximum[0]]
    return result;

def wikidata_query_album(artist_id,album_name,spotify_id):
    sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
    sparql.setQuery("""
    SELECT ?album ?albumLabel ?albumSpotifyId
    WHERE
    {{
      ?album wdt:P31/wdt:P279* wd:Q482994.
      ?album wdt:P175 wd:{0}.
      ?album rdfs:label ?albumLabel.
      FILTER(LANG(?albumLabel) = "en").
      OPTIONAL
      {{
        ?album wdt:P2205 ?albumSpotifyId.
        FILTER REGEX(?albumSpotifyId,"{1}").
      }}.
    }}
    ORDER BY DESC(?albumSpotifyId)
    """.format(artist_id,spotify_id)
    )
    sparql.setReturnFormat(JSON)
    temp = sparql.query().convert();
    return wikidata_serverside_filter(temp,"albumSpotifyId","albumLabel",album_name);


def wikidata_query_song(artist_id,song_name,spotify_id):
    sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
    sparql.setQuery("""
    SELECT ?song ?songLabel ?songSpotifyId
    WHERE
    {{
      ?song wdt:P31/wdt:P279* wd:Q2188189.
      ?song wdt:P175 wd:{0}.
      ?song rdfs:label ?songLabel.
      FILTER(LANG(?songLabel) = "en").
      OPTIONAL
      {{
        ?song wdt:P2207 ?songSpotifyId.
        FILTER REGEX(?songSpotifyId,"{1}").
      }}.
    }}
    ORDER BY DESC(?songSpotifyId)
    """.format(artist_id,spotify_id)
    )
    sparql.setReturnFormat(JSON)
    temp = sparql.query().convert();
    return wikidata_serverside_filter(temp,"songSpotifyId","songLabel",song_name);


def wikidata_merge_results(artist_res,album_res,song_res):
    merged_data = {
        "results" : {
            "bindings" : [
                {}
            ]
        }
    }
    
    for key,value in artist_res["results"]["bindings"][0].items():
        merged_data["results"]["bindings"][0][key] = value
    
    for key,value in album_res["results"]["bindings"][0].items():
        merged_data["results"]["bindings"][0][key] = value
    
    for key,value in song_res["results"]["bindings"][0].items():
        merged_data["results"]["bindings"][0][key] = value
    
    return merged_data;

def wikidata_sanitize_input(input_list):
    sanitized_list = []
    for input_element in input_list:
        sanitized_element = {}
        for entity,data in input_element.items():
            sanitized_data = {}
            for key,value in data.items():
                sanitized_data[key] = bleach.clean(value)
            sanitized_element[entity] = sanitized_data
        sanitized_list.append(sanitized_element)
    return sanitized_list;
'''
def wikidata_search_track(artist_name,artist_id,album_name,album_id,song_name,song_id):
    sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
#    sparql.setQuery("""
#    SELECT ?artist ?artistLabel ?artistSpotifyId ?album ?albumLabel ?albumSpotifyId ?song ?songLabel ?songSpotifyId
    sparql.setQuery("""
    SELECT ?artist ?artistSpotifyId ?album ?albumSpotifyId ?song ?songSpotifyId
    WHERE
    {{
      ?artist wdt:P31/wdt:P279* wd:Q2088357.
      ?artist rdfs:label ?artistLabel.
      FILTER(LANG(?artistLabel) = "en").
      FILTER REGEX(?artistLabel,"{0}","i").
      OPTIONAL
      {{
        ?artist wdt:P1902 ?artistSpotifyId.
        FILTER REGEX(?artistSpotifyId,"{1}").
      }}.
      
      ?album wdt:P31/wdt:P279* wd:Q482994.
      ?album wdt:P175 ?artist.
      ?album rdfs:label ?albumLabel.
      FILTER(LANG(?albumLabel) = "en").
      FILTER REGEX(?albumLabel,"{2}","i").
      OPTIONAL
      {{
        ?album wdt:P2205 ?albumSpotifyId.
        FILTER REGEX(?albumSpotifyId,"{3}").
      }}.
      
      ?song wdt:P31/wdt:P279* wd:Q2188189.
      ?song wdt:P361 ?album.
      ?song wdt:P175 ?artist.
      ?song rdfs:label ?songLabel.
      FILTER(LANG(?songLabel) = "en").
      FILTER REGEX(?songLabel,"{4}","i").
      OPTIONAL
      {{
        ?song wdt:P2207 ?songSpotifyId.
        FILTER REGEX(?songSpotifyId,"{5}").
      }}.
    }}
    ORDER BY DESC(?artistSpotifyId) DESC(?albumSpotifyId) DESC(?songSpotifyId)
    LIMIT 1
    """.format(artist_name,artist_id,album_name,album_id,song_name,song_id)
    )
    sparql.setReturnFormat(JSON)
    return sparql.query().convert();
'''

def wikidata_search_track(artist_name,artist_id,album_name,album_id,song_name,song_id):
    artist_result = wikidata_query_artist(artist_name,artist_id)
    cleaned_result = wikidata_clean_result(artist_result["results"]["bindings"][0],"artist","artistSpotifyId")
    album_result = wikidata_query_album(cleaned_result["wikidata_id"],album_name,album_id)
    song_result = wikidata_query_song(cleaned_result["wikidata_id"],song_name,song_id)
    merged_result = wikidata_merge_results(artist_result,album_result,song_result)
    return merged_result;

def wikidata_clean_result(result,wikidata_key,spotify_key):
    cleaned_result = {
        "wikidata_id":result[wikidata_key]["value"].split("/")[-1],
    }
    if (result.get(spotify_key) is not None):
        cleaned_result["spotify_id"] = result[spotify_key]["value"]
    else:
        cleaned_result["spotify_id"] = None
    return cleaned_result;

def wikidata_clean_results(results):
    cleaned_results = []
    for result in results["results"]["bindings"]:
        new_element = {}
        new_element["artist"] = wikidata_clean_result(result,"artist","artistSpotifyId")
        new_element["album"] = wikidata_clean_result(result,"album","albumSpotifyId")
        new_element["song"] = wikidata_clean_result(result,"song","songSpotifyId")
        cleaned_results.append(new_element)
    return cleaned_results;

def wikidata_wrap_results(results):
    wrapped_results = []
    client = Client()
    for result in results:
        new_element = {
            "artist" : client.get(EntityId(result["artist"]["wikidata_id"]),True),
            "album" : client.get(EntityId(result["album"]["wikidata_id"]),True),
            "song" : client.get(EntityId(result["song"]["wikidata_id"]),True),
        }
        wrapped_results.append(new_element)
    return wrapped_results;

def wikidata_load_generic(attributes):
    generic = {}
    if len(attributes["labels"]) != 0:
        en_label = attributes["labels"].get("en")
        if en_label is not None:
            generic["label"] = en_label["value"]
    if len(attributes["descriptions"]) != 0:
        en_description = attributes["descriptions"].get("en")
        if en_description is not None:
            generic["description"] = en_description["value"]
    if len(attributes["sitelinks"]) != 0:
        value = attributes["sitelinks"].get("enwiki")
        if value is not None:
            generic["wiki"] = value["url"]
    return generic

def wikidata_stringify_entity_list(client,object_list):
    entity_string = ""
    i = 0
    for obj in object_list:
        entity = client.get(EntityId(obj["mainsnak"]["datavalue"]["value"]["id"]),True)
        if len(entity.attributes["labels"]) != 0:
            en_label = entity.attributes["labels"].get("en")
            if en_label is not None:
                entity_string += en_label["value"]
                if i < len(object_list) - 1:
                    entity_string += ", "
                i = i+1
    return entity_string

def wikidata_stringify_date_list(date_list):
    date_string = ""
    i = 0
    for date in date_list:
        date_string += date["mainsnak"]["datavalue"]["value"]["time"]
        if i < len(date_list) - 1:
            date_string += ", "
        i = i+1
    return date_string

def wikidata_load_artist(attributes):
    artist = wikidata_load_generic(attributes)
    if len(attributes["claims"]) != 0:
        client = Client()
        # artist["z_stuff"] = attributes["claims"]
        location_list = attributes["claims"].get("P740")
        if location_list is not None:
            location_string = wikidata_stringify_entity_list(client,location_list)
            artist["location"] = location_string;
        award_list = attributes["claims"].get("P166")
        if award_list is not None:
            award_string = wikidata_stringify_entity_list(client,award_list)
            artist["awards"] = award_string;
        inception_list = attributes["claims"].get("P571")
        if inception_list is not None:
            artist["inception"] = wikidata_stringify_date_list(inception_list)
    return artist

def wikidata_load_album(attributes):
    album = wikidata_load_generic(attributes)
    if len(attributes["claims"]) != 0:
        client = Client()
        # album["z_stuff"] = attributes["claims"]
        genre_list = attributes["claims"].get("P136")
        if genre_list is not None:
            genre_string = wikidata_stringify_entity_list(client,genre_list)
            album["genre"] = genre_string;
        producer_list = attributes["claims"].get("P162")
        if producer_list is not None:
            producer_string = wikidata_stringify_entity_list(client,producer_list)
            album["producer"] = producer_string;
        release_date_list = attributes["claims"].get("P577")
        if release_date_list is not None:
            album["release date"] = wikidata_stringify_date_list(release_date_list)
            
    return album

def wikidata_load_song(attributes):
    song = wikidata_load_generic(attributes)
    if len(attributes["claims"]) != 0:
        client = Client()
        # song["z_stuff"] = attributes["claims"]
        genre_list = attributes["claims"].get("P136")
        if genre_list is not None:
            genre_string = wikidata_stringify_entity_list(client,genre_list)
            song["genre"] = genre_string;
        instrumentation_list = attributes["claims"].get("P870")
        if instrumentation_list is not None:
            instrumentation_string = wikidata_stringify_entity_list(client,instrumentation_list)
            song["instrumentation"] = instrumentation_string;
        lyrics_by_list = attributes["claims"].get("P676")
        if lyrics_by_list is not None:
            lyrics_by_string = wikidata_stringify_entity_list(client,lyrics_by_list)
            song["lyrics_by"] = lyrics_by_string;
        release_date_list = attributes["claims"].get("P577")
        if release_date_list is not None:
            song["release date"] = wikidata_stringify_date_list(release_date_list)
    return song

def wikidata_download_results(results):
    downloaded_results = []
    for result in results:
        new_element = {
            "artist" : wikidata_load_artist(result["artist"].attributes),
            "album" : wikidata_load_album(result["album"].attributes),
            "song" : wikidata_load_song(result["song"].attributes),
        }
        new_element["artist"]["id"] = result["artist"].id
        new_element["album"]["id"] = result["album"].id
        new_element["song"]["id"] = result["song"].id
        downloaded_results.append(new_element)
    return downloaded_results;

def get_song_info(artist, artist_spotify_id, album, album_spotify_id, track, track_spotify_id):
    results = wikidata_search_track(artist,artist_spotify_id,album,album_spotify_id,track,track_spotify_id)
    cleaned_results = wikidata_clean_results(results)
    wrapped_results = wikidata_wrap_results(cleaned_results)
    downloaded_results = wikidata_download_results(wrapped_results)
    sanitized_results = wikidata_sanitize_input(downloaded_results)
    return sanitized_results;
