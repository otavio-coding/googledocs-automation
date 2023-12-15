from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from datetime import date, datetime
import locale
import os
import csv
import time


def generate_files(recipient_sub):
    # Authenticates the app, see full documentation at https://developers.google.com/docs/api/quickstart/python?hl=pt-br
    SCOPES = ['https://www.googleapis.com/auth/documents', 'https://www.googleapis.com/auth/drive']
    DOCUMENT_ID = '1f4XmlfH5N1Cde2mhZPkEsQYAIRq6259AczLbvjz_q_0'
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

    try:
        # "service" is used to interact with google docs.
        service = build('docs', 'v1', credentials=creds)

        # Sets the language for the date format, here we're using Brazilian Portuguese (pt_BR).
        locale.setlocale(locale.LC_ALL, 'pt_BR')
        data_atual = date.today()
        data_value = data_atual.strftime("%d de %B de %Y")
        replacement_values = {}
        with open('RecipientsList.csv') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['SUBS'] == recipient_sub:
                    # Sets the replacement values, please adapt according to your CSV file and your placeholder file.
                    # The keys should be your placeholders and the values the corresponding data in the CSV.
                    replacement_values = {
                        "data": data_value,
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
        service.documents().batchUpdate(documentId=DOCUMENT_ID, body={'requests': requests}).execute()

        # "drive_service" is used to interact with google drive.
        drive_service = build('drive', 'v3', credentials=creds)

        # Downloads the PDF in the 'GeneratedDocs' folder.
        pdf_request = drive_service.files().export_media(fileId=DOCUMENT_ID, mimeType='application/pdf')
        pdf_file = pdf_request.execute()
        if pdf_file:
            with open('GeneratedDocs/' + recipient_sub + '-dec.pdf', 'wb') as output_file:
                output_file.write(pdf_file)
            print('File successfully generated for recipient: ' + recipient_sub)

            # Sets back the placeholders
            requests = []
            for field, value in replacement_values.items():
                requests.append({'replaceAllText': {'containsText': {'text': value, 'matchCase': 'true'},
                                                    'replaceText': '[{}]'.format(field)}})
            service.documents().batchUpdate(documentId=DOCUMENT_ID, body={'requests': requests}).execute()
            time.sleep(2)
        else:
            print('Error: Failed to export the document as PDF.')

    except HttpError as err:
        print(err)


def main():
    start_time = time.time()  # Record the start time

    with open('RecipientsList.csv') as file:
        reader = csv.DictReader(file)
        next(reader)
        for row in reader:
            generate_files(row["SUBS"])

    end_time = time.time()  # Record the end time
    elapsed_time = end_time - start_time
    print(f"Total execution time: {elapsed_time} seconds")


if __name__ == '__main__':
    main()
