import auth


def fetch_playlist(playlistId):
    service = auth.get_service(api_name='youtube',api_version='v3',scopes=["https://www.googleapis.com/auth/youtube.readonly"])

    response = service.playlistItems().list(
        part="snippet",
        maxResults=10,
        playlistId=playlistId
    ).execute()
    array = []
    for eachContent in response['items']:
        # print(i['snippet']['title'])
        snippet = eachContent['snippet']
        array.append({
            'title':snippet['title'],
            # 'description':snippet['description'],
            'thumbnail': snippet['thumbnails']['default']['url'],
            'url': 'https://www.youtube.com/watch?v=' + snippet['resourceId']['videoId'] + '&list=' + snippet['playlistId']
            })
    array.append({'nextToken': response['nextPageToken']})
    return array

# print(fetch_playlist("PLbpi6ZahtOH6G_A4_RLzzqdVf4TG5ilzf"))