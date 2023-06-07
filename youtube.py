import auth


def fetch_playlist(playlistId, nextPageToken = ''):
    service = auth.get_service(api_name='youtube',api_version='v3',scopes=["https://www.googleapis.com/auth/youtube.readonly"])

    response = service.playlistItems().list(
        part="snippet",  #options={id, }
        maxResults=10,
        playlistId=playlistId,
        pageToken=nextPageToken
    ).execute()
    array = []
    # print(response)
    for eachContent in response['items']:
        # print(i['snippet']['title'])
        snippet = eachContent['snippet']
        array.append({
            'id': snippet['resourceId']['videoId'],
            'title':snippet['title'],
            # 'description':snippet['description'],
            'thumbnail': snippet['thumbnails']['default']['url'],
            'url': 'https://www.youtube.com/watch?v=' + snippet['resourceId']['videoId'] + '&list=' + snippet['playlistId'],
            'player': 'http://www.youtube.com/embed/' + snippet['resourceId']['videoId'],
            })
    array.append({'nextToken': ('/' + response['nextPageToken'] if 'nextPageToken' in response else '')})
    return array

# print(fetch_playlist("PLbpi6ZahtOH6G_A4_RLzzqdVf4TG5ilzf"))