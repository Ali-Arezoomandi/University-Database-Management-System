from database import get_connection

def get_advisor():
        conn = get_connection()
        cursor = conn.cursor()

        query = """
            SELECT *
            FROM advisor
        """
        cursor.execute(query)
        results = cursor.fetchall()    
        
        return results
    
    
def add_advisor(s_id, i_id):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        query = """
            INSERT INTO advisor (s_id, i_id) VALUES (%s, %s)
        """
        values = (s_id, i_id)
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
        
        
def delete_advisor(s_id):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        query = """
            DELETE FROM advisor
            WHERE s_id = %s
        """
        values = (s_id,)
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
        
        
def update_advisor(s_id, i_id):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        query = """
            UPDATE advisor
            SET i_id=%s
            WHERE s_id=%s
        """
        values = (i_id, s_id)
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
        

def search_s_id_by_i_id(i_id):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        query = """
            SELECT * 
            FROM advisor 
            WHERE i_id = %s
        """
        cursor.execute(query, (i_id,))
        results = cursor.fetchall()
        
        return results
    except Exception as e:
        print(e)
        return []
    finally:
        cursor.close()
        conn.close()


def search_i_id_by_s_id(s_id):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        query = """
            SELECT * 
            FROM advisor 
            WHERE s_id = %s
        """
        cursor.execute(query, (s_id,))
        results = cursor.fetchall()
        
        return results
    except Exception as e:
        print(e)
        return []
    finally:
        cursor.close()
        conn.close()