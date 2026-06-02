from database import get_connection

def get_section():
        conn = get_connection()
        cursor = conn.cursor()

        query = """
            SELECT *
            FROM section
        """
        cursor.execute(query)
        results = cursor.fetchall()    
        
        return results
    
    
def add_section(course_id, sec_id, semester, year, building, room_number, time_slot_id):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        query = """
            INSERT INTO section (course_id, sec_id, semester, year, building, room_number, time_slot_id) VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        values = (course_id, sec_id, semester, year, building, room_number, time_slot_id)
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
        
        
def delete_section(course_id , sec_id , semester , year):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        query = """
            DELETE FROM section
            WHERE (course_id , sec_id , semester , year) = (%s, %s, %s, %s)
        """
        values = (course_id , sec_id , semester , year)
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
        
        
def update_section(room_number, building, time_slot_id,  course_id , sec_id , semester , year):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        query = """
            UPDATE section
            SET room_number=%s, building=%s, time_slot_id=%s
            WHERE course_id = %s AND sec_id = %s AND semester = %s AND year = %s
        """
        values = (room_number, building, time_slot_id, course_id , sec_id , semester , year)
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
        
