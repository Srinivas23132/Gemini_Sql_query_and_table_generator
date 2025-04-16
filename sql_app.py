import os
import streamlit as st
import sqlite3
from dotenv import load_dotenv
import google.generativeai as genai
import pandas as pd

# Load environment variables from .env file
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    st.error("GOOGLE_API_KEY not found in .env file. Please add it.")
    st.stop()

# Configure the Gemini API key
genai.configure(api_key=GOOGLE_API_KEY)

# Initialize the Gemini model (using gemini-2.0-flash)
try:
    model = genai.GenerativeModel('gemini-2.0-flash')
except Exception as e:
    st.error(f"Error initializing the Gemini model: {e}")
    st.stop()

def clean_sql_query(raw_query: str) -> str:
    """
    Remove markdown code fences and unwanted characters from the generated SQL queries.
    """
    # Remove common markdown code fence markers
    cleaned = raw_query.replace("```sql", "").replace("```", "").strip()
    return cleaned

def parse_multiple_queries(raw_output: str) -> list:
    """
    Split the provided raw output into individual SQL queries,
    filtering out comment lines.
    Assumes each valid SQL statement is terminated by a semicolon.
    """
    cleaned_output = clean_sql_query(raw_output)
    # Remove comment lines (lines starting with --)
    filtered_lines = []
    for line in cleaned_output.splitlines():
        if not line.strip().startswith("--"):
            filtered_lines.append(line)
    filtered_text = "\n".join(filtered_lines)
    # Split by semicolon; ignore empty strings.
    queries = [q.strip() for q in filtered_text.split(";") if q.strip()]
    return queries

def generate_sql_queries(natural_language_query: str) -> str:
    """
    Generate multiple SQL queries based on the user's natural language request.
    The prompt instructs the model to return queries (each ending with a semicolon).
    """
    prompt = f"""
You are an expert at converting natural language into SQL queries.
The database schema is as follows:

1. BRANCH(Branch_ID TEXT PRIMARY KEY, Branch_Location TEXT, Contact_No TEXT)
2. CUSTOMER(Customer_Name TEXT, Customer_Address TEXT, Email TEXT, Contact_No NUMBER PRIMARY KEY)
3. COURIER(Courier_Id TEXT PRIMARY KEY, From_Address TEXT, To_Address TEXT, Branch_ID TEXT, Booking_Date DATE, Expected_Delivery_Date DATE, Weight REAL, Cost REAL, Contact_No TEXT)
4. COURIER_STATUS(Courier_Id TEXT, Status TEXT, Remarks TEXT, Actual_Delivered_date DATE, Delivered_Branch_ID TEXT)

Relationships:
- CUSTOMER.Contact_No is a foreign key in COURIER(Contact_No)
- BRANCH.Branch_ID is a foreign key in COURIER(Branch_ID)
- COURIER.Courier_Id is a foreign key in COURIER_STATUS(Courier_Id)
- BRANCH.Branch_ID is also a foreign key in COURIER_STATUS(Delivered_Branch_ID)

Based on the following user request, generate a list of SQL queries.
Do not execute any queries by default; only generate the queries. 
If the user's request includes insertion of sample data, include INSERT statements,
and also include SELECT statements to print out full table contents.
Please return your answer as plain SQL with each query terminated by a semicolon.
User Request: "{natural_language_query}"
"""
    try:
        response = model.generate_content(prompt)
        return clean_sql_query(response.text)
    except Exception as e:
        st.error(f"Error generating SQL queries: {e}")
        return None

def execute_multiple_queries(multi_query: str) -> dict:
    """
    Execute each individual query on the 'courier.db' database.
    A single connection is maintained for the entire execution block to avoid locking issues.
    For SELECT queries, the function fetches and returns the results in a DataFrame.
    Returns a dictionary mapping each query label to its result or status.
    """
    queries = parse_multiple_queries(multi_query)
    results = {}
    conn = sqlite3.connect('courier.db')
    cursor = conn.cursor()
    try:
        for i, query in enumerate(queries, start=1):
            try:
                if query.strip().upper().startswith("SELECT"):
                    cursor.execute(query)
                    rows = cursor.fetchall()
                    # Handle the case where there might be no data returned.
                    if cursor.description:
                        columns = [desc[0] for desc in cursor.description]
                        results[f"Query {i} (SELECT)"] = pd.DataFrame(rows, columns=columns)
                    else:
                        results[f"Query {i} (SELECT)"] = pd.DataFrame()
                else:
                    cursor.execute(query)
                    results[f"Query {i} (Non-SELECT)"] = "Executed successfully."
            except Exception as ex:
                results[f"Query {i}"] = f"Error: {ex}"
        conn.commit()
    finally:
        conn.close()
    return results

# Streamlit UI
st.title("📦 Courier Management: Multi-Query Executor")
st.markdown("""
Enter a natural language request to generate multiple SQL queries.
For example:
- *"Insert random data into all tables and then print the contents of all tables."*
- *"Display all customers and the couriers they have booked, along with branch details."*
""")

user_input = st.text_input("🔍 Enter your request:")

if st.button("Submit"):
    if user_input:
        with st.spinner("Generating SQL queries using Gemini..."):
            raw_queries = generate_sql_queries(user_input)
            if raw_queries:
                st.subheader("🧠 Generated SQL Queries:")
                queries = parse_multiple_queries(raw_queries)
                for i, query in enumerate(queries, start=1):
                    st.markdown(f"**Query {i}:**")
                    st.code(query, language='sql')
                st.markdown("---")
                with st.spinner("Executing queries..."):
                    execution_results = execute_multiple_queries(raw_queries)
                    for label, result in execution_results.items():
                        st.markdown(f"**Result for {label}:**")
                        if isinstance(result, pd.DataFrame):
                            if result.empty:
                                st.info("Empty result.")
                            else:
                                st.dataframe(result)
                        else:
                            st.text(result)
            else:
                st.error("Failed to generate SQL queries. Please refine your request.")
    else:
        st.warning("Please enter a natural language request.")
