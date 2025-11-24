import sqlite3
from google.adk.tools import ToolContext

_connection = sqlite3.connect(":memory:", check_same_thread=False)
_cursor = _connection.cursor()

def db_interactions(sql_command: str):
    """
    Execute SQL commands within an in-memory SQLite database.
    Handles schema creation, data manipulation, and querying.
    """

    try:
        _cursor.execute(sql_command) if sql_command.find(";") == 1 else _cursor.executescript(sql_command)
        if sql_command.strip().lower().startswith("select"):
            rows = _cursor.fetchall()
            return {"response": "query executed successfully", "rows": rows}
        else:
            _connection.commit()
            return {"response": "successfully executed command"}
    except Exception as e:
        return {"response": "error", "details": str(e)}