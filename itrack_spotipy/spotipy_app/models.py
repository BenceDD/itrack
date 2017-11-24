from django.db import models

from SPARQLWrapper import SPARQLWrapper, JSON
from wikidata.client import Client
from wikidata.entity import EntityId

import difflib
import bleach

# Create your models here.

class WikiDataWrapper:

    artist_band_query_string = """
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
    """
    
    artist_human_query_string = """
        SELECT ?artist ?artistSpotifyId
        WHERE
        {{
          ?artist wdt:P31 wd:Q5.
          ?artist wdt:P358 ?discography.
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
    """

    album_query_string = """
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
    """

    song_query_string = """
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
    """

    def query_artist_band(self, artist_name, spotify_id):
        sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
        sparql.setQuery(self.artist_band_query_string.format(artist_name, spotify_id))
        sparql.setReturnFormat(JSON)
        return sparql.query().convert()["results"]
	
    def query_artist_human(self, artist_name, spotify_id):
        sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
        sparql.setQuery(self.artist_human_query_string.format(artist_name, spotify_id))
        sparql.setReturnFormat(JSON)
        return sparql.query().convert()["results"]

    def query_artist(self, artist_name, spotify_id):
        result = self.query_artist_band(artist_name,spotify_id)
        if len(result["bindings"]) == 0:
            result = self.query_artist_human(artist_name,spotify_id)
        return result;

    def query_album(self, artist_id, album_name, spotify_id):
        sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
        sparql.setQuery(self.album_query_string.format(artist_id,spotify_id))
        sparql.setReturnFormat(JSON)
        temp = sparql.query().convert()["results"]
        return self.serverside_filter(temp, "albumSpotifyId", "albumLabel", album_name);

    def query_song(self, artist_id, song_name, spotify_id):
        sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
        sparql.setQuery(self.song_query_string.format(artist_id, spotify_id))
        sparql.setReturnFormat(JSON)
        temp = sparql.query().convert()["results"]
        return self.serverside_filter(temp, "songSpotifyId", "songLabel", song_name);

    def serverside_filter(self, result, spotify_id_key, label_key, label):
        if len(result["bindings"]) == 0:
            return result;
        if result["bindings"][0].get(spotify_id_key) is not None:
            result["bindings"] = [result["bindings"][0]]
        else:
            maximum = ({},0.0)
            found = False
            for binding in result["bindings"]:
                ratio = difflib.SequenceMatcher(None, label, binding[label_key]["value"]).ratio()
                if ratio > maximum[1]:
                    maximum = (binding,ratio)
                    found = True
            if not found:
                result["bindings"] = []
            else:
                result["bindings"] = [maximum[0]]
        return result;

    def merge_results(self, artist_res, album_res, song_res):
        bindings = {}
        if len(artist_res["bindings"]) > 0:
            bindings.update(artist_res["bindings"][0])
        if len(album_res["bindings"]) > 0:
            bindings.update(album_res["bindings"][0])
        if len(song_res["bindings"]) > 0:
            bindings.update(song_res["bindings"][0])
        return {
            "bindings" : [
                bindings,
            ]
        };

    def sanitize_input(self, input_list):
        sanitized_list = []
        for input_element in input_list:
            sanitized_element = {}
            for entity,data in input_element.items():
                sanitized_data = {}
                for key, value in data.items():
                    sanitized_data[key] = bleach.clean(value)
                sanitized_element[entity] = sanitized_data
            sanitized_list.append(sanitized_element)
        return sanitized_list;

    def search_track(self, artist_name, artist_id, album_name, album_id, song_name, song_id):
        artist_result = self.query_artist(artist_name,artist_id)
        album_result = {"bindings" : []}
        song_result = {"bindings" : []}
        if len(artist_result["bindings"]) > 0:
            cleaned_result = self.clean_result(artist_result["bindings"][0], "artist", "artistSpotifyId")
            album_result = self.query_album(cleaned_result["wikidata_id"], album_name, album_id)
            song_result = self.query_song(cleaned_result["wikidata_id"], song_name, song_id)
        merged_result = self.merge_results(artist_result, album_result, song_result)
        return merged_result;

    def clean_result(self, result, wikidata_key, spotify_key):
        wikidata_result = result.get(wikidata_key)
        if wikidata_result is None:
            return None;
        cleaned_result = {
            "wikidata_id":wikidata_result["value"].split("/")[-1],
        }
        if (result.get(spotify_key) is not None):
            cleaned_result["spotify_id"] = result[spotify_key]["value"]
        else:
            cleaned_result["spotify_id"] = None
        return cleaned_result;

    def clean_results(self, results):
        cleaned_results = []
        for result in results["bindings"]:
            new_element = {}
            new_element["artist"] = self.clean_result(result, "artist", "artistSpotifyId")
            new_element["album"] = self.clean_result(result, "album", "albumSpotifyId")
            new_element["song"] = self.clean_result(result, "song", "songSpotifyId")
            cleaned_results.append(new_element)
        return cleaned_results;

    def wrap_results(self, results):
        wrapped_results = []
        client = Client()
        for result in results:
            artist_data = result.get("artist")
            album_data = result.get("album")
            song_data = result.get("song")
            new_element = {}
            if artist_data is not None:
                new_element["artist"] = client.get(EntityId(artist_data["wikidata_id"]), True)
            else:
                new_element["artist"] = None
            if album_data is not None:
                new_element["album"] = client.get(EntityId(album_data["wikidata_id"]), True)
            else:
                new_element["album"] = None
            if song_data is not None:
                new_element["song"] = client.get(EntityId(song_data["wikidata_id"]), True)
            else:
                new_element["song"] = None
            wrapped_results.append(new_element)
        return wrapped_results;

    def load_generic(self, attributes):
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

    def stringify_entity_list(self, client, object_list):
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

    def stringify_date_list(self, date_list):
        date_string = ""
        i = 0
        for date in date_list:
            date_string += date["mainsnak"]["datavalue"]["value"]["time"]
            if i < len(date_list) - 1:
                date_string += ", "
            i = i+1
        return date_string

    def load_artist(self, attributes):
        artist = self.load_generic(attributes)
        if len(attributes["claims"]) != 0:
            client = Client()
            # artist["z_stuff"] = attributes["claims"]
            location_list = attributes["claims"].get("P740")
            if location_list is not None:
                location_string = self.stringify_entity_list(client,location_list)
                artist["location"] = location_string;
            award_list = attributes["claims"].get("P166")
            if award_list is not None:
                award_string = self.stringify_entity_list(client,award_list)
                artist["awards"] = award_string;
            inception_list = attributes["claims"].get("P571")
            if inception_list is not None:
                artist["inception"] = self.stringify_date_list(inception_list)
        return artist

    def load_album(self, attributes):
        album = self.load_generic(attributes)
        if len(attributes["claims"]) != 0:
            client = Client()
            # album["z_stuff"] = attributes["claims"]
            genre_list = attributes["claims"].get("P136")
            if genre_list is not None:
                genre_string = self.stringify_entity_list(client,genre_list)
                album["genre"] = genre_string;
            producer_list = attributes["claims"].get("P162")
            if producer_list is not None:
                producer_string = self.stringify_entity_list(client,producer_list)
                album["producer"] = producer_string;
            release_date_list = attributes["claims"].get("P577")
            if release_date_list is not None:
                album["release date"] = self.stringify_date_list(release_date_list)
                
        return album

    def load_song(self, attributes):
        song = self.load_generic(attributes)
        if len(attributes["claims"]) != 0:
            client = Client()
            # song["z_stuff"] = attributes["claims"]
            genre_list = attributes["claims"].get("P136")
            if genre_list is not None:
                genre_string = self.stringify_entity_list(client,genre_list)
                song["genre"] = genre_string;
            instrumentation_list = attributes["claims"].get("P870")
            if instrumentation_list is not None:
                instrumentation_string = self.stringify_entity_list(client,instrumentation_list)
                song["instrumentation"] = instrumentation_string;
            lyrics_by_list = attributes["claims"].get("P676")
            if lyrics_by_list is not None:
                lyrics_by_string = self.stringify_entity_list(client,lyrics_by_list)
                song["lyrics_by"] = lyrics_by_string;
            release_date_list = attributes["claims"].get("P577")
            if release_date_list is not None:
                song["release date"] = self.stringify_date_list(release_date_list)
        return song

    def wikidata_download_results(self, results):
        downloaded_results = []
        for result in results:
            new_element = {}
            if result["artist"] is not None:
                new_element["artist"] = self.load_artist(result["artist"].attributes)
                new_element["artist"]["id"] = result["artist"].id
            else:
                new_element["artist"] = None
            if result["album"] is not None:
                new_element["album"] = self.load_album(result["album"].attributes)
                new_element["album"]["id"] = result["album"].id
            else:
                new_element["album"] = None
            if result["song"] is not None:
                new_element["song"] = self.load_song(result["song"].attributes)
                new_element["song"]["id"] = result["song"].id
            else:
                new_element["song"] = None
            downloaded_results.append(new_element)
        return downloaded_results;

    def get_song_info(self, artist, artist_spotify_id, album, album_spotify_id, track, track_spotify_id):
        results = self.search_track(artist, artist_spotify_id, album, album_spotify_id, track, track_spotify_id)
        cleaned_results = self.clean_results(results)
        wrapped_results = self.wrap_results(cleaned_results)
        downloaded_results = self.wikidata_download_results(wrapped_results)
        sanitized_results = self.sanitize_input(downloaded_results)
        return sanitized_results;
