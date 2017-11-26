function Controller() {
    var model = Model()
    var view = View()

    return {
        updateSongCard: function(track_id) {
            view.spotifyLoading()
            if (track_id == null) {
                model.getCurrentPlaying().then(function(track) {
                    view.displaySong(track, true)
                    return track
                }).then(function(track) {
                    view.wikidataLoading()
                    return model.getSongInfo(track)
                }).then(function(info) {
                    view.displaySongInfo(info)
                }).catch(function(msg) {
                    console.log(msg)
                    view.wikidataError()
                })
            } else {
                var track = model.getTrackByID(track_id)
                view.displaySong(track, false)
                view.wikidataLoading()
                model.getSongInfo(track).then(function(info) {
                    view.displaySongInfo(info)
                }).catch(function(msg) {
                    console.log(msg)
                    view.wikidataError()
                })
            }
        },
        updatePlaylistCards: function() {
            model.getUserPlaylist().then(function(playlists) {
                view.displayPlaylistCards(playlists)
            }).catch(function(msg) {
                console.log(msg)
                view.spotifyError()
            })
        },
        fillPlaylistCardWithSongs: function(playlist_id) {
            // this name 'fillPlaylistCardWithSongs' referred in the createPlaylistCard method!!
            model.getPlaylistContentByID(playlist_id).then(function(tracklist) {
                view.displayPlaylistCardContent(playlist_id, tracklist)
            }).catch(function(msg) {
                console.log(msg)
                view.spotifyError()
            })
        },
        resetView: view.resetView
    }
}
