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


def main():
    # Autentica o app, ver documentação da API em https://developers.google.com/docs/api/quickstart/python?hl=pt-br
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
        # Cria o objeto "service" que é a interface que usada para interagir com o google docs.
        service = build('docs', 'v1', credentials=creds)

        # Usa o input do usuário para buscar os valores para substituição na base de dados.
        subnum = input('Informe a subscrição do aluno: ')
        locale.setlocale(locale.LC_ALL, 'pt_BR')
        data_atual = date.today()
        data_value = data_atual.strftime("%d de %B de %Y")
        valores_de_substituicao = {}
        with open('AlunosAtivos.csv') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['SUBS'] == subnum:
                    valores_de_substituicao = {
                        "data": data_value,
                        "nome": row['NOME'],
                        "rg": row['RG'],
                        "cpf": row['CPF'],
                        "data_inicio": datetime.strptime(row['DATA'], '%Y-%m-%d').strftime('%d/%m/%Y')
                    }

        # Constrói a solicitação de substituição de valores do documento que está no Drive.
        requests = []
        for field, value in valores_de_substituicao.items():
            requests.append({'replaceAllText': {'containsText': {'text': '[{}]'.format(field), 'matchCase': 'true'},
                                                'replaceText': value}})

        # Executa a solicitação de substituição de valores.
        service.documents().batchUpdate(documentId=DOCUMENT_ID, body={'requests': requests}).execute()

        print('Campos alterados com sucesso.')

        # Cria o objeto "drive_service" que é a interface que usada para interagir com o google drive.
        drive_service = build('drive', 'v3', credentials=creds)

        # Exporta o doc como PDF e faz o download.
        pdf_request = drive_service.files().export_media(fileId=DOCUMENT_ID, mimeType='application/pdf')
        pdf_file = pdf_request.execute()
        if pdf_file:
            with open(subnum + '-dec.pdf', 'wb') as output_file:
                output_file.write(pdf_file)
            print('Documento exportado com sucesso.')

            # Reverte o documento para a forma original com os campos vazios
            requests = []
            for field, value in valores_de_substituicao.items():
                requests.append({'replaceAllText': {'containsText': {'text': value, 'matchCase': 'true'},
                                                    'replaceText': '[{}]'.format(field)}})
            service.documents().batchUpdate(documentId=DOCUMENT_ID, body={'requests': requests}).execute()
            time.sleep(2)
            print('Documento original restaurado.')
        else:
            print('Error: Failed to export the document as PDF.')

    except HttpError as err:
        print(err)


if __name__ == '__main__':
    main()
