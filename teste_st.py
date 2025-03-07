import streamlit as st
import pandas as pd
import boto3
import time

# Define AWS credentials and other configuration variables
S3_STAGING_DIR = "s3://hubii-data-lakehouse/temp"
AWS_ACCESS_KEY = "AKIA2VVGSYJZ5XP4EXO4"
AWS_SECRET_KEY = "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"
SCHEMA_NAME = "default"
AWS_REGION = "us-east-1"

# Initialize Athena client
athena_client = boto3.client(
    "athena",
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    region_name=AWS_REGION,
)

# Start the query execution
query_response = athena_client.start_query_execution(
    QueryString="SELECT * FROM silver.order_hub_sent limit 10",
    QueryExecutionContext={"Database": SCHEMA_NAME},
    ResultConfiguration={
        "OutputLocation": S3_STAGING_DIR,
        "EncryptionConfiguration": {"EncryptionOption": "SSE_S3"},
    },
)

# Wait for the query to finish executing
while True:
    try:
        result = athena_client.get_query_results(
            QueryExecutionId=query_response["QueryExecutionId"]
        )
        if result["ResultSet"]["Rows"]:
            break
    except Exception as err:
        if "not yet finished" in str(err):
            time.sleep(0.001)
        else:
            raise err

# Extract the column names
columns = [col["Label"] for col in result["ResultSet"]["ResultSetMetadata"]["ColumnInfo"]]

# Extract the rows and handle different data types
rows = result["ResultSet"]["Rows"]
data = []
for row in rows[1:]:  # Skip the header row
    data_row = []
    for col in row["Data"]:
        # Check for different possible data types in Athena results
        if "VarCharValue" in col:
            data_row.append(col["VarCharValue"])
        elif "IntegerValue" in col:
            data_row.append(int(col["IntegerValue"]))
        elif "DoubleValue" in col:
            data_row.append(float(col["DoubleValue"]))
        else:
            data_row.append(None)  # Handle None/empty data
    data.append(data_row)

# Convert the data to a Pandas DataFrame
df = pd.DataFrame(data, columns=columns)

st.set_page_config(layout="wide")
# Título do Dashboard
st.title('Dashboard do Edu Máquina')
# Filtros
st.sidebar.header('Filtros')
search_id_filter=True
# Aplicar filtros
if search_id_filter:
    # Criação das abas
    tab1, tab2, tab3 = st.tabs(["Perfil da Busca", "Ranking de Engajamento", "Engajamento por Sub-Temas"])
    with tab1:
        st.header("Perfil da Busca")
        col1, col2 = st.columns([0.4, 0.6], gap="large")
        with col1:
            st.subheader('Aspectos semânticos...')
        
        with col2:
            st.subheader('Grandes números...')
    with tab2:
        st.header("Ranking de Engajamento")
        st.subheader("Dados Detalhados dos Vídeos")
        st.dataframe(df)
    with tab3:
        st.header("Engajamento por Sub-Temas")
        
        # Seleção entre temas pais e temas filhos
        theme_type = st.selectbox('Selecione o tipo de tema', ['Temas Pais', 'Temas Filhos'])
