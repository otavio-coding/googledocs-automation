# Google Docs Automation Script

This is a Python script designed to automate field replacement in a specific document on Google Docs. It uses the Google Docs and Google Drive API to perform tasks such as text replacement, exporting the modified document as a PDF file, and restoring the document to its original form. Below are the main features and usage instructions:

## Example:
Google Doc whose ID was passed as DOCUMENT_ID within the code:

"The student **[name]** registered under the **SIN number [sin]** and **ID [id]** is enrolled in this school."

Generated PDF:

"The student **Jhon Doe** registered under the **SIN number 123.456.789-11** and **ID 12.345.678-9** is enrolled in this school."

## Prerequisites
Before running the script, make sure you have completed the following steps:

1. Follow the [Google Docs API Quickstart guide in Python](https://developers.google.com/docs/api/quickstart/python?hl=en) to set up API credentials and save the `credentials.json` file.

2. Set the Google Document ID to be processed in `DOCUMENT_ID`.

3. Ensure that the required library is installed using the following command:

   ```bash
   pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client


## Usage

1. When running the script, it reads a CSV file row by row, in this case, RecipientsList.csv, to obtain recipient's information..

2. Recipient data is replaced in the corresponding placeholders in the Google document using the Google Docs API.

3. The document is exported as a PDF file on Google Drive, and the resulting file is saved locally in a folder called "GeneratedDocs".

4. After the export, the placeholders in the document are reverted to their original form.

5. Progress and any errors are displayed in the console.

Note: Ensure that the appropriate permissions have been granted to the account associated with the credentials to access and modify the document and export the PDF file.

Warning: This script operates on specific documents and depends on structured data in the CSV file. Ensure that you provide the correct paths to the files and customize as needed.

We hope this script streamlines your automation tasks in the Google Docs environment. Happy automation! 🚀🎉
