import urllib

params = urllib.parse.quote_plus(r'Driver={ODBC Driver 18 for SQL Server};Server=tcp:travel-api.database.windows.net,1433;Database=travel_api;Uid=travel-apiadmin;Pwd=Trvl123!;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;')
conn_str = 'mssql+pyodbc:///?odbc_connect={}'.format(params)

class Config:
    SECRET_KEY = 'very_secret_key'
    SQLALCHEMY_DATABASE_URI = conn_str
    SQLALCHEMY_TRACK_MODIFICATIONS = False