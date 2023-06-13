# google sheets data retrieval

from auth import get_service


# retrieve sheet data by sheet id
def retrieve_sheets_data(sheetId, formType = 'committee'):

    service = get_service(api_name='sheets',api_version='v4',)

    ranges = 'r2c1:r100c15'  #specify the fields range

    response = service.spreadsheets().values().batchGet(
            spreadsheetId=sheetId, ranges=ranges, majorDimension='ROWS').execute()

    result = {}

    for temp in response['valueRanges']:
        if 'values' not in temp:
            return {}

        result['data'].append(temp)
    return result