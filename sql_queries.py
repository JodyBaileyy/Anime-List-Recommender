create_table_query = """
  CREATE TABLE IF NOT EXISTS watch_list 
    (
      id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
      title TEXT NOT NULL,
      media_id INTEGER NOT NULL,
      score INTEGER,
      status VARCHAR(50) NOT NULL
    );
"""

add_anime_query = """
  INSERT INTO watch_list (media_id, title, score, status)
  VALUES (?, ?, ?, ?);
"""

watch_list_query = "SELECT * FROM watch_list ORDER BY score DESC;"
update_query = "UPDATE watch_list SET {column} = ? WHERE id = ?;"
delete_query = "DELETE FROM watch_list WHERE id = ?;"