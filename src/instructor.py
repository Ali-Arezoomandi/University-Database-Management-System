from database import get_connection

def get_instructors():
        conn = get_connection()
        cursor = conn.cursor()

        query = """
            SELECT *
            FROM instructor
        """
        cursor.execute(query)
        results = cursor.fetchall()    
        
        return results
    
    
def add_instructor(id, name, dept_name, salary):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        query = """
            INSERT INTO instructor (id, name, dept_name, salary) VALUES (%s, %s, %s, %s)
        """
        values = (id, name, dept_name, salary)
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
        
        
def delete_instructor(id):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        query = """
            DELETE FROM instructor
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
        
        
def update_instructor(id, name, salary):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        query = """
            UPDATE instructor
            SET name=%s, salary=%s
            WHERE id=%s
        """
        values = (name, salary, id)
        cursor.execute(query, values)
        
        conn.commit()
                
        if cursor.rowcount <= 0:
            return False
        return True
        
    except Exception as e:
        print()
        conn.rollback()
    finally:
        cursor.close()
        conn.close()
        
        
def get_instructor_by_dept_name(dept_name):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        x = ','.join(['%s'] * len(dept_name))
        query = f"""
            SELECT *
            FROM instructor
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