import pandas as pd

def read_excel_to_dataframe(file_path):
    """
    Reads an Excel file and converts it into a Pandas DataFrame,
    automatically detecting column headers.
    Returns the DataFrame.
    """
    try:
        df = pd.read_excel(file_path, sheet_name=0)  # Reads the first sheet by default
        return df
    except Exception as e:
        print(f"Error reading Excel file: {e}")
        return None

def display_dataframe(df):
    """
    Displays the DataFrame.
    """
    if df is not None:
        print(df)  # Display all rows
    else:
        print("Failed to load DataFrame.")

import pandas as pd

def compare_dataframes(excel_df, sql_df):
    """
    Compares two DataFrames based on the combination of NME_TABLE and NME_COLUMN.
    Prints differences and extra rows in the specified format.
    
    Parameters:
        excel_df (pd.DataFrame): The first DataFrame (Excel data).
        sql_df (pd.DataFrame): The second DataFrame (SQL data).
    """
    # Step 1: Map columns
    excel_df_mapped = excel_df.rename(columns={
        "NME_TBL": "NME_TABLE",
        "NME_SCHM": "NME_SCHEMA",
        "NME_DB": "NME_DATABASE",
        "NME_CLMN": "NME_COLUMN"
    })[["NME_TABLE", "NME_SCHEMA", "NME_DATABASE", "IDN_EON", "NME_COLUMN"]]

    sql_df_mapped = sql_df.rename(columns={
        "NME_TABLE": "NME_TABLE",
        "NME_SCHEMA": "NME_SCHEMA",
        "NME_DATABASE": "NME_DATABASE",
        "NME_COLUMN": "NME_COLUMN"
    })[["NME_TABLE", "NME_SCHEMA", "NME_DATABASE", "IDN_COLUMN", "NME_COLUMN"]]

    # Rename IDN_COLUMN to IDN_EON for consistency
    sql_df_mapped = sql_df_mapped.rename(columns={"IDN_COLUMN": "IDN_EON"})

    # Step 2: Compare based on NME_TABLE + NME_COLUMN combination
    merged_df = pd.merge(
        excel_df_mapped, sql_df_mapped,
        on=["NME_TABLE", "NME_COLUMN"], how="outer", suffixes=("_excel", "_sql")
    )

    # Step 3: Identify differences
    differences = []
    extra_in_excel = []
    extra_in_sql = []

    for _, row in merged_df.iterrows():
        if pd.isna(row["IDN_EON_excel"]) and not pd.isna(row["IDN_EON_sql"]):
            # Extra row in SQL
            extra_in_sql.append(row[["NME_TABLE", "NME_SCHEMA_sql", "NME_DATABASE_sql", "IDN_EON_sql", "NME_COLUMN"]])
        elif pd.isna(row["IDN_EON_sql"]) and not pd.isna(row["IDN_EON_excel"]):
            # Extra row in Excel
            extra_in_excel.append(row[["NME_TABLE", "NME_SCHEMA_excel", "NME_DATABASE_excel", "IDN_EON_excel", "NME_COLUMN"]])
        else:
            # Check for differences in other columns
            diff_cols = []
            if row["NME_SCHEMA_excel"] != row["NME_SCHEMA_sql"]:
                diff_cols.append("NME_SCHEMA")
            if row["NME_DATABASE_excel"] != row["NME_DATABASE_sql"]:
                diff_cols.append("NME_DATABASE")
            if row["IDN_EON_excel"] != row["IDN_EON_sql"]:
                diff_cols.append("IDN_EON")

            if diff_cols:
                differences.append({
                    "combination": (row["NME_TABLE"], row["NME_COLUMN"]),
                    "diff_cols": "|".join(diff_cols),
                    "excel_values": row[["NME_TABLE", "NME_COLUMN", "NME_SCHEMA_excel", "NME_DATABASE_excel", "IDN_EON_excel"]],
                    "sql_values": row[["NME_TABLE", "NME_COLUMN", "NME_SCHEMA_sql", "NME_DATABASE_sql", "IDN_EON_sql"]]
                })

    # Step 4: Print results
    if differences:
        print("df,df_columns with differences:NME_TABLE,NME_COLUMN,NME_SCHEMA,NME_DATABASE,IDN_EON")
        for diff in sorted(differences, key=lambda x: x["combination"]):
            print(f"excel_df,{diff['diff_cols']},{','.join(map(str, diff['excel_values']))}")
            print(f"sql_df,{diff['diff_cols']},{','.join(map(str, diff['sql_values']))}")

    if extra_in_sql:
        print(f"\nExtra {len(extra_in_sql)} rows in sql_df:")
        extra_sql_df = pd.DataFrame(extra_in_sql)
        print(extra_sql_df.to_string(index=False))

    if extra_in_excel:
        print(f"\nExtra {len(extra_in_excel)} rows in excel_df:")
        extra_excel_df = pd.DataFrame(extra_in_excel)
        print(extra_excel_df.to_string(index=False))


# Example usage
file_path = "a1.xlsx"  # Change this to the actual file path
excel_df = read_excel_to_dataframe(file_path)
sql_df = read_excel_to_dataframe("b1.xlsx")  # Assuming SQL data is in another Excel file

compare_dataframes(excel_df, sql_df)
