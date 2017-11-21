function Model() {
    
    // This should be replaced by local storage cache!
    var savedPlaylists = {}
    var userPlaylist = null
    
    function getCurrentPlaying() {
        return new Promise(function(success, error) {
            fetch('http://localhost:8000/ajax/get_current_listening/', {
                method: 'get'
            }).then(res=>res.json()).then(function(result) {
                return result['track']
            }).then(success).catch(error);
        });
    }

    function getUserPlaylist() {
        return new Promise(function(success, error) {
            if (userPlaylist != null) {
                success(userPlaylist)
                return
            }
            fetch('http://localhost:8000/ajax/get_user_playlists/', {
                method: 'get'
            }).then(res=>res.json()).then(function(result) {
                userPlaylist = result['playlists']
                return userPlaylist
            }).then(success).catch(error);
        });
    }

    function getPlaylistContentByID(playlist_id) {
        return new Promise(function(success, error) {
            if (savedPlaylists[playlist_id] != null) {
                success(savedPlaylists[playlist_id])
                return
            }
            getUserPlaylist().then(function(playlists) {
                var owner_id = null
                for (i in playlists) {
                    if (playlists[i]['playlist_id'] == playlist_id)
                        owner_id = playlists[i]['owner_id']
                }
                return owner_id
            }).then(function(owner_id) {
                var data = new FormData();
                data.append('playlist_id', playlist_id)
                data.append('owner_id', owner_id)
                data.append('csrfmiddlewaretoken', jQuery("[name=csrfmiddlewaretoken]").val());
                return fetch("http://localhost:8000/ajax/get_playlist_by_id/", {
                    method: 'POST',
                    body: data,
                    credentials: 'same-origin',
                })
            }).then(res=>res.json()).then(function(result) {
                savedPlaylists[playlist_id] = result['playlist']
                return savedPlaylists[playlist_id]
            }).then(success).catch(error);
        });
    }

    return {
        getCurrentPlaying: getCurrentPlaying,
        getUserPlaylist: getUserPlaylist,
        getPlaylistContentByID: getPlaylistContentByID,
        getTrackByID: function(track_id) {
            for (list in savedPlaylists) {
                for (track in savedPlaylists[list]) {
                    if (savedPlaylists[list][track]['track_id'] == track_id)
                        return savedPlaylists[list][track]
                }
            }
        },
    }
}