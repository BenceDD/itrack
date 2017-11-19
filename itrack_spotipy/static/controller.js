function Controller() {
	// model functions
	function getCurrentPlaying() {
		return new Promise(function(success, error) {
			fetch('http://localhost:8000/ajax/get_current_listening/', {
				method: 'get'
			}).then(res=>res.json()).then(success).catch(error);
		});
	}

	function getUserPlaylist() {
        return new Promise(function(success, error) {
            fetch('http://localhost:8000/ajax/get_user_playlists/', {
				method: 'get'
			}).then(res=>res.json()).then(success).catch(error);
        });
    }

    function getPlaylistContentByID(owner_id, playlist_id) {
    	return new Promise(function(success, error) {
			var data = new FormData();
			data.append('playlist_id', playlist_id)
			data.append('owner_id', owner_id)
			data.append('csrfmiddlewaretoken', jQuery("[name=csrfmiddlewaretoken]").val());
			fetch("http://localhost:8000/ajax/get_playlist_by_id/", {
			    method: 'POST',
			    body: data,
			    credentials: 'same-origin',
			}).then(res=>res.json()).then(success).catch(error);
		});
	}

	// view functions
	function updateSongCard(track) {
		document.getElementById("currently_playing_div").innerHTML = track['artist'] + ' - ' +  track['title']
	}


	function updatePlaylistCards(playlists) {

		function makePlaylistCardTable(playlist) {
			// data is a list of name, artis and album
			var artist_title = 'Előadó'
			var album_title = 'Album'
			var track_title = 'Cím'
			//console.log(data)
			var content = '<table class="table table-striped"> <thead> <tr> <th scope="col">#</th> <th scope="col">' + track_title + 
				'</th> <th scope="col">' + artist_title + '</th> <th scope="col">' + album_title + '</th> </tr> </thead> <tbody> <tr> <th scope="row">1</th> <td>Mark</td> <td>Otto</td> <td>@mdo</td> </tr> <tr> <th scope="row">2</th> <td>Jacob</td> <td>Thornton</td> <td>@fat</td> </tr> <tr> <th scope="row">3</th> <td>Larry</td> <td>the Bird</td> <td>@twitter</td> </tr> </tbody></table>'
			return content
		}

		function createPlaylistCard(parent_id, id, header_content, collapse_content) {
			var heading_id = 'track_heading_' + id
			var collapse_id = 'track_collapse_' + id
			// TODO: ez szörnyen néz ki.
			var heading_html = '<div class="card-header" role="tab" id="' + heading_id + '"><h6 class="mb-0"><a data-toggle="collapse" href="#' + collapse_id +
				'" aria-expanded="true" aria-controls="' + collapse_id + '">' + header_content + '</a></h5></div>';
			var collapse_html = '<div id="' + collapse_id + '" class="collapse" role="tabpanel" aria-labelledby="headingOne" data-parent="#' + parent_id + 
				'"><div class="card-body">' + collapse_content + '</div></div>'

			return '<p><div class="card bg-light">' + heading_html + collapse_html + '</div></p>';
		}

		return new Promise(function(success) {
			// TODO: vagy JQuery vagy NE.
			var table = $('#track_cards_div')
			for (id in playlists) {
			    table.append(createPlaylistCard('track_cards_div', id, playlists[id]['name'], 'Betöltés...'));
			}
			success()
		});
	}

	return {
		updateCurrentPlayling: function() {
			getCurrentPlaying().then(function(result) {
				updateSongCard(result['track'])
			})
		},
		updatePlaylistCards: function() {
			getUserPlaylist().then(function(result) {
				return result['playlists']
			}).then(updatePlaylistCards)
		},
		getPlaylistContentByID: getPlaylistContentByID // csak azért hogy működjön a gomb..
	}
}