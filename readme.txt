📚 Libraries - 🖥️Frameworks utilized

- pip install python-pptx - PowerPoint file creation
- pip install secure-smtplib - Email service
- pip install flask - Web UI Framework
- pip install pandas - Data manipulation (csv files)
- pip install pandas openpyxl - Data manipulation (excel files)
- pip install fsspec - Data manipulation (excel files)

☁️ Azure integration steps

1-Go to Entra ID, and create a service principal
2-Go to "Certificates and secrets" and create an azure secret
3-Assign "Storage Blob Data Contributor" role to my service principal to manage containers
4-Store all your secrets in a .env variables
5-Install azure libraries - pip install azure-identity azure-mgmt-containerinstance
6-Go to azure service plans and create one
7-Go to azure services and create a web app
8-Set environment variables in azure
9-Create a storage account
10-Create blob storage
11-Copy access key from storage account
12-Set that key in the web app connection strings