from database import get_connection

def get_enrollments():
        conn = get_connection()
        cursor = conn.cursor()

        query = """
            SELECT *
            FROM takes
        """
        cursor.execute(query)
        results = cursor.fetchall()    
        
        return results
    
    
def add_enroll(id, course_id, sec_id, semester, year, grade):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        query = """
            INSERT INTO takes (id, course_id, sec_id, semester, year, grade) VALUES (%s, %s, %s, %s, %s, %s)
        """
        values = (id, course_id, sec_id, semester, year, grade)
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
        
        
def delete_enroll(id, course_id):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        query = """
            DELETE FROM takes
            WHERE id=%s AND course_id=%s
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
        
        
def update_enroll(id, course_id, grade):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        query = """
            UPDATE takes
            SET grade=%s
            WHERE id=%s AND course_id=%s
        """
        values = (grade, id, course_id)
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