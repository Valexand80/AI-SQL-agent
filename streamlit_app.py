import streamlit as st
import pandas as pd
import pymysql
import re
from openai import OpenAI
from dotenv import load_dotenv
import os

# Load OpenAI key
load_dotenv("agent.env")
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# --- SQL agent function ---
def ask_sql_question(user_question, schema_context):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that writes SQL queries for a MySQL database."},
                {"role": "user", "content": f"{schema_context}\nConvert this request into SQL: {user_question}"}
            ]
        )

        full_response = response.choices[0].message.content.strip()
        match = re.search(r"```sql\n(.*?)```", full_response, re.DOTALL)
        generated_sql = match.group(1).strip() if match else full_response

        conn = pymysql.connect(
            host=os.getenv("MYSQL_HOST"),
    	    port=int(os.getenv("MYSQL_PORT")),
            user=os.getenv("MYSQL_USER"),
            password=os.getenv("MYSQL_PASSWORD"),
            database=os.getenv("MYSQL_DATABASE")
            connect_timeout=5
        )

        cursor = conn.cursor()
        cursor.execute(generated_sql)
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        cursor.close()
        conn.close()

        df = pd.DataFrame(rows, columns=columns)
        return generated_sql, df

    except Exception as e:
        return None, f"❌ Error: {str(e)}"


# --- Streamlit UI ---
st.title("Natural Language SQL AI Agent")

# Text input
user_question = st.text_input("Ask a question about your database:")

# Run button
if st.button("Run Query") and user_question.strip():
    schema_context = """
    You are working with a MySQL database called 'us_project' that contains the following tables:

    us_household_income:
  - row_id (int)
  - id (int)
  - State_Code (int)
  - State_Name (text)
  - State_ab (text)
  - County (text)
  - City (text)
  - Place (text)
  - Type (text)
  - Primary (text)
  - Zip_Code (int)
  - Area_Code (int)
  - ALand (int)
  - AWater (int)
  - Lat (double)
  - Lon (double)


us_household_income_statistics:
  - id (int)
  - State_Name (text)
  - Mean (int)
  - Median (int)
  - Stdev (int)
  - sum_w (double)

water_content_view:
  - State_Name (text)
  - City (text)
  - County (text)
  - ALand (int)
  - AWater (int)
  - Total_area (bigint)
  - WaterPercent (decimal)
  - Water_content (varchar)
    """

    sql, result = ask_sql_question(user_question, schema_context)

    if isinstance(result, pd.DataFrame):
        st.code(sql, language="sql")
        st.dataframe(result)
    else:
        st.error(result)
