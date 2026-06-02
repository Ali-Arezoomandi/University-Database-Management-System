from database import get_connection

def get_courses():
        conn = get_connection()
        cursor = conn.cursor()

        query = """
            SELECT *
            FROM course
        """
        cursor.execute(query)
        results = cursor.fetchall()    
        
        return results
    
    
def add_course(course_id, title, dept_name, credits):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        query = """
            INSERT INTO course (course_id, title, dept_name, credits) VALUES (%s, %s, %s, %s)
        """
        values = (course_id, title, dept_name, credits)
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
        
        
def delete_course(course_id):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        query = """
            DELETE FROM course
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
        
        
def update_course(course_id, title, credits):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        query = """
            UPDATE course
            SET title=%s, credits=%s
            WHERE course_id=%s
        """
        values = (title, credits, course_id)
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
        
        
def get_course_by_dept_name(dept_name):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        x = ','.join(['%s'] * len(dept_name))
        query = f"""
            SELECT *
            FROM course
            WHERE dept_name IN ({x})
        """

        cursor.execute(query, dept_name)
        
        result = cursor.fetchall()
        return result
        
    except Exception as e:
        print(e)
        conn.rollback()
    finally:
        cursor.close()
        conn.close()