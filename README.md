# Script de Automação Google Docs

Este é um script Python projetado para automatizar a substituição de campos em um documento específico no Google Docs. Ele utiliza a API do Google Docs e do Google Drive para realizar tarefas como a substituição de texto, exportação do documento modificado como um arquivo PDF e restauração do documento à sua forma original. Abaixo estão as principais funcionalidades e instruções de uso:

## Pré-requisitos
Antes de executar o script, certifique-se de ter realizado as seguintes etapas:

1. Siga o guia de [início rápido da API do Google Docs em Python](https://developers.google.com/docs/api/quickstart/python?hl=pt-br) para configurar as credenciais de API e salve o arquivo `credentials.json`.

2. Defina o ID do documento Google a ser processado em `DOCUMENT_ID`.

3. Garanta que a biblioteca necessária esteja instalada usando o seguinte comando:

   ```bash
   pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client


## Uso

1. Ao executar o script, será solicitada o id da linha do CSV com os dados que serão usados. Insira o valor desejado.

2. O script lê um arquivo CSV, nesse caso AlunosAtivos.csv, para obter informações do aluno com base na subscrição fornecida.

3. Os dados do aluno são substituídos nos marcadores correspondentes no documento Google usando a API do Google Docs.

4. O documento é exportado como um arquivo PDF no Google Drive, e o arquivo resultante é salvo localmente.

5. Após a exportação, os marcadores no documento são revertidos à forma original.

6. O progresso e eventuais erros são exibidos no console.

Observação: Certifique-se de que as permissões adequadas foram concedidas à conta associada às credenciais para acessar e modificar o documento e exportar o arquivo PDF.

Aviso: Este script opera em documentos específicos e depende de dados estruturados no arquivo CSV. Certifique-se de fornecer os caminhos corretos para os arquivos e personalizar conforme necessário.

Esperamos que este script facilite suas tarefas de automação no ambiente Google Docs. Feliz automação! 🚀🎉
