function View() {
    var default_album_cover = 'https://lh3.googleusercontent.com/UrY7BAZ-XfXGpfkeWg0zCCeo-7ras4DCoRalC_WXXWTK9q5b0Iw7B0YQMsVxZaNB7DM=w300-rw'

    // html setters/getters...
    function set_song_card_header(message) { $('#song_card_header').html(message) }
    function set_song_card_title(title) { $('#song_card_title').html(title) }
    function set_song_card_content(content) { $('#song_card_content').html(content) }
    function set_album_cover_src(src) { $("#album_cover").attr("src", src) }
    function set_album_card_title(title) { $('#album_card_title').html(title) }
    function set_album_card_content(content) { $('#album_card_content').html(content) }
    function set_album_card_link_wp(link) { $('#album_card_link_wp').attr('href', link) }
    function set_album_card_link_wd(link) { $('#album_card_link_wd').attr('href', link) }
    function set_artist_card_title(title) { $('#artist_card_title').html(title) }
    function set_artist_card_content(content) { $('#artist_card_content').html(content) }
    function set_artist_card_link_wp(link) { $('#artist_card_link_wp').attr('href', link) }
    function set_artist_card_link_wd(link) { $('#artist_card_link_wd').attr('href', link) }
    function toggle_album_card(visible) { $('#album_card').toggle(visible) }
    function toggle_artist_card(visible) { $('#artist_card').toggle(visible) }
    function toggle_song_card_album_sparator(visible) { $('#song_card_album_sparator').toggle(visible) }
    function toggle_album_artist_sparator(visible) { $('#album_artist_sparator').toggle(visible) }
    function get_playlist_container() { return $('#playlist_container') }

    function get_playlist_card_heading_id(playlist_id) { return 'playlist_heading_' + playlist_id }
    function get_playlist_card_collapse_id(playlist_id) { return 'playlist_collapse_' + playlist_id }
    function get_playlist_card_content_id(playlist_id) { return 'playlist_content_' + playlist_id }
    function get_playlist_card_with_id(playlist_id) { return $('#' + get_playlist_card_content_id(playlist_id)) }

    // code generators
    function createPlaylistCard(parent_id, playlist_id, header_content, collapse_content) {
        // This is create a single playlist item, fill with the given data. 
        var collapse_id = get_playlist_card_collapse_id(playlist_id)
        var heading_html = '<div class="card-header" role="tab" id="' + get_playlist_card_heading_id(playlist_id) +
            '"><h6 class="mb-0"><a data-toggle="collapse" onclick="controller.fillPlaylistCardWithSongs(\'' + playlist_id + '\')" href="#' + collapse_id +
            '" aria-expanded="true" aria-controls="' + collapse_id + '">' + header_content + '</a></h5></div>';
        var collapse_html = '<div id="' + collapse_id + '" class="collapse" role="tabpanel" aria-labelledby="headingOne" data-parent="#' + parent_id + 
            '"><div id="' + get_playlist_card_content_id(playlist_id) + '" class="card-body">' + collapse_content + '</div></div>'
        return '<p><div class="card bg-light">' + heading_html + collapse_html + '</div></p>';
    }

    function makeTableRow(no, title, artists, album, track_id) {
        artists_array = []
        for (i in artists) 
            artists_array.push(artists[i]['name'])

        if (track_id)
            return '<tr onclick="controller.updateSongCard(\'' + track_id + '\')"><th scope="row">' + no + '</th><td>' + title + '</td><td>' + 
                artists_array.join(', ')  + '</td><td>' + album + '</td></tr>'
        else
            return '<tr"><th scope="row" class="text-muted">' + no + '</th><td class="text-muted">' + title + '</td><td class="text-muted">' + 
                artists_array.join(', ')  + '</td><td class="text-muted">' + album + '</td></tr>'
    }

    function makeTableData(tracklist) {
        var artist_title = 'Előadó'
        var album_title = 'Album'
        var track_title = 'Cím'

        var table_data = '<table class="table table-hover"><thead><tr><th scope="col">#</th><th scope="col">' + track_title + 
                '</th><th scope="col">' + artist_title + '</th><th scope="col">' + album_title + '</th></tr></thead><tbody>'
        for (i in tracklist) 
            table_data += makeTableRow(String(Number(i) + 1), tracklist[i]['title'], tracklist[i]['artists'], tracklist[i]['album'], tracklist[i]['track_id'])
        table_data += '</tbody></table>'
        return table_data
    }

    // state functions
    function spotifyLoading() {
        toggle_album_card(false)
        toggle_artist_card(false)
        toggle_song_card_album_sparator(false)
        toggle_album_artist_sparator(false)
        set_song_card_header('Betöltés...')
        set_album_card_title('A jelenleg hallgatott szám címe')
        set_song_card_content('Az adatok lekérése folyamatban. Itt fognak majd megjelenni az információk a kiválaszott számmal kapcsolatban.')
        set_album_cover_src(default_album_cover)
    }

    function displaySong(track, now_playlig) {
        if (now_playlig)
            set_song_card_header('Jelenleg ezt hallgatod')
        else
            set_song_card_header('Lejátszási listáról')

        artists = []
        for (i in track['artists']) 
            artists.push(track['artists'][i]['name'])

        set_song_card_title(artists.join(', ') + ' - ' +  track['title'])

        if (track['image'] != null)
            set_album_cover_src(track['image'])
        else 
            set_album_cover_src(default_album_cover)
    }

    function displayPlaylistCards(user_playlists) {
        var table = get_playlist_container()
        for (i in user_playlists) 
            table.append(createPlaylistCard('playlist_container', user_playlists[i]['playlist_id'], user_playlists[i]['name'], 'Betöltés...'));
    }

    function displayPlaylistCardContent(playlist_id, tracklist) {
        var table_data = makeTableData(tracklist)
        get_playlist_card_with_id(playlist_id).html(table_data)
    }

    function displaySongInfo(info) {
        if ('text' in info['song'])
            set_song_card_content(info['song']['text'])
        else
            set_song_card_content('Sajnos nem található adat ehhez a számhoz.')
        
        if ('label' in info['album'] && 'text' in info['album']) {
            set_album_card_title('Album: ' + info['album']['label'])
            set_album_card_content(info['album']['text'])
            set_album_card_link_wp(info['album']['wiki'])
            set_album_card_link_wd('https://www.wikidata.org/wiki/' + info['album']['id'])
            toggle_song_card_album_sparator(true)
            toggle_album_card(true)
        }
        
        if ('label' in info['artist'] && 'text' in info['artist']) {
            set_artist_card_title('Előadó: ' + info['artist']['label'])
            set_artist_card_content(info['artist']['text'])
            set_artist_card_link_wp(info['artist']['wiki'])
            set_artist_card_link_wd('https://www.wikidata.org/wiki/' + info['artist']['id'])
            toggle_album_artist_sparator(true)
            toggle_artist_card(true)
        }
    }

    return {
        spotifyLoading: spotifyLoading,
        displaySong: displaySong,
        displayPlaylistCards: displayPlaylistCards,
        displayPlaylistCardContent: displayPlaylistCardContent,
        displaySongInfo: displaySongInfo,
        spotifyError: function() {
            set_song_card_header('A Spotify sajnos nem éhető el')
            set_song_card_title(':(')
        },
        wikidataError: function() {
            set_song_card_header('Valami gond volt a WikiData adatok lekérése közben...')
        }
    }
}
