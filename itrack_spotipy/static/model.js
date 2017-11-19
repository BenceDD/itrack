function Model() {
	
	// This should be replaced by local storage cache!
	var savedPlaylists = []

	return {
		// This should not cached!
		getCurrentPlaying: function() {
			return new Promise(function(success, error) {
				fetch('http://localhost:8000/ajax/get_current_listening/', {
					method: 'get'
				}).then(res=>res.json()).then(success).catch(error);
			});
		},
		// This can be caced, but can change...
		getUserPlaylist: function() {
	        return new Promise(function(success, error) {
	            fetch('http://localhost:8000/ajax/get_user_playlists/', {
					method: 'get'
				}).then(res=>res.json()).then(success).catch(error);
	        });
	    },
	    // This never changes, so can be cached for a long period.
	    getPlaylistContentByID: function (owner_id, playlist_id) {
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
	}
}