import sqlite3

def create_db_schema(db_schema: dict):
    """Create db schema"""
    con = sqlite3.connect(":memory:")

    sql_script = db_schema["sql_script"]

    cursor = con.cursor()
    cursor.execute(sql_script)

    return {"response": "successfully created schema"}
