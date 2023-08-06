from motordecalidad.constants import *
from pyspark.sql import DataFrame
def send_email(receiver_email):
    import smtplib, ssl
    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    sender_email = "motordecalidadtlfhispan@gmail.com"
    password = "motordecalidad123"
    message = """\
    Subject: Reporte de Calidad
    Se han encontrado errores que superan los limites establecidos en la validación de calidad"""
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)
#Function to define the dbutils library from Azure Databricks
def get_dbutils(spark):
        try:
            from pyspark.dbutils import DBUtils
            dbutils = DBUtils(spark)
        except ImportError:
            import IPython
            dbutils = IPython.get_ipython().user_ns["dbutils"]
        return dbutils
def applyFilter(object:DataFrame, filtered) :
    try:
        filteredColumn = filtered.get(JsonParts.Fields)
        filterValue = filtered.get(JsonParts.Values)
        print("Extracción de parametros de filtrado finalizada")
        return object.filter(col(filteredColumn)==filterValue)
    except:
        print("Se omite filtro")
        return object