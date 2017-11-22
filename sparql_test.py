
from SPARQLWrapper import SPARQLWrapper, JSON
from wikidata.client import Client
from wikidata.entity import EntityId

from itrack_spotipy.spotipy_app import models

import pprint
import sys

pp = pprint.PrettyPrinter(indent=4)

results = models.wikidata_search_track("JVG","55mdlQp6zN8zdyIYB9DDQj","247365","2tShA8neDBPFY0Bc06qEpx","Tarkenee","3G9gUGRgM4lB2ebVPUcMKI")
cleaned_results = models.wikidata_clean_results(results)
wrapped_results = models.wikidata_wrap_results(cleaned_results)
downloaded_results = models.wikidata_download_results(wrapped_results)

pp.pprint(results)
print("\n\n\n")
pp.pprint(cleaned_results)
print("\n\n\n")
pp.pprint(wrapped_results)
print("\n\n\n")
pp.pprint(downloaded_results)
print("\n\n\n")

sys.stdout.flush()

results = models.wikidata_search_track("Nightwish","2NPduAUeLVsfIauhRwuft1","Once","13BVicwsbPLIaMvr6ivH6B","Wish I Had an Angel","6H8weEvfzCtffIIcwDOK6m")
cleaned_results = models.wikidata_clean_results(results)
wrapped_results = models.wikidata_wrap_results(cleaned_results)
downloaded_results = models.wikidata_download_results(wrapped_results)

pp.pprint(results)
print("\n\n\n")
pp.pprint(cleaned_results)
print("\n\n\n")
pp.pprint(wrapped_results)
print("\n\n\n")
pp.pprint(downloaded_results)
print("\n\n\n")

sys.stdout.flush()

results = models.wikidata_search_track("Anthrax","3JysSUOyfVs1UQ0UaESheP","Persistence Of Time","1FZJXIaK7UEOWUXXChiUqv","Got The Time","62rSF7anVnDAmc9Vnmb7cH")
cleaned_results = models.wikidata_clean_results(results)
wrapped_results = models.wikidata_wrap_results(cleaned_results)
downloaded_results = models.wikidata_download_results(wrapped_results)

pp.pprint(results)
print("\n\n\n")
pp.pprint(cleaned_results)
print("\n\n\n")
pp.pprint(wrapped_results)
print("\n\n\n")
pp.pprint(downloaded_results)
print("\n\n\n")

sys.stdout.flush()
