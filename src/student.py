from database import get_connection

def get_students():
        conn = get_connection()
        cursor = conn.cursor()

        query = """
            SELECT *
            FROM student
        """
        cursor.execute(query)
        results = cursor.fetchall()    
        
        return results
    
    
def add_student(id, name, dept_name, tot_cred):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        query = """
            INSERT INTO student (id, name, dept_name, tot_cred) VALUES (%s, %s, %s, %s)
        """
        values = (id, name, dept_name, tot_cred)
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
        
        
def delete_student(id):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        query = """
            DELETE FROM student
            WHERE id = %s
        """
        values = (id,)
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
        
        
def update_student(id, name, dept_name, tot_cred):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        query = """
            UPDATE student
            SET name=%s, dept_name=%s, tot_cred=%s
            WHERE id=%s
        """
        values = (name, dept_name, tot_cred, id)
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
        
        
        
def get_student_by_dept_name(dept_name):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        x = ','.join(['%s'] * len(dept_name))
        query = f"""
            SELECT *
            FROM student
            WHERE dept_name in ({x})
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
    