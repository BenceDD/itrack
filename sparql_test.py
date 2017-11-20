
from SPARQLWrapper import SPARQLWrapper, JSON
from wikidata.client import Client
from wikidata.entity import EntityId

import pprint
import sys

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
        generic["label"] = attributes["labels"]["en"]
    if len(attributes["descriptions"]) != 0:
        generic["description"] = attributes["descriptions"]["en"]
    if len(attributes["sitelinks"]) != 0:
        value = attributes["sitelinks"].get("enwiki")
        if value is not None:
            generic["wiki"] = value
    return generic

def wikidata_load_artist(attributes):
    artist = wikidata_load_generic(attributes)
    if len(attributes["claims"]) != 0:
        artist["stuff"] = attributes["claims"]
    return artist

def wikidata_load_album(attributes):
    album = wikidata_load_generic(attributes)
    if len(attributes["claims"]) != 0:
        album["stuff"] = attributes["claims"]
    return album

def wikidata_load_song(attributes):
    song = wikidata_load_generic(attributes)
    if len(attributes["claims"]) != 0:
        song["stuff"] = attributes["claims"]
    return song

def wikidata_download_results(results):
    downloaded_results = []
    for result in results:
        new_element = {
            "artist" : wikidata_load_artist(result["artist"].attributes),
            "album" : wikidata_load_album(result["album"].attributes),
            "song" : wikidata_load_song(result["song"].attributes),
        }
        downloaded_results.append(new_element)
    return downloaded_results;

pp = pprint.PrettyPrinter(indent=4)

results = wikidata_search_track("JVG","55mdlQp6zN8zdyIYB9DDQj","247365","2tShA8neDBPFY0Bc06qEpx","Tarkenee","3G9gUGRgM4lB2ebVPUcMKI")
cleaned_results = wikidata_clean_results(results)
wrapped_results = wikidata_wrap_results(cleaned_results)
downloaded_results = wikidata_download_results(wrapped_results)

pp.pprint(results)
pp.pprint("\n\n\n")
pp.pprint(cleaned_results)
pp.pprint("\n\n\n")
pp.pprint(wrapped_results)
pp.pprint("\n\n\n")
pp.pprint(downloaded_results)
pp.pprint("\n\n\n")

sys.stdout.flush()

results = wikidata_search_track("Nightwish","2NPduAUeLVsfIauhRwuft1","Once","13BVicwsbPLIaMvr6ivH6B","Wish I Had an Angel","6H8weEvfzCtffIIcwDOK6m")
cleaned_results = wikidata_clean_results(results)
wrapped_results = wikidata_wrap_results(cleaned_results)
downloaded_results = wikidata_download_results(wrapped_results)

pp.pprint(results)
pp.pprint("\n\n\n")
pp.pprint(cleaned_results)
pp.pprint("\n\n\n")
pp.pprint(wrapped_results)
pp.pprint("\n\n\n")
pp.pprint(downloaded_results)
pp.pprint("\n\n\n")

sys.stdout.flush()

results = wikidata_search_track("Anthrax","3JysSUOyfVs1UQ0UaESheP","Persistence Of Time","1FZJXIaK7UEOWUXXChiUqv","Got The Time","62rSF7anVnDAmc9Vnmb7cH")
cleaned_results = wikidata_clean_results(results)
wrapped_results = wikidata_wrap_results(cleaned_results)
downloaded_results = wikidata_download_results(wrapped_results)

pp.pprint(results)
pp.pprint("\n\n\n")
pp.pprint(cleaned_results)
pp.pprint("\n\n\n")
pp.pprint(wrapped_results)
pp.pprint("\n\n\n")
pp.pprint(downloaded_results)
pp.pprint("\n\n\n")

sys.stdout.flush()
