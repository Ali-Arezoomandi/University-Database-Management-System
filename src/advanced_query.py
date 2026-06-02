# src/advanced_query.py
from database import get_connection

def get_best_grade():
    try:
        conn = get_connection()
        cursor = conn.cursor()

        query = """
            SELECT÷ s.id, s.name, s.dept_name, c.course_id, c.title, t.grade
            FROM student s
            JOIN takes t ON s.id = t.id
            JOIN course c ON t.course_id = c.course_id
            WHERE t.grade = 'A'
            ORDER BY s.id
        """
        
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Exception as e:
        print(e)
        return []
    finally:
        cursor.close()
        conn.close()
        
        
def number_of_course_student_from_by_dept_name():
    try:
        conn = get_connection()
        cursor = conn.cursor()

        query = """
            WITH course_count(dept_name, value) AS (
                    SELECT dept_name, COUNT(course_id)
                    FROM course
                    GROUP BY dept_name
                ),
                student_count(dept_name, value) AS (
                    SELECT dept_name, COUNT(id)
                    FROM student
                    GROUP BY dept_name
                )
            SELECT s.dept_name,
                    s.value AS number_of_student,
                    c.value AS number_of_course
            FROM student_count s JOIN course_count c
            ON s.dept_name = c.dept_name
        """
        
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Exception as e:
        print(e)
        return []
    finally:
        cursor.close()
        conn.close()
        

def get_instructor_with_amount_of_course_credits():
    try:
        conn = get_connection()
        cursor = conn.cursor()

        query = """
            SELECT i.id,
                   i.name, 
                   i.dept_name, 
                   COUNT(t.course_id) AS number_of_course, 
                   SUM(c.credits) AS sum_of_credits
            FROM instructor i 
            JOIN teaches t ON i.id = t.id
            JOIN course c ON t.course_id = c.course_id
            GROUP BY i.id, i.name, i.dept_name
        """
        
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Exception as e:
        print(e)
        return []
    finally:
        cursor.close()
        conn.close()
        
        
def get_students_of_section(course_id, sec_id, semester, year):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        query = """
            SELECT s.id, s.name
            FROM student s 
            JOIN takes t ON s.id = t.id
            JOIN section s2 ON s2.course_id = t.course_id
                            AND s2.sec_id = t.sec_id
                            AND s2.semester = t.semester
                            AND s2.year = t.year
            WHERE t.course_id=%s AND t.sec_id=%s AND t.semester=%s AND t.year=%s
        """
        values = (course_id, sec_id, semester, year)
        
        cursor.execute(query, values)
        result = cursor.fetchall()
        return result
    except Exception as e:
        print(e)
        return []
    finally:
        cursor.close()
        conn.close()
        