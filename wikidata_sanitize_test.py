
from itrack_spotipy.spotipy_app import models

test_input = [   {   'album': {   'description': 'album by Anthrax & \' <script>alert("Tunderbaba!")</script>',
                     'genre': 'thrash metal & \' <script>alert("Tunderbaba!")</script>',
                     'id': 'Q1339948 & \' <script>alert("Tunderbaba!")</script>',
                     'label': 'Persistence of Time & \' <script>alert("Tunderbaba!")</script>',
                     'wiki': 'https://en.wikipedia.org/wiki/Persistence_of_Time & \' <script>alert("Tunderbaba!")</script>'},
        'artist': {   'description': 'American heavy metal band & \' <script>alert("Tunderbaba!")</script>',
                      'id': 'Q109871 & \' <script>alert("Tunderbaba!")</script>',
                      'label': 'Anthrax & \' <script>alert("Tunderbaba!")</script>',
                      'wiki': 'https://en.wikipedia.org/wiki/Anthrax_(American_band) & \' <script>alert("Tunderbaba!")</script>'},
        'song': {   'genre': 'new wave music & \' <script>alert("Tunderbaba!")</script>',
                    'id': 'Q18663649 & \' <script>alert("Tunderbaba!")</script>',
                    'label': 'Got the Time & \' <script>alert("Tunderbaba!")</script>',
                    'wiki': 'https://en.wikipedia.org/wiki/Got_the_Time & \' <script>alert("Tunderbaba!")</script>'}}] 

print(test_input)

print("in the following output in every value every &,<,>,/ and ' should be converted into & --> &amp;< --> &lt;> --> &gt;\" --> &quot;\' --> &#x27;")

sanitized_input = models.wikidata_sanitize_input(test_input)

print(sanitized_input)
