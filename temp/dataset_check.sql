select compositions.title as song, albums.title as album, artists.name as artist from albums
inner join album_comp_links on albums.album_id = album_comp_links.album_id
inner join compositions on compositions.composition_id = album_comp_links.composition_id
inner join artists on compositions.artist_id = artists.artist_id




select unnest(array[1, 2, 3]), unnest(array[4, 5, 6, 7])