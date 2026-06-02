from database import get_connection

def get_prereq():
        conn = get_connection()
        cursor = conn.cursor()

        query = """
            SELECT *
            FROM prereq
        """
        cursor.execute(query)
        results = cursor.fetchall()    
        
        return results
    
    
def add_prereq(course_id, prereq_id):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        query = """
            INSERT INTO prereq (course_id, prereq_id) VALUES (%s, %s)
        """
        values = (course_id, prereq_id)
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
        
        
def delete_prereq(course_id):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        query = """
            DELETE FROM prereq
            WHERE course_id = %s
        """
        values = (course_id,)
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
        
        
def update_prereq(course_id, prereq_id):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        query = """
            UPDATE prereq
            SET prereq_id=%s
            WHERE course_id=%s
        """
        values = (prereq_id, course_id)
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
        

def search_prereq_by_course(course_id):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        query = """
            SELECT * 
            FROM prereq 
            WHERE course_id = %s
        """
        cursor.execute(query, (course_id,))
        results = cursor.fetchall()
        
        return results
    except Exception as e:
        print(e)
        return []
    finally:
        cursor.close()
        conn.close()


def search_courses_by_prereq(prereq_id):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        query = """
            SELECT * 
            FROM prereq 
            WHERE prereq_id = %s
        """
        cursor.execute(query, (prereq_id,))
        results = cursor.fetchall()
        
        return results
    except Exception as e:
        print(e)
        return []
    finally:
        cursor.close()
        conn.close()