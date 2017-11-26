function View() {
    var default_album_cover = 'https://lh3.googleusercontent.com/UrY7BAZ-XfXGpfkeWg0zCCeo-7ras4DCoRalC_WXXWTK9q5b0Iw7B0YQMsVxZaNB7DM=w300-rw'

    // html setters/getters...
    function set_song_card_header(message) { $('#song_card_header').html(message) }
    function set_song_card_title(title) { $('#song_card_title').html(title) }
    function set_song_card_content(content) { $('#song_card_content').html(content) }
    function set_song_card_link_wp(link) { $('#song_card_link_wp').attr('href', link) }
    function set_song_card_link_wd(link) { $('#song_card_link_wd').attr('href', link) }
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
    function toggle_song_card_link_wp(visible) { $('#song_card_link_wp').toggle(visible) }
    function toggle_song_card_link_wd(visible) { $('#song_card_link_wd').toggle(visible) }
    function toggle_album_card_link_wp(visible) { $('#album_card_link_wp').toggle(visible) }
    function toggle_album_card_link_wd(visible) { $('#album_card_link_wd').toggle(visible) }
    function toggle_artist_card_link_wp(visible) { $('#artist_card_link_wp').toggle(visible) }
    function toggle_artist_card_link_wd(visible) { $('#artist_card_link_wd').toggle(visible) }
    function toggle_song_card_album_sparator(visible) { $('#song_card_album_sparator').toggle(visible) }
    function toggle_album_artist_sparator(visible) { $('#album_artist_sparator').toggle(visible) }
    function get_playlist_container() { return $('#playlist_container') }
    function get_song_card_info_list() { return $('#song_card_info_list') }
    function get_album_card_info_list() { return $('#album_card_info_list') }
    function get_artist_card_info_list() { return $('#artist_card_info_list') }
    function empty_song_card_info_list() { $('#song_card_info_list').empty() }
    function empty_album_card_info_list() { $('#album_card_info_list').empty() }
    function empty_artist_card_info_list() { $('#artist_card_info_list').empty() }

    function get_playlist_card_heading_id(playlist_id) { return 'playlist_heading_' + playlist_id }
    function get_playlist_card_collapse_id(playlist_id) { return 'playlist_collapse_' + playlist_id }
    function get_playlist_card_content_id(playlist_id) { return 'playlist_content_' + playlist_id }
    function get_playlist_card_with_id(playlist_id) { return $('#' + get_playlist_card_content_id(playlist_id)) }

    // code generators
    function createPlaylistCard(parent_id, playlist_id, header_content, collapse_content) {
        // This is create a single playlist item, fill with the given data. 
        var collapse_id = get_playlist_card_collapse_id(playlist_id)
        var heading_html = '<div class="card-header" role="tab" id="' + get_playlist_card_heading_id(playlist_id) +
            '"><h6 class="mb-0"><a class="text-secondary" data-toggle="collapse" onclick="controller.fillPlaylistCardWithSongs(\'' + playlist_id + '\')" href="#' + collapse_id +
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

    function addList(list_obj, content) {
        list_obj.append('<li>' + content + '</li>')
    }

    // state functions
    function resetView() {
        toggle_album_card(false)
        toggle_artist_card(false)
        toggle_song_card_album_sparator(false)
        toggle_album_artist_sparator(false)
        toggle_song_card_link_wp(false)
        toggle_song_card_link_wd(false)
        toggle_album_card_link_wp(false)
        toggle_album_card_link_wd(false)
        toggle_artist_card_link_wp(false)
        toggle_artist_card_link_wd(false)
        empty_song_card_info_list()
        empty_album_card_info_list()
        empty_artist_card_info_list()
        set_song_card_header('')
        set_song_card_title('')
        set_song_card_content('')
    }

    function spotifyLoading() {
        resetView()
        set_song_card_header('Betöltés...')
        set_song_card_title('A jelenleg hallgatott szám címe')
        set_album_cover_src(default_album_cover)
    }

    function wikidataLoading() {
        set_song_card_content('Itt fognak majd megjelenni az információk a kiválaszott számmal kapcsolatban.<br>Az adatok lekérése folyamatban...<br>')
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
        if (Object.keys(info['song']).length == 0 ) {
            if (Object.keys(info['album']).length == 0 && Object.keys(info['artist']).length == 0) {
                set_song_card_content('Sajnos nem található adat ehhez a számhoz.')
                return
            } else {
                set_song_card_content('Az album/előadó adatai alább láthatóak.')
            }
        }

        // fill song...
        if ('text' in info['song'])
            set_song_card_content(info['song']['text'])
        else
            set_song_card_content('')
        if ('release date' in info['song']) 
            addList(get_song_card_info_list(), 'Megjelenés éve: ' + (new Date(info['song']['release date']).getFullYear()))
        if ('genre' in info['song']) 
            addList(get_song_card_info_list(), 'Műfaj: ' + info['song']['genre'])
        if ('instrumentation' in info['song']) 
            addList(get_song_card_info_list(), 'Hangszerelés: ' + info['song']['instrumentation'])
        if ('lyrics_by' in info['song']) 
            addList(get_song_card_info_list(), 'Dalszöveg: ' + info['song']['lyrics_by'])
        if ('wiki' in info['song']) {
            set_song_card_link_wp(info['song']['wiki'])
            toggle_song_card_link_wp(true)
        }
        if ('id' in info['song']) {
            set_song_card_link_wd('https://www.wikidata.org/wiki/' + info['song']['id'])
            toggle_song_card_link_wd(true)
        }

        // fill album...
        if ('label' in info['album'] && Object.keys(info['album']).length > 1) {
            set_album_card_title('Album: ' + info['album']['label'])

            if ('text' in info['album'])
                set_album_card_content(info['album']['text'])
            if ('release date' in info['album']) 
                addList(get_album_card_info_list(), 'Megjelenés éve: ' + (new Date(info['album']['release date']).getFullYear()))
            if ('genre' in info['album']) 
                addList(get_album_card_info_list(), 'Műfaj: ' + info['album']['genre'])
            if ('producer' in info['album']) 
                addList(get_album_card_info_list(), 'Procuder: ' + info['album']['producer'])
            if ('wiki' in info['album']) {
                set_album_card_link_wp(info['album']['wiki'])
                toggle_album_card_link_wp(true)
            }
            if ('id' in info['album']) {
                set_album_card_link_wd('https://www.wikidata.org/wiki/' + info['album']['id'])
                toggle_album_card_link_wd(true)
            }

            toggle_song_card_album_sparator(true)
            toggle_album_card(true)
        }
        
        // fill artist...
        if ('label' in info['artist'] && Object.keys(info['artist']).length > 1) {
            set_artist_card_title('Előadó: ' + info['artist']['label'])

            if ('text' in info['artist'])
                set_artist_card_content(info['artist']['text'])
            if ('location' in info['artist']) 
                addList(get_artist_card_info_list(), 'Hely: ' + info['artist']['location'])
            if ('awards' in info['artist']) 
                addList(get_artist_card_info_list(), 'Díjak: ' + info['artist']['awards'])
            if ('inception' in info['artist']) 
                addList(get_artist_card_info_list(), 'Kezdés éve: ' + (new Date(info['artist']['inception']).getFullYear()))

            if ('wiki' in info['artist']) {
                set_artist_card_link_wp(info['artist']['wiki'])
                toggle_artist_card_link_wp(true)
            }
            if ('id' in info['artist']) {
                set_artist_card_link_wd('https://www.wikidata.org/wiki/' + info['artist']['id'])
                toggle_artist_card_link_wd(true)
            }

            toggle_album_artist_sparator(true)
            toggle_artist_card(true)
        }
    }

    return {
        spotifyLoading: spotifyLoading,
        wikidataLoading: wikidataLoading,
        displaySong: displaySong,
        displayPlaylistCards: displayPlaylistCards,
        displayPlaylistCardContent: displayPlaylistCardContent,
        displaySongInfo: displaySongInfo,
        spotifyError: function() {
            resetView()
            set_song_card_header('A Spotify nem éhető el!')
            set_song_card_title(':(')
        },
        wikidataError: function() {
            set_song_card_header('Valami gond volt a WikiData adatok lekérése közben...')
        },
        resetView: resetView,
    }
}
