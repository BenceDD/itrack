from django.db import models

from SPARQLWrapper import SPARQLWrapper, JSON
from wikidata.client import Client
from wikidata.entity import EntityId

import bleach

# Create your models here.

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

def wikidata_clean_results(results):
    decoded_result = []
    for result in results["results"]["bindings"]:
        new_element = {}
        new_element["artist"] = {
            "wikidata_id":result["artist"]["value"].split("/")[-1],
        }
        if (result.get("artistSpotifyId") is not None):
            new_element["artist"]["spotify_id"] = result["artistSpotifyId"]["value"]
        else:
            new_element["artist"]["spotify_id"] = None
        
        new_element["album"] = {
            "wikidata_id":result["album"]["value"].split("/")[-1],
        }
        if (result.get("albumSpotifyId") is not None):
            new_element["album"]["spotify_id"] = result["albumSpotifyId"]["value"]
        else:
            new_element["album"]["spotify_id"] = None
        
        new_element["song"] = {
            "wikidata_id":result["song"]["value"].split("/")[-1],
        }
        if (result.get("songSpotifyId") is not None):
            new_element["song"]["spotify_id"] = result["songSpotifyId"]["value"]
        else:
            new_element["song"]["spotify_id"] = None
        
        decoded_result.append(new_element)
    return decoded_result;

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
        generic["label"] = attributes["labels"]["en"]["value"]
    if len(attributes["descriptions"]) != 0:
        generic["description"] = attributes["descriptions"]["en"]["value"]
    if len(attributes["sitelinks"]) != 0:
        value = attributes["sitelinks"].get("enwiki")
        if value is not None:
            generic["wiki"] = value["url"]
    return generic

def wikidata_stringify_entity_list(client,object_list):
    genre_string = ""
    i = 0
    for obj in object_list:
        entity = client.get(EntityId(obj["mainsnak"]["datavalue"]["value"]["id"]),True)
        if len(entity.attributes["labels"]) != 0:
            genre_string += entity.attributes["labels"]["en"]["value"]
            if i < len(object_list) - 1:
                genre_string += ", "
            i = i+1
    return genre_string

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
