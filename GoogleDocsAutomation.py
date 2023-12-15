from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
# from googleapiclient.errors import HttpError
import concurrent.futures


from datetime import date, datetime
import locale
import os
import csv
import time


def google_auth():
    """Authenticates the app, see full documentation at
    https://developers.google.com/docs/api/quickstart/python?hl=pt-br"""

    SCOPES = ['https://www.googleapis.com/auth/documents', 'https://www.googleapis.com/auth/drive']
    creds = None

    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds


def today_date_string(language, string_format):
    """Creates a string using the language stated as first parameter and the format in second parameter
    If you call today_date_string(en_US, %B d% Y%) it returns 'Month dd yyyy', e.g November 11 2023"""
    # Sets the language for the date format, here we're using Brazilian Portuguese (pt_BR).
    locale.setlocale(locale.LC_ALL, language)
    current_date = date.today()
    return current_date.strftime(string_format)


def create_copy(template_id, drive_service):
    """Creates a copy of the file which ID was passed as first parameter and returns the ID of the copy."""

    copy_title = 'Copy Title'
    body = {
        'name': copy_title
    }
    drive_response = drive_service.files().copy(
        fileId=template_id, body=body).execute()
    copy_id = drive_response.get('id')
    return copy_id


def generate_file(row):
    global creds
    # Starts a service with Google Docs and Google Drive.
    docs_service = build('docs', 'v1', credentials=creds)
    drive_service = build('drive', 'v3', credentials=creds)

    template_id = '1f4XmlfH5N1Cde2mhZPkEsQYAIRq6259AczLbvjz_q_0'
    copy_id = create_copy(template_id, drive_service)

    replacement_values = {
        "data": today_date_string('pt_BR', '%d de %B de %Y'),
        "nome": row['NAME'],
        "rg": row['RG'],
        "cpf": row['CPF'],
        "data_inicio": datetime.strptime(row['DATE'], '%Y-%m-%d').strftime('%d/%m/%Y')
    }

    # Builds the request to substitute the placeholders, e.g. [name] becomes 'John Doe'.
    requests = []
    for field, value in replacement_values.items():
        requests.append({'replaceAllText': {'containsText': {'text': '[{}]'.format(field), 'matchCase': 'true'},
                                            'replaceText': value}})
    docs_service.documents().batchUpdate(documentId=copy_id, body={'requests': requests}).execute()

    # Downloads the PDF in the 'GeneratedDocs' folder.
    pdf_request = drive_service.files().export_media(fileId=copy_id, mimeType='application/pdf')
    pdf_file = pdf_request.execute()
    if pdf_file:
        with open('GeneratedDocs/' + row['SUBS'] + '-dec.pdf', 'wb') as output_file:
            output_file.write(pdf_file)
        print('File successfully generated for recipient: ' + row['SUBS'])
    else:
        print('Error: Failed to export the document as PDF.')

    drive_service.files().delete(fileId=copy_id).execute()


def main():
    start_time = time.time()  # Record the start time

    with open('RecipientsList.csv') as file:
        reader = csv.DictReader(file)
        rows = list(reader)
        print(len(rows))

    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(generate_file, rows)

    end_time = time.time()  # Record the end time
    elapsed_time = end_time - start_time
    print(f"Total execution time: {elapsed_time} seconds")


creds = google_auth()


if __name__ == '__main__':

    main()
