import sqlite3
import json
from models import Entry, Mood, Tag

def get_all_entries():
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:

        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            e.id,
            e.concept,
            e.entry,
            e.date,
            e.mood_id,
            m.id,
            m.label
        FROM entries e
        JOIN moods m
        ON m.id = e.mood_id
        """)
        
        entries = []

        dataset = db_cursor.fetchall()

        for row in dataset:

            # Create an entry instance from the current row.
            # Note that the database fields are specified in
            # exact order of the parameters defined in the
            # entry class above.
            entry = Entry(row['id'], row['concept'], row['entry'], row['date'], row['mood_id'])
            mood = Mood(row['mood_id'], row['label'])
            
            entry.mood = mood.__dict__
            entries.append(entry.__dict__)
            
            db_cursor.execute("""
               select t.id, t.tag
               from entry_tags en
               join tags t on t.id = en.tag_id
               where en.entry_id = ?
            """, (entry.id, ))
            
            tags = []
            
            tag_dataset = db_cursor.fetchall()
            
            for tag_row in tag_dataset:
                tag = Tag(tag_row['id'], tag_row['tag'])
                tags.append(tag.__dict__)
                
            entry.tags = tags

    # Use `json` package to properly serialize list as JSON
    return json.dumps(entries)

def get_single_entry(id):
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Use a ? parameter to inject a variable's value
        # into the SQL statement.
        db_cursor.execute("""
        SELECT
            e.id,
            e.concept,
            e.entry,
            e.date,
            e.mood_id
        FROM entries e
        WHERE e.id = ?
        """, ( id, ))

        # Load the single result into memory
        data = db_cursor.fetchone()

        # Create an entry instance from the current row
        entry = Entry(data['id'], data['concept'], data['entry'],
                            data['date'], data['mood_id'])

    return json.dumps(entry.__dict__)
    
def delete_entry(id):
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        DELETE FROM entries
        WHERE id = ?
        """, (id, ))
        
def search_entries(value):
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:

        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        
        db_cursor.execute("""
        SELECT
            e.id,
            e.concept,
            e.entry,
            e.date,
            e.mood_id
        FROM entries e
        WHERE entry LIKE ?
        """, ('%'+value+'%', ))

        entries = []

        dataset = db_cursor.fetchall()

        for row in dataset:

            # Create an entry instance from the current row.
            # Note that the database fields are specified in
            # exact order of the parameters defined in the
            # entry class above.
            entry = Entry(row['id'], row['concept'], row['entry'], row['date'], row['mood_id'])

            entries.append(entry.__dict__)

    # Use `json` package to properly serialize list as JSON
    return json.dumps(entries)

def create_entry(new_entry):
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO entries
            ( concept, entry, date, mood_id )
        VALUES
            ( ?, ?, ?, ? );
        """, (new_entry['concept'], new_entry['entry'],
              new_entry['date'], new_entry['mood_id'] ))

        id = db_cursor.lastrowid
        new_entry['id'] = id
        
        
        for tag in new_entry['tags']:
            db_cursor.execute("""
            INSERT INTO entry_tags
                ( tag_id, entry_id )
            VALUES 
                ( ?, ? );
            """, (tag, new_entry['id']))


    return json.dumps(new_entry)

def update_entry(id, new_entry):
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        UPDATE entries
            SET
                concept = ?,
                entry = ?,
                date = ?,
                mood_id = ?
        WHERE id = ?
        """, (new_entry['concept'], new_entry['entry'],
              new_entry['date'], new_entry['mood_id'], id, ))

        # Were any rows affected?
        # Did the client send an `id` that exists?
        rows_affected = db_cursor.rowcount

    if rows_affected == 0:
        # Forces 404 response by main module
        return False
    else:
        # Forces 204 response by main module
        return True
