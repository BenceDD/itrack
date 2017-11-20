function View() {
	var model = Model()
	var default_album_cover = 'https://lh3.googleusercontent.com/UrY7BAZ-XfXGpfkeWg0zCCeo-7ras4DCoRalC_WXXWTK9q5b0Iw7B0YQMsVxZaNB7DM=w300-rw'

	function updateSongCard(track, now_playlig) {
		if (now_playlig)
			document.getElementById("currently_playing_header").innerHTML = 'Jelenleg ezt hallgatod'
		else
			document.getElementById("currently_playing_header").innerHTML = 'Lejátszási listáról'

		document.getElementById("currently_playing_div").innerHTML = track['artists'].join(', ') + ' - ' +  track['title']
		
		var image_url = default_album_cover
		if (track['image'] != null)
			image_url = track['image']
		document.getElementById('album_cover').src = image_url
	}

	function playlistCardHeadingID(playlist_id) {
		return 'track_heading_' + playlist_id
	}

	function playlistCardCollapseID(playlist_id) {
		return 'track_collapse_' + playlist_id
	}

	function playlistCardContentID(playlist_id) {
		return 'track_content_' + playlist_id 
	}

	function displayCards(user_playlists) {

		function createPlaylistCard(parent_id, playlist_id, header_content, collapse_content) {
			var collapse_id = playlistCardCollapseID(playlist_id)
			// TODO: ez szörnyen néz ki.
			var heading_html = '<div class="card-header" role="tab" id="' + playlistCardHeadingID(playlist_id) +
				'"><h6 class="mb-0"><a data-toggle="collapse" onclick="view.fillPlaylistCardWithSongs(\'' + playlist_id + '\')" href="#' + collapse_id +
				'" aria-expanded="true" aria-controls="' + collapse_id + '">' + header_content + '</a></h5></div>';
			var collapse_html = '<div id="' + collapse_id + '" class="collapse" role="tabpanel" aria-labelledby="headingOne" data-parent="#' + parent_id + 
				'"><div id="' + playlistCardContentID(playlist_id) + '" class="card-body">' + collapse_content + '</div></div>'
			return '<p><div class="card bg-light">' + heading_html + collapse_html + '</div></p>';
		}
		
		// TODO: vagy JQuery vagy NE.
		var table = $('#track_cards_div')
		for (i in user_playlists) 
		    table.append(createPlaylistCard('track_cards_div', user_playlists[i]['playlist_id'], user_playlists[i]['name'], 'Betöltés...'));
	}

	function fillPlaylistWithTracklist(playlist_id, tracklist) {
		function makeRow(no, title, artists, album, track_id) {
			return '<tr onclick="view.updateSongCard(\'' + track_id + '\')"><th scope="row">' + no + '</th><td>' + title + '</td><td>' + 
				artists.join(', ')  + '</td><td>' + album + '</td></tr>'
		}

		var artist_title = 'Előadó'
		var album_title = 'Album'
		var track_title = 'Cím'

		var content = '<table class="table table-hover"><thead><tr><th scope="col">#</th><th scope="col">' + track_title + 
				'</th><th scope="col">' + artist_title + '</th><th scope="col">' + album_title + '</th></tr></thead><tbody>'
		for (i in tracklist) 
			content += makeRow(String(Number(i) + 1), tracklist[i]['title'], tracklist[i]['artists'], tracklist[i]['album'], tracklist[i]['track_id'])
		content += '</tbody></table>'

		document.getElementById(playlistCardContentID(playlist_id)).innerHTML = content
	}

	return {
		updateSongCard: function(track_id) {
			if (track_id == null) {
				model.getCurrentPlaying().then(function(track) {
					updateSongCard(track, true)
				})
			} else {
				updateSongCard(model.getTrackByID(track_id), false)
			}
		},
		updatePlaylistCards: function() {
			model.getUserPlaylist().then(function(playlists) {
				displayCards(playlists)
			})
		},
		fillPlaylistCardWithSongs: function(playlist_id) {
			// this name 'fillPlaylistCardWithSongs' referred in the createPlaylistCard method!!
			model.getPlaylistContentByID(playlist_id).then(function(tracklist) {
				fillPlaylistWithTracklist(playlist_id, tracklist)
			})
		}
	}
}
