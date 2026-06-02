from database import get_connection

def get_teaches():
        conn = get_connection()
        cursor = conn.cursor()

        query = """
            SELECT *
            FROM teaches
        """
        cursor.execute(query)
        results = cursor.fetchall()    
        
        return results
    
    
def add_teaches(id, course_id, sec_id, semester, year):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        query = """
            INSERT INTO teaches (id, course_id, sec_id, semester, year) VALUES (%s, %s, %s, %s, %s)
        """
        values = (id, course_id, sec_id, semester, year)
        cursor.execute(query, values)
        
        conn.commit()
        
        if cursor.rowcount <= 0:
            return False
        return True
        
    except Exception as e:
        print(e)
        conn.rollback()
    finally:
        cursor.close()
        conn.close()
        
        
def delete_teaches(id, course_id):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        query = """
            DELETE FROM teaches
            WHERE id=%s AND course_id = %s
        """
        values = (id, course_id)
        cursor.execute(query, values)
        
        conn.commit()
                
        if cursor.rowcount <= 0:
            return False
        return True
        
    except Exception as e:
        print(e)
        conn.rollback()
    finally:
        cursor.close()
        conn.close()
        

def search_teaches_by_instructor(ins_id):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        query = """
            SELECT * 
            FROM teaches 
            WHERE id = %s
        """
        cursor.execute(query, (ins_id,))
        results = cursor.fetchall()
        
        return results
    except Exception as e:
        print(e)
        return []
    finally:
        cursor.close()
        conn.close()