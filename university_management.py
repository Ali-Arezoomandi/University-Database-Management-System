import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import ScrolledFrame
from ttkbootstrap.toast import ToastNotification
import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import random
from src.student import get_students, add_student, delete_student, update_student, get_student_by_dept_name
from src.course import get_courses, add_course, delete_course, update_course, get_course_by_dept_name
from src.instructor import get_instructors, add_instructor, delete_instructor, update_instructor, get_instructor_by_dept_name
from src.enrollment import get_enrollments, add_enroll, delete_enroll, update_enroll
from src.section import get_section, add_section, delete_section, update_section
from src.teaches import get_teaches, add_teaches, delete_teaches, search_teaches_by_instructor
from src.prereq import get_prereq, add_prereq, delete_prereq, update_prereq, search_prereq_by_course, search_courses_by_prereq
from src.advisor import get_advisor, add_advisor, delete_advisor, update_advisor, search_s_id_by_i_id, search_i_id_by_s_id
from src.advanced_query import get_best_grade, number_of_course_student_from_by_dept_name, get_instructor_with_amount_of_course_credits, get_students_of_section


# ─────────────────────────────────────────────
#  Sample Data
# ─────────────────────────────────────────────
STUDENTS = []
results = get_students()
for (id, name, dept_name, tot_cred) in results:
    data = (id, name, dept_name, int(tot_cred))
    STUDENTS.append(data)
    
COURSES = []
results = get_courses()
for (course_id, title, dept_name, credits) in results:
    data = (course_id, title, dept_name, credits)
    COURSES.append(data)

INSTRUCTORS = []
results = get_instructors()
for (id, name, dept_name, salary) in results:
    data = (id, name, dept_name, salary)
    INSTRUCTORS.append(data)

ENROLLMENTS = []
results = get_enrollments()
for (id, course_id, sec_id, semester, year, grade) in results:
    data = (id, course_id, sec_id, semester, year, grade)
    ENROLLMENTS.append(data)
    
SECTIONS = []
results = get_section()
for (course_id, sec_id, semester, year, building, room_number, time_slot_id) in results:
    data = (course_id, sec_id, semester, year, building, room_number, time_slot_id)
    SECTIONS.append(data)
    
TEACHES = []
results = get_teaches()
for (id, course_id, sec_id, semester, year) in results:
    data = (id, course_id, sec_id, semester, year)
    TEACHES.append(data)

PREREQ = []
results = get_prereq()
for (course_id, prereq_id) in results:
    data = (course_id, prereq_id)
    PREREQ.append(data)

ADVISOR = []
results = get_advisor()
for (s_id, i_id) in results:
    data = (s_id, i_id)
    ADVISOR.append(data)


# ─────────────────────────────────────────────
#  Icon helpers (Unicode emoji as labels)
# ─────────────────────────────────────────────
ICONS = {
    "Dashboard":   "🏠",
    "Students":    "🎓",
    "Courses":     "📚",
    "Instructors": "👩‍🏫",
    "Enrollment":  "📋",
    "Sections":    "📖",
    "Teaches":     "👨‍🏫",
    "Prereq":      "🔗",
    "Advisor":     "🧑‍🏫",
    "Reports":     "📊",
    "Exit":        "🚪",
}


# ═════════════════════════════════════════════
#  Main Application
# ═════════════════════════════════════════════
class UniversityApp(ttk.Window):
    def __init__(self):
        super().__init__(themename="darkly")
        self.title("University Management System")
        self.geometry("1200x720")
        self.minsize(960, 800)
        self._center_window()

        # theme toggle state
        self._dark = True
        self._themes = {"dark": "darkly", "light": "flatly"}

        self._build_ui()
        self._show_page("Dashboard")

    # ── centering ──────────────────────────────
    def _center_window(self):
        self.update_idletasks()
        sw, sh = self.winfo_screenwidth(), self.winfo_screenheight()
        w, h = 1200, 720
        self.geometry(f"{w}x{h}+{(sw-w)//2}+{(sh-h)//2}")

    # ── build shell ────────────────────────────
    def _build_ui(self):
        # top bar
        self._build_topbar()
        # content area
        body = ttk.Frame(self)
        body.pack(fill=BOTH, expand=YES)
        # sidebar
        self._build_sidebar(body)
        # main frame
        self.main_frame = ttk.Frame(body, padding=0)
        self.main_frame.pack(side=LEFT, fill=BOTH, expand=YES)
        # status bar
        self._build_statusbar()

    # ── top bar ────────────────────────────────
    def _build_topbar(self):
        bar = ttk.Frame(self, bootstyle="primary", padding=(16, 8))
        bar.pack(fill=X)

        ttk.Label(
            bar, text="🎓  University Management System",
            font=("Segoe UI", 16, "bold"), bootstyle="inverse-primary"
        ).pack(side=LEFT)

        # theme toggle
        self.theme_btn = ttk.Button(
            bar, text="☀ Light Mode", bootstyle="outline-light",
            command=self._toggle_theme, width=14
        )
        self.theme_btn.pack(side=RIGHT, padx=(0, 8))

        ttk.Label(
            bar, text=f"👤 Admin  |  {datetime.now().strftime('%A, %d %b %Y')}",
            font=("Segoe UI", 10), bootstyle="inverse-primary"
        ).pack(side=RIGHT, padx=16)

    # ── sidebar ────────────────────────────────
    def _build_sidebar(self, parent):
        sidebar = ttk.Frame(parent, bootstyle="secondary", width=200)
        sidebar.pack(side=LEFT, fill=Y)
        sidebar.pack_propagate(False)

        ttk.Label(
            sidebar, text="NAVIGATION",
            font=("Segoe UI", 9, "bold"), bootstyle="secondary",
            padding=(16, 16, 0, 8)
        ).pack(anchor=W)

        self._nav_buttons = {}
        pages = ["Dashboard", "Students", "Courses", "Instructors", "Enrollment", "Sections", "Teaches", "Prereq", "Advisor", "Reports"]
        for page in pages:
            btn = ttk.Button(
                sidebar,
                text=f"  {ICONS[page]}  {page}",
                bootstyle="secondary",
                command=lambda p=page: self._show_page(p),
                width=22,
            )
            btn.pack(fill=X, padx=8, pady=2)
            self._nav_buttons[page] = btn

        # separator + exit
        ttk.Separator(sidebar).pack(fill=X, padx=8, pady=12)
        ttk.Button(
            sidebar,
            text=f"  {ICONS['Exit']}  Exit",
            bootstyle="danger-outline",
            command=self._on_exit,
            width=22,
        ).pack(fill=X, padx=8, pady=2)

    # ── status bar ─────────────────────────────
    def _build_statusbar(self):
        bar = ttk.Frame(self, bootstyle="dark", padding=(12, 4))
        bar.pack(fill=X, side=BOTTOM)
        self.status_var = tk.StringVar(value="Ready")
        ttk.Label(bar, textvariable=self.status_var,
                  font=("Segoe UI", 9), bootstyle="inverse-dark").pack(side=LEFT)
        ttk.Label(bar, text=f"v1.0  |  © {datetime.now().year} University System",
                  font=("Segoe UI", 9), bootstyle="inverse-dark").pack(side=RIGHT)

    # ── theme toggle ───────────────────────────
    def _toggle_theme(self):
        self._dark = not self._dark
        self.style.theme_use(self._themes["dark" if self._dark else "light"])
        self.theme_btn.config(text="☀ Light Mode" if self._dark else "🌙 Dark Mode")

    # ── page router ────────────────────────────
    def _show_page(self, name):
        for w in self.main_frame.winfo_children():
            w.destroy()
        # highlight active nav
        for n, b in self._nav_buttons.items():
            b.config(bootstyle="info" if n == name else "secondary")
        self.status_var.set(f"Section: {name}")
        pages = {
            "Dashboard":   self._page_dashboard,
            "Students":    self._page_students,
            "Courses":     self._page_courses,
            "Instructors": self._page_instructors,
            "Enrollment":  self._page_enrollment,
            "Sections":    self._page_sections,
            "Teaches":     self._page_teaches,
            "Prereq":      self._page_prereq,
            "Advisor":     self._page_advisor,
            "Reports":     self._page_reports,
        }
        pages[name]()


    # ════════════════════════════════════════════
    #  DASHBOARD PAGE
    # ════════════════════════════════════════════
    def _page_dashboard(self):
        f = ScrolledFrame(self.main_frame, autohide=True)
        f.pack(fill=BOTH, expand=YES)
        inner = f.container

        ttk.Label(inner, text="Welcome, Admin 👋",
                  font=("Segoe UI", 20, "bold")).pack(anchor=W, padx=24, pady=(24, 4))
        ttk.Label(inner, text="Here's an overview of your university system.",
                  font=("Segoe UI", 11), bootstyle="secondary").pack(anchor=W, padx=24, pady=(0, 20))

        # stat cards
        cards = ttk.Frame(inner)
        cards.pack(fill=X, padx=24)
        stats = [
            ("🎓", "Total Students",    len(STUDENTS),    "info"),
            ("📚", "Total Courses",     len(COURSES),     "success"),
            ("👩‍🏫", "Instructors",       len(INSTRUCTORS), "warning"),
            ("📋", "Enrollments",       len(ENROLLMENTS), "danger"),
        ]
        for icon, label, value, style in stats:
            card = ttk.Frame(cards, bootstyle=style, padding=20)
            card.pack(side=LEFT, expand=YES, fill=X, padx=6)
            ttk.Label(card, text=icon, font=("Segoe UI", 28),
                      bootstyle=f"inverse-{style}").pack()
            ttk.Label(card, text=str(value), font=("Segoe UI", 28, "bold"),
                      bootstyle=f"inverse-{style}").pack()
            ttk.Label(card, text=label, font=("Segoe UI", 10),
                      bootstyle=f"inverse-{style}").pack()

        ttk.Separator(inner).pack(fill=X, padx=24, pady=20)

        # recent activity
        ttk.Label(inner, text="Recent Enrollments",
                  font=("Segoe UI", 14, "bold")).pack(anchor=W, padx=24, pady=(0, 8))
        cols = ("Student ID", "Course", "Semester", "Grade")
        tree = self._make_tree(inner, cols)
        for row in ENROLLMENTS[-5:]:
            tree.insert("", END, values=row)


    # ════════════════════════════════════════════
    #  STUDENTS PAGE
    # ════════════════════════════════════════════
    def _page_students(self):
    
        def refresh_students_list():
            global STUDENTS
            STUDENTS = []
            results = get_students()
            for (id, name, dept_name, tot_cred) in results:
                STUDENTS.append((id, name, dept_name, int(tot_cred)))
        
        for w in self.main_frame.winfo_children():
            w.destroy()
        
        main = ttk.Frame(self.main_frame)
        main.pack(fill=BOTH, expand=YES, padx=10, pady=10)
        
        ttk.Label(main, text="🎓 Student Management", font=("Segoe UI", 18, "bold")).pack(pady=10)
        
        filter_frame = ttk.LabelFrame(main, text="Filter by Department")
        filter_frame.pack(fill=X, padx=10, pady=5)

        departments = ["Biology", "Comp. Sci.", "Elec. Eng.", "Finance", "Geology", "History", "Music", "Physics", "All"]

        dept_vars = {}

        def on_dept_filter():
            selected_depts = [dept for dept, var in dept_vars.items() if var.get() and dept != "All"]
            
            if selected_depts and dept_vars["All"].get():
                dept_vars["All"].set(False)
            
            if dept_vars["All"].get():
                for dept, var in dept_vars.items():
                    if dept != "All":
                        var.set(False)
                selected_depts = []
            
            if dept_vars["All"].get() or len(selected_depts) == 0:
                filtered_data = STUDENTS  # یا COURSES
            else:
                filtered_data = get_student_by_dept_name(selected_depts)  # یا get_course_by_dept_name
            
            for item in tree.get_children():
                tree.delete(item)
            for row in filtered_data:
                tree.insert("", END, values=row)
            
            self._notify(f"Showing {len(filtered_data)} items")

        dept_frame = ttk.Frame(filter_frame)
        dept_frame.pack(pady=8)

        row_frame = None
        for i, dept in enumerate(departments):
            if i % 4 == 0:
                row_frame = ttk.Frame(dept_frame)
                row_frame.pack(anchor=W, pady=2)
            
            var = tk.BooleanVar(value=(dept == "All"))
            cb = ttk.Checkbutton(row_frame, text=dept, variable=var, command=on_dept_filter)
            cb.pack(side=LEFT, padx=10)
            dept_vars[dept] = var
        
        top_buttons = ttk.Frame(main)
        top_buttons.pack(pady=5)
        
        def add_row():
            vals = [entries[lbl].get().strip() for lbl in labels]
            if all(vals):
                res = add_student(vals[0], vals[1], vals[2], int(vals[3]))
                if res:
                    refresh_students_list()
                    tree.insert("", END, values=vals)
                    self._notify("Student saved!")
                    clear_form()
            else:
                messagebox.showwarning("Missing", "Please fill all fields")
        
        def update_row():
            selected = tree.selection()
            if not selected:
                messagebox.showinfo("Select", "Please select a student to update")
                return
            
            vals = [entries[lbl].get().strip() for lbl in labels]
            if not all(vals):
                messagebox.showwarning("Missing", "Please fill all fields")
                return
            
            old_values = tree.item(selected[0], "values")
            old_id = old_values[0]
            old_dept_name = old_values[2]
            
            if old_id != vals[0] or old_dept_name != vals[2]:
                self._notify("Can't change ID or Dept Name field!", "danger")
            else:
                res = update_student(old_id, vals[1], vals[2], vals[3])
                if res:
                    refresh_students_list()
                    tree.item(selected[0], values=vals)
                    self._notify(f"Student {old_id} updated!")
                    clear_form()
        
        def del_row():
            selected = tree.selection()
            if selected:
                row = tree.item(selected[0], 'values')
                row_id = row[0]
                res = delete_student(row_id)
                if res:
                    refresh_students_list()
                    tree.delete(selected[0])
                    self._notify("Student deleted!")
                    clear_form()
            else:
                messagebox.showinfo("Select", "Please select a student first")
        
        ttk.Button(top_buttons, text="➕ ADD", command=add_row, width=12).pack(side=LEFT, padx=5)
        ttk.Button(top_buttons, text="✏ UPDATE", command=update_row, width=12).pack(side=LEFT, padx=5)
        ttk.Button(top_buttons, text="🗑 DELETE", command=del_row, width=12).pack(side=LEFT, padx=5)
        
        cols = ("id", "name", "dept_name", "tot_cred")
        tree_frame = ttk.Frame(main)
        tree_frame.pack(fill=BOTH, expand=YES, pady=10)
        
        tree = ttk.Treeview(tree_frame, columns=cols, show="headings", height=15)
        for col in cols:
            tree.heading(col, text=col)
            tree.column(col, width=150)
        
        scroll = ttk.Scrollbar(tree_frame, orient=VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scroll.set)
        tree.pack(side=LEFT, fill=BOTH, expand=YES)
        scroll.pack(side=RIGHT, fill=Y)
        
        for row in STUDENTS:
            tree.insert("", END, values=row)
        
        input_frame = ttk.LabelFrame(main, text="Student Details")
        input_frame.pack(fill=X, pady=10)
        
        entry_frame = ttk.Frame(input_frame)
        entry_frame.pack(pady=10)
        
        entries = {}
        labels = ["ID", "Name", "Dept Name", "Credits"]
        default_values = ["", "", "", ""]
        
        for i, (lbl, val) in enumerate(zip(labels, default_values)):
            f = ttk.Frame(entry_frame)
            f.pack(side=LEFT, padx=8)
            ttk.Label(f, text=lbl, font=("Segoe UI", 9, "bold")).pack()
            e = ttk.Entry(f, width=15)
            e.pack(pady=2)
            e.insert(0, val)
            entries[lbl] = e
        
        def load_selected():
            selected = tree.selection()
            if selected:
                values = tree.item(selected[0], "values")
                for i, lbl in enumerate(labels):
                    if i < len(values):
                        entries[lbl].delete(0, tk.END)
                        entries[lbl].insert(0, values[i])
        
        tree.bind("<<TreeviewSelect>>", lambda e: load_selected())
        
        def clear_form():
            for e in entries.values():
                e.delete(0, tk.END)
        
        btn_frame = ttk.Frame(input_frame)
        btn_frame.pack(pady=10)
        ttk.Button(btn_frame, text="Clear", command=clear_form, width=12).pack(side=LEFT, padx=5)
        
        
    def _add_student_from_form(self, tree, s_vars, fields):
        vals = [v.get().strip() for v in s_vars.values()]
        if all(vals):
            tree.insert("", END, values=vals)
            self._notify("Student added! 🎓")
            for v in s_vars.values():
                v.set("")
        else:
            messagebox.showwarning("Missing", "Please fill all fields.")

    def _update_student_from_form(self, tree, s_vars, fields):
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Select", "Please select a student to update.")
            return
        vals = [v.get().strip() for v in s_vars.values()]
        if all(vals):
            tree.item(selected[0], values=vals)
            self._notify("Student updated! ✏")
        else:
            messagebox.showwarning("Missing", "Please fill all fields.")

    def _delete_student_from_tree(self, tree):
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Select", "Please select a student to delete.")
            return
        if messagebox.askyesno("Confirm Delete", "Delete this student?"):
            tree.delete(selected[0])
            self._notify("Student deleted! 🗑")

    def _student_select(self, tree):
        sel = tree.selection()
        if not sel:
            return
        vals = tree.item(sel[0], "values")
        keys = list(self._s_vars.keys())
        for k, v in zip(keys, vals):
            self._s_vars[k].set(v)

    def _student_add(self, tree):
        vals = [v.get().strip() for v in self._s_vars.values()]
        if not all(vals):
            messagebox.showwarning("Missing Data", "Please fill all fields.")
            return
        tree.insert("", END, values=vals)
        self._notify("Student added successfully! ✅")

    def _student_update(self, tree):
        sel = tree.selection()
        if not sel:
            messagebox.showinfo("Select Row", "Please select a student to update.")
            return
        vals = [v.get().strip() for v in self._s_vars.values()]
        tree.item(sel[0], values=vals)
        self._notify("Student updated! ✏")

    def _student_delete(self, tree):
        sel = tree.selection()
        if not sel:
            messagebox.showinfo("Select Row", "Please select a student to delete.")
            return
        if messagebox.askyesno("Confirm Delete", "Delete this student?"):
            tree.delete(sel[0])
            self._notify("Student deleted! 🗑")

    def _student_search(self, tree):
        q = self._s_vars["name"].get().strip().lower()  
        for item in tree.get_children():
            vals = tree.item(item, "values")
            if q in str(vals).lower():
                tree.selection_set(item)
                tree.see(item)
                return
        messagebox.showinfo("Not Found", "No matching student found.")

    def _filter_tree(self, tree, data, query):
        for item in tree.get_children():
            tree.delete(item)
        q = query.lower()
        for row in data:
            if q in str(row).lower():
                tree.insert("", END, values=row)


    # ════════════════════════════════════════════
    #  COURSES PAGE
    # ════════════════════════════════════════════
    def _page_courses(self):
        def refresh_courses_list():
            global COURSES
            COURSES = []
            results = get_courses()
            for (course_id, title, dept_name, credits) in results:
                COURSES.append((course_id, title, dept_name, credits))
        
        for w in self.main_frame.winfo_children():
            w.destroy()
        
        main = ttk.Frame(self.main_frame)
        main.pack(fill=BOTH, expand=YES, padx=10, pady=10)
        
        ttk.Label(main, text="📚 Course Management", font=("Segoe UI", 18, "bold")).pack(pady=10)
        
        filter_frame = ttk.LabelFrame(main, text="Filter by Department")
        filter_frame.pack(fill=X, padx=10, pady=5)

        departments = ["Biology", "Comp. Sci.", "Elec. Eng.", "Finance", "Geology", "History", "Music", "Physics", "All"]

        dept_vars = {}

        def on_dept_filter():
            selected_depts = [dept for dept, var in dept_vars.items() if var.get() and dept != "All"]
            
            if selected_depts and dept_vars["All"].get():
                dept_vars["All"].set(False)
            
            if dept_vars["All"].get():
                for dept, var in dept_vars.items():
                    if dept != "All":
                        var.set(False)
                selected_depts = []
            
            if dept_vars["All"].get() or len(selected_depts) == 0:
                filtered_data = STUDENTS  # یا COURSES
            else:
                filtered_data = get_course_by_dept_name(selected_depts)  
            
            for item in tree.get_children():
                tree.delete(item)
            for row in filtered_data:
                tree.insert("", END, values=row)
            
            self._notify(f"Showing {len(filtered_data)} items")

        dept_frame = ttk.Frame(filter_frame)
        dept_frame.pack(pady=8)

        row_frame = None
        for i, dept in enumerate(departments):
            if i % 4 == 0:
                row_frame = ttk.Frame(dept_frame)
                row_frame.pack(anchor=W, pady=2)
            
            var = tk.BooleanVar(value=(dept == "All"))
            cb = ttk.Checkbutton(row_frame, text=dept, variable=var, command=on_dept_filter)
            cb.pack(side=LEFT, padx=10)
            dept_vars[dept] = var
        
        top_buttons = ttk.Frame(main)
        top_buttons.pack(pady=5)
        
        def add_row():
            vals = [entries[lbl].get().strip() for lbl in labels]
            if all(vals):
                res = add_course(vals[0], vals[1], vals[2], int(vals[3]))
                if res:
                    refresh_courses_list()
                    tree.insert("", END, values=vals)
                    self._notify("Course saved!")
                    clear_form()
            else:
                messagebox.showwarning("Missing", "Please fill all fields")
        
        def update_row():
            selected = tree.selection()
            if not selected:
                messagebox.showinfo("Select", "Please select a course to update")
                return
            
            vals = [entries[lbl].get().strip() for lbl in labels]
            if not all(vals):
                messagebox.showwarning("Missing", "Please fill all fields")
                return
            
            old_values = tree.item(selected[0], "values")
            old_course_id = old_values[0]
            old_dept_name = old_values[2]
            
            if old_course_id != vals[0] or old_dept_name != vals[2]:
                self._notify("Can't change Course ID or Dept Name!", "danger")
            else:
                res = update_course(old_course_id, vals[1], vals[3])
                if res:
                    refresh_courses_list()
                    tree.item(selected[0], values=vals)
                    self._notify(f"Course {old_course_id} updated!")
                    clear_form()
        
        def del_row():
            selected = tree.selection()
            if selected:
                row = tree.item(selected[0], 'values')
                row_id = row[0]
                res = delete_course(row_id)
                if res:
                    refresh_courses_list()
                    tree.delete(selected[0])
                    self._notify("Course deleted!")
                    clear_form()
            else:
                messagebox.showinfo("Select", "Please select a course first")
        
        ttk.Button(top_buttons, text="➕ ADD", command=add_row, width=12).pack(side=LEFT, padx=5)
        ttk.Button(top_buttons, text="✏ UPDATE", command=update_row, width=12).pack(side=LEFT, padx=5)
        ttk.Button(top_buttons, text="🗑 DELETE", command=del_row, width=12).pack(side=LEFT, padx=5)
        
        cols = ("course_id", "title", "dept_name", "credits")
        tree_frame = ttk.Frame(main)
        tree_frame.pack(fill=BOTH, expand=YES, pady=10)
        
        tree = ttk.Treeview(tree_frame, columns=cols, show="headings", height=15)
        for col in cols:
            tree.heading(col, text=col)
            tree.column(col, width=150)
        
        scroll = ttk.Scrollbar(tree_frame, orient=VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scroll.set)
        tree.pack(side=LEFT, fill=BOTH, expand=YES)
        scroll.pack(side=RIGHT, fill=Y)
        
        for row in COURSES:
            tree.insert("", END, values=row)
        
        input_frame = ttk.LabelFrame(main, text="Course Details")
        input_frame.pack(fill=X, pady=10)
        
        entry_frame = ttk.Frame(input_frame)
        entry_frame.pack(pady=10)
        
        entries = {}
        labels = ["Course ID", "Title", "Dept Name", "Credits"]
        
        for i, lbl in enumerate(labels):
            f = ttk.Frame(entry_frame)
            f.pack(side=LEFT, padx=8)
            ttk.Label(f, text=lbl, font=("Segoe UI", 9, "bold")).pack()
            e = ttk.Entry(f, width=18)
            e.pack(pady=2)
            entries[lbl] = e
        
        def load_selected():
            selected = tree.selection()
            if selected:
                values = tree.item(selected[0], "values")
                for i, lbl in enumerate(labels):
                    if i < len(values):
                        entries[lbl].delete(0, tk.END)
                        entries[lbl].insert(0, values[i])
        
        tree.bind("<<TreeviewSelect>>", lambda e: load_selected())
        
        def clear_form():
            for e in entries.values():
                e.delete(0, tk.END)
        
        btn_frame = ttk.Frame(input_frame)
        btn_frame.pack(pady=10)
        ttk.Button(btn_frame, text="Clear", command=clear_form, width=12).pack(side=LEFT, padx=5)


    # ════════════════════════════════════════════
    #  INSTRUCTORS PAGE
    # ════════════════════════════════════════════
    def _page_instructors(self):
        def refresh_instructors_list():
            global INSTRUCTORS
            INSTRUCTORS = []
            results = get_instructors()
            for (id, name, dept_name, salary) in results:
                INSTRUCTORS.append((id, name, dept_name, salary))
        
        for w in self.main_frame.winfo_children():
            w.destroy()
        
        main = ttk.Frame(self.main_frame)
        main.pack(fill=BOTH, expand=YES, padx=10, pady=10)
        
        ttk.Label(main, text="👩‍🏫 Instructor Management", font=("Segoe UI", 18, "bold")).pack(pady=10)
        
        filter_frame = ttk.LabelFrame(main, text="Filter by Department")
        filter_frame.pack(fill=X, padx=10, pady=5)

        departments = ["Biology", "Comp. Sci.", "Elec. Eng.", "Finance", "Geology", "History", "Music", "Physics", "All"]

        dept_vars = {}

        def on_dept_filter():
            selected_depts = [dept for dept, var in dept_vars.items() if var.get() and dept != "All"]
            
            if selected_depts and dept_vars["All"].get():
                dept_vars["All"].set(False)
            
            if dept_vars["All"].get():
                for dept, var in dept_vars.items():
                    if dept != "All":
                        var.set(False)
                selected_depts = []
            
            if dept_vars["All"].get() or len(selected_depts) == 0:
                filtered_data = INSTRUCTORS
            else:
                filtered_data = get_instructor_by_dept_name(selected_depts)
            
            for item in tree.get_children():
                tree.delete(item)
            for row in filtered_data:
                tree.insert("", END, values=row)
            
            self._notify(f"Showing {len(filtered_data)} instructors")

        dept_frame = ttk.Frame(filter_frame)
        dept_frame.pack(pady=8)

        row_frame = None
        for i, dept in enumerate(departments):
            if i % 4 == 0:
                row_frame = ttk.Frame(dept_frame)
                row_frame.pack(anchor=W, pady=2)
            
            var = tk.BooleanVar(value=(dept == "All"))
            cb = ttk.Checkbutton(row_frame, text=dept, variable=var, command=on_dept_filter)
            cb.pack(side=LEFT, padx=10)
            dept_vars[dept] = var
        
        top_buttons = ttk.Frame(main)
        top_buttons.pack(pady=5)
        
        def add_row():
            vals = [entries[lbl].get().strip() for lbl in labels]
            if all(vals):
                res = add_instructor(vals[0], vals[1], vals[2], float(vals[3]))
                if res:
                    refresh_instructors_list()
                    on_dept_filter() 
                    self._notify("Instructor saved!")
                    clear_form()
            else:
                messagebox.showwarning("Missing", "Please fill all fields")
        
        def update_row():
            selected = tree.selection()
            if not selected:
                messagebox.showinfo("Select", "Please select an instructor to update")
                return
            
            vals = [entries[lbl].get().strip() for lbl in labels]
            if not all(vals):
                messagebox.showwarning("Missing", "Please fill all fields")
                return
            
            old_values = tree.item(selected[0], "values")
            old_id = old_values[0]
            old_dept_name = old_values[2]
            
            if old_id != vals[0] or old_dept_name != vals[2]:
                self._notify("Can't change instructor ID or Dept Name!", "danger")
            else:
                res = update_instructor(old_id, vals[1], float(vals[3]))
                if res:
                    refresh_instructors_list()
                    on_dept_filter()
                    self._notify(f"Instructor {old_id} updated!")
                    clear_form()
        
        def del_row():
            selected = tree.selection()
            if selected:
                row = tree.item(selected[0], 'values')
                row_id = row[0]
                if messagebox.askyesno("Confirm Delete", f"Delete instructor {row_id}?"):
                    res = delete_instructor(row_id)
                    if res:
                        refresh_instructors_list()
                        on_dept_filter()
                        self._notify("Instructor deleted!")
                        clear_form()
            else:
                messagebox.showinfo("Select", "Please select an instructor first")
        
        ttk.Button(top_buttons, text="➕ ADD", command=add_row, width=12).pack(side=LEFT, padx=5)
        ttk.Button(top_buttons, text="✏ UPDATE", command=update_row, width=12).pack(side=LEFT, padx=5)
        ttk.Button(top_buttons, text="🗑 DELETE", command=del_row, width=12).pack(side=LEFT, padx=5)
        
        cols = ("id", "name", "dept_name", "salary")
        tree_frame = ttk.Frame(main)
        tree_frame.pack(fill=BOTH, expand=YES, pady=10)
        
        tree = ttk.Treeview(tree_frame, columns=cols, show="headings", height=15)
        for col in cols:
            tree.heading(col, text=col)
            tree.column(col, width=150)
        
        scroll = ttk.Scrollbar(tree_frame, orient=VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scroll.set)
        tree.pack(side=LEFT, fill=BOTH, expand=YES)
        scroll.pack(side=RIGHT, fill=Y)
        
        for row in INSTRUCTORS:
            tree.insert("", END, values=row)
        
        input_frame = ttk.LabelFrame(main, text="Instructor Details")
        input_frame.pack(fill=X, pady=10)
        
        entry_frame = ttk.Frame(input_frame)
        entry_frame.pack(pady=10)
        
        entries = {}
        labels = ["ID", "Name", "Dept Name", "Salary"]
        default_values = ["", "", "", ""]
        
        for i, (lbl, val) in enumerate(zip(labels, default_values)):
            f = ttk.Frame(entry_frame)
            f.pack(side=LEFT, padx=8)
            ttk.Label(f, text=lbl, font=("Segoe UI", 9, "bold")).pack()
            e = ttk.Entry(f, width=15)
            e.pack(pady=2)
            e.insert(0, val)
            entries[lbl] = e
        
        def load_selected():
            selected = tree.selection()
            if selected:
                values = tree.item(selected[0], "values")
                for i, lbl in enumerate(labels):
                    if i < len(values):
                        entries[lbl].delete(0, tk.END)
                        entries[lbl].insert(0, values[i])
        
        tree.bind("<<TreeviewSelect>>", lambda e: load_selected())
        
        def clear_form():
            for e in entries.values():
                e.delete(0, tk.END)
        
        btn_frame = ttk.Frame(input_frame)
        btn_frame.pack(pady=10)
        ttk.Button(btn_frame, text="Clear", command=clear_form, width=12).pack(side=LEFT, padx=5)


    # ════════════════════════════════════════════
    #  ENROLLMENT PAGE
    # ════════════════════════════════════════════
    def _page_enrollment(self):
        def refresh_enrollments_list():
            global ENROLLMENTS
            ENROLLMENTS = []
            results = get_enrollments()
            for (id, course_id, sec_id, semester, year, grade) in results:
                ENROLLMENTS.append((id, course_id, sec_id, semester, year, grade))
        
        for w in self.main_frame.winfo_children():
            w.destroy()
        
        main = ttk.Frame(self.main_frame)
        main.pack(fill=BOTH, expand=YES, padx=10, pady=10)
        
        ttk.Label(main, text="📋 Enrollment Management", font=("Segoe UI", 18, "bold")).pack(pady=10)
        
        top_buttons = ttk.Frame(main)
        top_buttons.pack(pady=5)
        
        def add_row():
            vals = [entries[lbl].get().strip() for lbl in labels]
            if all(vals):
                res = add_enroll(vals[0], vals[1], vals[2], vals[3], int(vals[4]), vals[5])
                if res:
                    refresh_enrollments_list()
                    tree.insert("", END, values=vals)
                    self._notify("Enrollment saved!")
                    clear_form()
            else:
                messagebox.showwarning("Missing", "Please fill all fields")
        
        def update_row():
            selected = tree.selection()
            if not selected:
                messagebox.showinfo("Select", "Please select an enrollment to update")
                return
            
            vals = [entries[lbl].get().strip() for lbl in labels]
            if not all(vals):
                messagebox.showwarning("Missing", "Please fill all fields")
                return
            
            old_values = tree.item(selected[0], "values")
            old_student_id = old_values[0]
            old_course_id = old_values[1]
            old_sec = old_values[2]
            old_semester = old_values[3]
            old_year = int(old_values[4])
            
            if old_student_id != vals[0] or old_course_id != vals[1] or old_sec != vals[2] or old_semester != vals[3] or old_year != int(vals[4]):
                self._notify("Can't change Enrollment ID, Course_id, Sec_id, Semester or Year!", "danger")
            else:
                res = update_enroll(old_student_id, old_course_id, vals[5])
                if res:
                    refresh_enrollments_list()
                    tree.item(selected[0], values=vals)
                    self._notify(f"Enrollment updated!")
                    clear_form()
            
        def del_row():
            selected = tree.selection()
            if selected:
                row = tree.item(selected[0], 'values')
                student_id = row[0]
                course_id = row[1]
                res = delete_enroll(student_id, course_id)
                if res:
                    refresh_enrollments_list()
                    tree.delete(selected[0])
                    self._notify("Enrollment deleted!")
                    clear_form()
            else:
                messagebox.showinfo("Select", "Please select an enrollment first")
        
        ttk.Button(top_buttons, text="➕ ADD", command=add_row, width=12).pack(side=LEFT, padx=5)
        ttk.Button(top_buttons, text="✏ UPDATE", command=update_row, width=12).pack(side=LEFT, padx=5)
        ttk.Button(top_buttons, text="🗑 DELETE", command=del_row, width=12).pack(side=LEFT, padx=5)
        
        cols = ("student_id", "course_id", "sec_id", "semester", "year", "grade")
        tree_frame = ttk.Frame(main)
        tree_frame.pack(fill=BOTH, expand=YES, pady=10)
        
        tree = ttk.Treeview(tree_frame, columns=cols, show="headings", height=12)
        for col in cols:
            tree.heading(col, text=col)
            tree.column(col, width=120)
        
        scroll = ttk.Scrollbar(tree_frame, orient=VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scroll.set)
        tree.pack(side=LEFT, fill=BOTH, expand=YES)
        scroll.pack(side=RIGHT, fill=Y)
        
        for row in ENROLLMENTS:
            tree.insert("", END, values=row)
        
        input_frame = ttk.LabelFrame(main, text="Enrollment Details")
        input_frame.pack(fill=X, pady=10)
        
        entry_frame = ttk.Frame(input_frame)
        entry_frame.pack(pady=10)
        
        entries = {}
        labels = ["Student ID", "Course ID", "Sec ID", "Semester", "Year", "Grade"]
        
        for i, lbl in enumerate(labels):
            f = ttk.Frame(entry_frame)
            f.pack(side=LEFT, padx=5)
            ttk.Label(f, text=lbl, font=("Segoe UI", 8, "bold")).pack()
            e = ttk.Entry(f, width=10)
            e.pack(pady=2)
            if lbl == "Year":
                e.insert(0, "2026")
            elif lbl == "Semester":
                e.insert(0, "Spring")
            entries[lbl] = e
        
        def load_selected():
            selected = tree.selection()
            if selected:
                values = tree.item(selected[0], "values")
                for i, lbl in enumerate(labels):
                    if i < len(values):
                        entries[lbl].delete(0, tk.END)
                        entries[lbl].insert(0, values[i])
        
        tree.bind("<<TreeviewSelect>>", lambda e: load_selected())
        
        def clear_form():
            for lbl, e in entries.items():
                e.delete(0, tk.END)
                if lbl == "Year":
                    e.insert(0, "1404")
                elif lbl == "Semester":
                    e.insert(0, "Fall")
        
        btn_frame = ttk.Frame(input_frame)
        btn_frame.pack(pady=10)
        ttk.Button(btn_frame, text="Clear", command=clear_form, width=12).pack(side=LEFT, padx=5)
        
        
    # ════════════════════════════════════════════
    #  SECTIONS PAGE
    # ════════════════════════════════════════════
    def _page_sections(self):
    
        def refresh_sections_list():
            global SECTIONS
            SECTIONS = []
            results = get_section()
            for (course_id, sec_id, semester, year, building, room_number, time_slot_id) in results:
                SECTIONS.append((course_id, sec_id, semester, year, building, room_number, time_slot_id))
        
        for w in self.main_frame.winfo_children():
            w.destroy()
        
        main = ttk.Frame(self.main_frame)
        main.pack(fill=BOTH, expand=YES, padx=10, pady=10)
        
        ttk.Label(main, text="📖 Section Management", font=("Segoe UI", 18, "bold")).pack(pady=10)
        
        top_buttons = ttk.Frame(main)
        top_buttons.pack(pady=5)
        
        def add_row():
            vals = [entries[lbl].get().strip() for lbl in labels]
            if all(vals):
                res = add_section(vals[0], vals[1], vals[2], int(vals[3]), vals[4], vals[5], vals[6])
                if res:
                    refresh_sections_list()
                    tree.insert("", END, values=vals)
                    self._notify("Section added successfully!")
                    clear_form()
                else:
                    messagebox.showerror("Error", "Failed to add section. Check if course exists!")
            else:
                messagebox.showwarning("Missing", "Please fill all fields")
        
        def update_row():
            selected = tree.selection()
            if not selected:
                messagebox.showinfo("Select", "Please select a section to update")
                return
            
            vals = [entries[lbl].get().strip() for lbl in labels]
            if not all(vals):
                messagebox.showwarning("Missing", "Please fill all fields")
                return
            
            old_values = tree.item(selected[0], "values")
            old_course_id = old_values[0]
            old_sec_id = old_values[1]
            old_semester = old_values[2]
            old_year = old_values[3]
            
            # بررسی تغییر نکردن کلید اصلی
            if (old_course_id != vals[0] or old_sec_id != vals[1] or 
                old_semester != vals[2] or str(old_year) != vals[3]):
                self._notify("Can't change Course ID, Sec ID, Semester or Year!", "danger")
            else:
                res = update_section(vals[5], vals[4], vals[6], old_course_id, old_sec_id, old_semester, old_year)
                if res:
                    refresh_sections_list()
                    tree.item(selected[0], values=vals)
                    self._notify("Section updated successfully!")
                    clear_form()
                else:
                    messagebox.showerror("Error", "Failed to update section")
        
        def del_row():
            selected = tree.selection()
            if not selected:
                messagebox.showinfo("Select", "Please select a section to delete")
                return
            
            if messagebox.askyesno("Confirm Delete", "Delete this section? This may affect enrollments!"):
                values = tree.item(selected[0], "values")
                res = delete_section(values[0], values[1], values[2], values[3])
                if res:
                    refresh_sections_list()
                    tree.delete(selected[0])
                    self._notify("Section deleted successfully!")
                    clear_form()
                else:
                    messagebox.showerror("Error", "Failed to delete section")
        
        ttk.Button(top_buttons, text="➕ ADD", command=add_row, width=12).pack(side=LEFT, padx=5)
        ttk.Button(top_buttons, text="✏ UPDATE", command=update_row, width=12).pack(side=LEFT, padx=5)
        ttk.Button(top_buttons, text="🗑 DELETE", command=del_row, width=12).pack(side=LEFT, padx=5)
        
        cols = ("course_id", "sec_id", "semester", "year", "building", "room_number", "time_slot_id")
        tree_frame = ttk.Frame(main)
        tree_frame.pack(fill=BOTH, expand=YES, pady=10)
        
        tree = ttk.Treeview(tree_frame, columns=cols, show="headings", height=8)
        for col in cols:
            tree.heading(col, text=col)
            tree.column(col, width=110)
        
        scroll = ttk.Scrollbar(tree_frame, orient=VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scroll.set)
        tree.pack(side=LEFT, fill=BOTH, expand=YES)
        scroll.pack(side=RIGHT, fill=Y)
        
        refresh_sections_list()
        for row in SECTIONS:
            tree.insert("", END, values=row)
        
        detail_frame = ttk.Frame(main, bootstyle="info")
        detail_frame.pack(fill=BOTH, expand=YES, pady=10, padx=10)
        
        ttk.Label(detail_frame, text="📌 Students Enrolled in Selected Section", 
                font=("Segoe UI", 11, "bold"), bootstyle="info").pack(anchor=W, pady=5)
        
        info_frame = ttk.Frame(detail_frame)
        info_frame.pack(fill=X, pady=5)
        ttk.Label(info_frame, text="Selected Section:", font=("Segoe UI", 10, "bold")).pack(side=LEFT)
        selected_label = ttk.Label(info_frame, text="None", font=("Segoe UI", 10), bootstyle="info")
        selected_label.pack(side=LEFT, padx=5)
        
        cols_students = ("Student ID", "Student Name")
        tree_students = ttk.Treeview(detail_frame, columns=cols_students, show="headings", height=6)
        tree_students.heading("Student ID", text="Student ID")
        tree_students.heading("Student Name", text="Student Name")
        tree_students.column("Student ID", width=150)
        tree_students.column("Student Name", width=200)
        
        scroll_students = ttk.Scrollbar(detail_frame, orient=VERTICAL, command=tree_students.yview)
        tree_students.configure(yscrollcommand=scroll_students.set)
        tree_students.pack(side=LEFT, fill=BOTH, expand=YES, pady=5)
        scroll_students.pack(side=RIGHT, fill=Y, pady=5)
        
        def on_section_select(event):
            for item in tree_students.get_children():
                tree_students.delete(item)
            
            selected = tree.selection()
            if not selected:
                selected_label.config(text="None")
                return
            
            values = tree.item(selected[0], "values")
            if len(values) < 4:
                selected_label.config(text="Invalid")
                return
            
            course_id = values[0]
            sec_id = values[1]
            semester = values[2]
            year = values[3]
            
            selected_label.config(text=f"{course_id} - Sec {sec_id} ({semester} {year})")
            
            try:
                students = get_students_of_section(course_id, sec_id, semester, year)
                if students:
                    for student in students:
                        tree_students.insert("", "end", values=student)
                    self._notify(f"Found {len(students)} students in this section")
                else:
                    tree_students.insert("", "end", values=("📭 No students found", ""))
            except Exception as e:
                tree_students.insert("", "end", values=(f"Error: {e}", ""))
        
        tree.bind("<<TreeviewSelect>>", on_section_select)
        
        input_frame = ttk.LabelFrame(main, text="Section Details")
        input_frame.pack(fill=X, pady=10)
        
        entry_frame = ttk.Frame(input_frame)
        entry_frame.pack(pady=10)
        
        entries = {}
        labels = ["Course ID", "Sec ID", "Semester", "Year", "Building", "Room Number", "Time Slot ID"]
        default_values = ["", "", "Fall", "2024", "", "", ""]
        
        for i, lbl in enumerate(labels):
            f = ttk.Frame(entry_frame)
            f.pack(side=LEFT, padx=5)
            ttk.Label(f, text=lbl, font=("Segoe UI", 8)).pack()
            e = ttk.Entry(f, width=10)
            e.pack(pady=2)
            if default_values[i]:
                e.insert(0, default_values[i])
            entries[lbl] = e
        
        def load_selected_to_form(event):
            selected = tree.selection()
            if selected:
                values = tree.item(selected[0], "values")
                for i, lbl in enumerate(labels):
                    if i < len(values):
                        entries[lbl].delete(0, tk.END)
                        entries[lbl].insert(0, values[i])
        
        tree.bind("<<TreeviewSelect>>", load_selected_to_form, add=True)
        
        def clear_form():
            default_values = ["", "", "Fall", "2024", "", "", ""]
            for i, (lbl, e) in enumerate(entries.items()):
                e.delete(0, tk.END)
                e.insert(0, default_values[i])
        
        btn_frame = ttk.Frame(input_frame)
        btn_frame.pack(pady=10)
        ttk.Button(btn_frame, text="Clear", command=clear_form, width=12).pack(side=LEFT, padx=5)
        
        
    # ════════════════════════════════════════════
    #  TEACHES PAGE
    # ════════════════════════════════════════════
    def _page_teaches(self):
        def refresh_teaches_list():
            global TEACHES
            TEACHES = []
            results = get_teaches()
            for (id, course_id, sec_id, semester, year) in results:
                TEACHES.append((id, course_id, sec_id, semester, year))
        
        for w in self.main_frame.winfo_children():
            w.destroy()
        
        main = ttk.Frame(self.main_frame)
        main.pack(fill=BOTH, expand=YES, padx=10, pady=10)
        
        ttk.Label(main, text="👨‍🏫 Teaches Management", font=("Segoe UI", 18, "bold")).pack(pady=10)
        
        search_frame = ttk.LabelFrame(main, text="Search by Instructor ID")
        search_frame.pack(fill=X, padx=10, pady=5)
        
        search_entry_frame = ttk.Frame(search_frame)
        search_entry_frame.pack(pady=8)
        
        ttk.Label(search_entry_frame, text="Instructor ID:").pack(side=LEFT, padx=5)
        search_var = tk.StringVar()
        search_entry = ttk.Entry(search_entry_frame, textvariable=search_var, width=15)
        search_entry.pack(side=LEFT, padx=5)
        
        def search_teaches():
            instructor_id = search_var.get().strip()
            if not instructor_id:
                messagebox.showwarning("Missing", "Please enter Instructor ID")
                return
            
            results = search_teaches_by_instructor(instructor_id)
            
            for item in tree.get_children():
                tree.delete(item)
            
            if results:
                for row in results:
                    tree.insert("", END, values=row)
                self._notify(f"Found {len(results)} records for instructor {instructor_id}")
            else:
                self._notify(f"No records found for instructor {instructor_id}", "warning")
        
        def reset_table():
            search_var.set("")
            refresh_teaches_list()
            for item in tree.get_children():
                tree.delete(item)
            for row in TEACHES:
                tree.insert("", END, values=row)
            self._notify("Table reset to full list")
        
        ttk.Button(search_entry_frame, text="🔍 Search", command=search_teaches, width=10).pack(side=LEFT, padx=5)
        ttk.Button(search_entry_frame, text="🔄 Reset", command=reset_table, width=10).pack(side=LEFT, padx=5)
        
        top_buttons = ttk.Frame(main)
        top_buttons.pack(pady=5)
        
        def add_row():
            vals = [entries[lbl].get().strip() for lbl in labels]
            if all(vals):
                res = add_teaches(vals[0], vals[1], vals[2], vals[3], int(vals[4]))
                if res:
                    refresh_teaches_list()
                    reset_table()
                    self._notify("Teach record saved!")
                    clear_form()
            else:
                messagebox.showwarning("Missing", "Please fill all fields")
        
        def del_row():
            selected = tree.selection()
            if selected:
                row = tree.item(selected[0], 'values')
                instructor_id = row[0]
                course_id = row[1]
                res = delete_teaches(instructor_id, course_id)
                if res:
                    refresh_teaches_list()
                    reset_table()
                    self._notify("Teach record deleted!")
                    clear_form()
            else:
                messagebox.showinfo("Select", "Please select a record first")
        
        ttk.Button(top_buttons, text="➕ ADD", command=add_row, width=12).pack(side=LEFT, padx=5)
        ttk.Button(top_buttons, text="🗑 DELETE", command=del_row, width=12).pack(side=LEFT, padx=5)
        
        cols = ("instructor_id", "course_id", "sec_id", "semester", "year")
        tree_frame = ttk.Frame(main)
        tree_frame.pack(fill=BOTH, expand=YES, pady=10)
        
        tree = ttk.Treeview(tree_frame, columns=cols, show="headings", height=12)
        for col in cols:
            tree.heading(col, text=col)
            tree.column(col, width=130)
        
        scroll = ttk.Scrollbar(tree_frame, orient=VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scroll.set)
        tree.pack(side=LEFT, fill=BOTH, expand=YES)
        scroll.pack(side=RIGHT, fill=Y)
        
        for row in TEACHES:
            tree.insert("", END, values=row)
        
        input_frame = ttk.LabelFrame(main, text="Teaches Details")
        input_frame.pack(fill=X, pady=10)
        
        entry_frame = ttk.Frame(input_frame)
        entry_frame.pack(pady=10)
        
        entries = {}
        labels = ["Instructor ID", "Course ID", "Sec ID", "Semester", "Year"]
        widths = [12, 10, 8, 10, 6]
        
        for i, (lbl, w) in enumerate(zip(labels, widths)):
            f = ttk.Frame(entry_frame)
            f.pack(side=LEFT, padx=5)
            ttk.Label(f, text=lbl, font=("Segoe UI", 8, "bold")).pack()
            e = ttk.Entry(f, width=w)
            e.pack(pady=2)
            if lbl == "Year":
                e.insert(0, "2024")
            elif lbl == "Semester":
                e.insert(0, "Fall")
            entries[lbl] = e
        
        def load_selected():
            selected = tree.selection()
            if selected:
                values = tree.item(selected[0], "values")
                for i, lbl in enumerate(labels):
                    if i < len(values):
                        entries[lbl].delete(0, tk.END)
                        entries[lbl].insert(0, values[i])
        
        tree.bind("<<TreeviewSelect>>", lambda e: load_selected())
        
        def clear_form():
            defaults = ["", "", "", "Fall", "2024"]
            for i, (lbl, e) in enumerate(entries.items()):
                e.delete(0, tk.END)
                e.insert(0, defaults[i])
        
        btn_frame = ttk.Frame(input_frame)
        btn_frame.pack(pady=10)
        ttk.Button(btn_frame, text="Clear", command=clear_form, width=12).pack(side=LEFT, padx=5)
        
        
    # ════════════════════════════════════════════
    #  PREREQ PAGE
    # ════════════════════════════════════════════
    def _page_prereq(self):
        def refresh_prereq_list():
            global PREREQ
            PREREQ = []
            results = get_prereq()
            for (course_id, prereq_id) in results:
                PREREQ.append((course_id, prereq_id))
        
        for w in self.main_frame.winfo_children():
            w.destroy()
        
        main = ttk.Frame(self.main_frame)
        main.pack(fill=BOTH, expand=YES, padx=10, pady=10)
        
        ttk.Label(main, text="🔗 Prerequisite Management", font=("Segoe UI", 18, "bold")).pack(pady=10)
        
        search_frame = ttk.LabelFrame(main, text="Search by Course ID")
        search_frame.pack(fill=X, padx=10, pady=5)
        
        search_entry_frame = ttk.Frame(search_frame)
        search_entry_frame.pack(pady=8)
        
        ttk.Label(search_entry_frame, text="Course ID:").pack(side=LEFT, padx=5)
        search_var = tk.StringVar()
        search_entry = ttk.Entry(search_entry_frame, textvariable=search_var, width=15)
        search_entry.pack(side=LEFT, padx=5)
        
        def search_prereq():
            course_id = search_var.get().strip()
            if not course_id:
                messagebox.showwarning("Missing", "Please enter Course ID")
                return
            
            results = search_prereq_by_course(course_id)
            
            for item in tree.get_children():
                tree.delete(item)
            
            if results:
                for row in results:
                    tree.insert("", END, values=row)
                self._notify(f"Found {len(results)} prerequisites for course {course_id}")
            else:
                self._notify(f"No prerequisites found for course {course_id}", "warning")
        
        def search_courses_that_need_prereq():
            prereq_id = search_var.get().strip()
            if not prereq_id:
                messagebox.showwarning("Missing", "Please enter Prerequisite ID")
                return
            
            results = search_courses_by_prereq(prereq_id)
            
            for item in tree.get_children():
                tree.delete(item)
            
            if results:
                for row in results:
                    tree.insert("", END, values=row)
                self._notify(f"Found {len(results)} courses that require {prereq_id} as prerequisite")
            else:
                self._notify(f"No courses found that require {prereq_id}", "warning")
        
        def reset_table():
            search_var.set("")
            refresh_prereq_list()
            for item in tree.get_children():
                tree.delete(item)
            for row in PREREQ:
                tree.insert("", END, values=row)
            self._notify("Table reset to full list")
        
        ttk.Button(search_entry_frame, text="🔍 Search by Course", command=search_prereq, width=14).pack(side=LEFT, padx=5)
        ttk.Button(search_entry_frame, text="🔍 Search by Prereq", command=search_courses_that_need_prereq, width=14).pack(side=LEFT, padx=5)
        ttk.Button(search_entry_frame, text="🔄 Reset", command=reset_table, width=10).pack(side=LEFT, padx=5)
        
        top_buttons = ttk.Frame(main)
        top_buttons.pack(pady=5)
        
        def add_row():
            vals = [entries[lbl].get().strip() for lbl in labels]
            if all(vals):
                res = add_prereq(vals[0], vals[1])
                if res:
                    refresh_prereq_list()
                    reset_table()
                    self._notify("Prerequisite saved!")
                    clear_form()
            else:
                messagebox.showwarning("Missing", "Please fill all fields")
        
        def update_row():
            selected = tree.selection()
            if not selected:
                messagebox.showinfo("Select", "Please select a prerequisite to update")
                return
            
            vals = [entries[lbl].get().strip() for lbl in labels]
            if not all(vals):
                messagebox.showwarning("Missing", "Please fill all fields")
                return
            
            old_values = tree.item(selected[0], "values")
            old_course_id = old_values[0]
            
            if old_course_id != vals[0]:
                self._notify("Can't change Course ID!", "danger")
            else:
                res = update_prereq(old_course_id, vals[1])
                if res:
                    refresh_prereq_list()
                    reset_table()
                    self._notify(f"Prerequisite updated!")
                    clear_form()
        
        def del_row():
            selected = tree.selection()
            if selected:
                row = tree.item(selected[0], 'values')
                course_id = row[0]
                res = delete_prereq(course_id)
                if res:
                    refresh_prereq_list()
                    reset_table()
                    self._notify("Prerequisite deleted!")
                    clear_form()
            else:
                messagebox.showinfo("Select", "Please select a prerequisite first")
        
        ttk.Button(top_buttons, text="➕ ADD", command=add_row, width=12).pack(side=LEFT, padx=5)
        ttk.Button(top_buttons, text="✏ UPDATE", command=update_row, width=12).pack(side=LEFT, padx=5)
        ttk.Button(top_buttons, text="🗑 DELETE", command=del_row, width=12).pack(side=LEFT, padx=5)
        
        cols = ("course_id", "prereq_id")
        tree_frame = ttk.Frame(main)
        tree_frame.pack(fill=BOTH, expand=YES, pady=10)
        
        tree = ttk.Treeview(tree_frame, columns=cols, show="headings", height=15)
        for col in cols:
            tree.heading(col, text=col)
            tree.column(col, width=200)
        
        scroll = ttk.Scrollbar(tree_frame, orient=VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scroll.set)
        tree.pack(side=LEFT, fill=BOTH, expand=YES)
        scroll.pack(side=RIGHT, fill=Y)
        
        for row in PREREQ:
            tree.insert("", END, values=row)
        
        input_frame = ttk.LabelFrame(main, text="Prerequisite Details")
        input_frame.pack(fill=X, pady=10)
        
        entry_frame = ttk.Frame(input_frame)
        entry_frame.pack(pady=10)
        
        entries = {}
        labels = ["Course ID", "Prerequisite ID"]
        widths = [15, 15]
        
        for i, (lbl, w) in enumerate(zip(labels, widths)):
            f = ttk.Frame(entry_frame)
            f.pack(side=LEFT, padx=10)
            ttk.Label(f, text=lbl, font=("Segoe UI", 9, "bold")).pack()
            e = ttk.Entry(f, width=w)
            e.pack(pady=2)
            entries[lbl] = e
        
        def load_selected():
            selected = tree.selection()
            if selected:
                values = tree.item(selected[0], "values")
                for i, lbl in enumerate(labels):
                    if i < len(values):
                        entries[lbl].delete(0, tk.END)
                        entries[lbl].insert(0, values[i])
        
        tree.bind("<<TreeviewSelect>>", lambda e: load_selected())
        
        def clear_form():
            for e in entries.values():
                e.delete(0, tk.END)
        
        btn_frame = ttk.Frame(input_frame)
        btn_frame.pack(pady=10)
        ttk.Button(btn_frame, text="Clear", command=clear_form, width=12).pack(side=LEFT, padx=5)
        
        
    # ════════════════════════════════════════════
    #  ADVISOR PAGE
    # ════════════════════════════════════════════
    def _page_advisor(self):
        def refresh_advisor_list():
            global ADVISOR
            ADVISOR = []
            results = get_advisor()
            for (s_id, i_id) in results:
                ADVISOR.append((s_id, i_id))
        
        for w in self.main_frame.winfo_children():
            w.destroy()
        
        main = ttk.Frame(self.main_frame)
        main.pack(fill=BOTH, expand=YES, padx=10, pady=10)
        
        ttk.Label(main, text="🧑‍🏫 Advisor Management", font=("Segoe UI", 18, "bold")).pack(pady=10)
        
        search_frame = ttk.LabelFrame(main, text="Search Advisor")
        search_frame.pack(fill=X, padx=10, pady=5)
        
        search_entry_frame = ttk.Frame(search_frame)
        search_entry_frame.pack(pady=8)
        
        ttk.Label(search_entry_frame, text="Search by:").pack(side=LEFT, padx=5)
        search_var = tk.StringVar()
        search_entry = ttk.Entry(search_entry_frame, textvariable=search_var, width=15)
        search_entry.pack(side=LEFT, padx=5)
        
        def search_by_student():
            s_id = search_var.get().strip()
            if not s_id:
                messagebox.showwarning("Missing", "Please enter Student ID")
                return
            
            results = search_i_id_by_s_id(s_id)
            
            for item in tree.get_children():
                tree.delete(item)
            
            if results:
                for row in results:
                    tree.insert("", END, values=row)
                self._notify(f"Found {len(results)} advisors for student {s_id}")
            else:
                self._notify(f"No advisor found for student {s_id}", "warning")
        
        def search_by_instructor():
            i_id = search_var.get().strip()
            if not i_id:
                messagebox.showwarning("Missing", "Please enter Instructor ID")
                return
            
            results = search_s_id_by_i_id(i_id)
            
            for item in tree.get_children():
                tree.delete(item)
            
            if results:
                for row in results:
                    tree.insert("", END, values=row)
                self._notify(f"Found {len(results)} advisors for instructor {i_id}")
            else:
                self._notify(f"No advisors found for instructor {i_id}", "warning")
        
        def reset_table():
            search_var.set("")
            refresh_advisor_list()
            for item in tree.get_children():
                tree.delete(item)
            for row in ADVISOR:
                tree.insert("", END, values=row)
            self._notify("Table reset to full list")
        
        ttk.Button(search_entry_frame, text="🔍 Search by Student", command=search_by_student, width=16).pack(side=LEFT, padx=5)
        ttk.Button(search_entry_frame, text="🔍 Search by Instructor", command=search_by_instructor, width=16).pack(side=LEFT, padx=5)
        ttk.Button(search_entry_frame, text="🔄 Reset", command=reset_table, width=10).pack(side=LEFT, padx=5)
        
        top_buttons = ttk.Frame(main)
        top_buttons.pack(pady=5)
        
        def add_row():
            vals = [entries[lbl].get().strip() for lbl in labels]
            if all(vals):
                res = add_advisor(vals[0], vals[1])
                if res:
                    refresh_advisor_list()
                    reset_table()
                    self._notify("Advisor record saved!")
                    clear_form()
            else:
                messagebox.showwarning("Missing", "Please fill all fields")
        
        def update_row():
            selected = tree.selection()
            if not selected:
                messagebox.showinfo("Select", "Please select an advisor record to update")
                return
            
            vals = [entries[lbl].get().strip() for lbl in labels]
            if not all(vals):
                messagebox.showwarning("Missing", "Please fill all fields")
                return
            
            old_values = tree.item(selected[0], "values")
            old_s_id = old_values[0]
            
            if old_s_id != vals[0]:
                self._notify("Can't change Student ID!", "danger")
            else:
                res = update_advisor(old_s_id, vals[1])
                if res:
                    refresh_advisor_list()
                    reset_table()
                    self._notify(f"Advisor for student {old_s_id} updated!")
                    clear_form()
        
        def del_row():
            selected = tree.selection()
            if selected:
                row = tree.item(selected[0], 'values')
                s_id = row[0]
                res = delete_advisor(s_id)
                if res:
                    refresh_advisor_list()
                    reset_table()
                    self._notify("Advisor record deleted!")
                    clear_form()
            else:
                messagebox.showinfo("Select", "Please select a record first")
        
        ttk.Button(top_buttons, text="➕ ADD", command=add_row, width=12).pack(side=LEFT, padx=5)
        ttk.Button(top_buttons, text="✏ UPDATE", command=update_row, width=12).pack(side=LEFT, padx=5)
        ttk.Button(top_buttons, text="🗑 DELETE", command=del_row, width=12).pack(side=LEFT, padx=5)
        
        cols = ("student_id", "instructor_id")
        tree_frame = ttk.Frame(main)
        tree_frame.pack(fill=BOTH, expand=YES, pady=10)
        
        tree = ttk.Treeview(tree_frame, columns=cols, show="headings", height=15)
        for col in cols:
            tree.heading(col, text=col)
            tree.column(col, width=200)
        
        scroll = ttk.Scrollbar(tree_frame, orient=VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scroll.set)
        tree.pack(side=LEFT, fill=BOTH, expand=YES)
        scroll.pack(side=RIGHT, fill=Y)
        
        for row in ADVISOR:
            tree.insert("", END, values=row)
        
        input_frame = ttk.LabelFrame(main, text="Advisor Details")
        input_frame.pack(fill=X, pady=10)
        
        entry_frame = ttk.Frame(input_frame)
        entry_frame.pack(pady=10)
        
        entries = {}
        labels = ["Student ID", "Instructor ID"]
        widths = [15, 15]
        
        for i, (lbl, w) in enumerate(zip(labels, widths)):
            f = ttk.Frame(entry_frame)
            f.pack(side=LEFT, padx=10)
            ttk.Label(f, text=lbl, font=("Segoe UI", 9, "bold")).pack()
            e = ttk.Entry(f, width=w)
            e.pack(pady=2)
            entries[lbl] = e
        
        def load_selected():
            selected = tree.selection()
            if selected:
                values = tree.item(selected[0], "values")
                for i, lbl in enumerate(labels):
                    if i < len(values):
                        entries[lbl].delete(0, tk.END)
                        entries[lbl].insert(0, values[i])
        
        tree.bind("<<TreeviewSelect>>", lambda e: load_selected())
        
        def clear_form():
            for e in entries.values():
                e.delete(0, tk.END)
        
        btn_frame = ttk.Frame(input_frame)
        btn_frame.pack(pady=10)
        ttk.Button(btn_frame, text="Clear", command=clear_form, width=12).pack(side=LEFT, padx=5)

    # ════════════════════════════════════════════
    #  REPORT
    # ════════════════════════════════════════════
    def _page_reports(self):

        for w in self.main_frame.winfo_children():
            w.destroy()
        

        main = ttk.Frame(self.main_frame)
        main.pack(fill=BOTH, expand=YES, padx=10, pady=10)
        

        ttk.Label(main, text="📊 Reports & Analytics", 
                font=("Segoe UI", 18, "bold")).pack(pady=10)
        

        frame1 = ttk.LabelFrame(main, text="Students with Grade A")
        frame1.pack(fill=BOTH, expand=YES, pady=5, padx=5)
        
        cols1 = ("Student ID", "Student Name", "Department", "Course ID", "Course Title", "Grade")
        tree1 = ttk.Treeview(frame1, columns=cols1, show="headings", height=8)
        
        for col in cols1:
            tree1.heading(col, text=col)
            tree1.column(col, width=130)
        
        scroll1 = ttk.Scrollbar(frame1, orient=VERTICAL, command=tree1.yview)
        tree1.configure(yscrollcommand=scroll1.set)
        tree1.pack(side=LEFT, fill=BOTH, expand=YES, padx=5, pady=5)
        scroll1.pack(side=RIGHT, fill=Y, pady=5)
        
        def load_grade_a():
            for item in tree1.get_children():
                tree1.delete(item)
            
            try:
                results = get_best_grade()
                if results:
                    for row in results:
                        tree1.insert("", "end", values=row)
                else:
                    tree1.insert("", "end", values=("No data found", "", "", "", "", ""))
            except Exception as e:
                tree1.insert("", "end", values=(f"Error: {e}", "", "", "", "", ""))
        
        load_grade_a()
        
        frame2 = ttk.LabelFrame(main, text="Statistics per Department (Students & Courses)")
        frame2.pack(fill=BOTH, expand=YES, pady=5, padx=5)
        
        cols2 = ("Department", "Number of Students", "Number of Courses")
        tree2 = ttk.Treeview(frame2, columns=cols2, show="headings", height=8)
        
        for col in cols2:
            tree2.heading(col, text=col)
            tree2.column(col, width=200)
        
        scroll2 = ttk.Scrollbar(frame2, orient=VERTICAL, command=tree2.yview)
        tree2.configure(yscrollcommand=scroll2.set)
        tree2.pack(side=LEFT, fill=BOTH, expand=YES, padx=5, pady=5)
        scroll2.pack(side=RIGHT, fill=Y, pady=5)
        
        def load_stats():
            for item in tree2.get_children():
                tree2.delete(item)
            
            try:
                results = number_of_course_student_from_by_dept_name()
                if results:
                    for row in results:
                        tree2.insert("", "end", values=row)
                else:
                    tree2.insert("", "end", values=("No data found", "", ""))
            except Exception as e:
                tree2.insert("", "end", values=(f"Error: {e}", "", ""))
        
        load_stats()
        
        frame3 = ttk.LabelFrame(main, text="Instructors - Courses Taught & Total Credits")
        frame3.pack(fill=BOTH, expand=YES, pady=5, padx=5)
        
        cols3 = ("Instructor ID", "Instructor Name", "Department", "Number of Courses", "Total Credits")
        tree3 = ttk.Treeview(frame3, columns=cols3, show="headings", height=8)
        
        for col in cols3:
            tree3.heading(col, text=col)
            if col == "Instructor Name":
                tree3.column(col, width=160)
            elif col == "Department":
                tree3.column(col, width=140)
            else:
                tree3.column(col, width=120)
        
        scroll3 = ttk.Scrollbar(frame3, orient=VERTICAL, command=tree3.yview)
        tree3.configure(yscrollcommand=scroll3.set)
        tree3.pack(side=LEFT, fill=BOTH, expand=YES, padx=5, pady=5)
        scroll3.pack(side=RIGHT, fill=Y, pady=5)
        
        def load_instructor_stats():
            for item in tree3.get_children():
                tree3.delete(item)
            
            try:
                results = get_instructor_with_amount_of_course_credits()
                if results:
                    for row in results:
                        tree3.insert("", "end", values=row)
                else:
                    tree3.insert("", "end", values=("No data found", "", "", "", ""))
            except Exception as e:
                tree3.insert("", "end", values=(f"Error: {e}", "", "", "", ""))
        
        load_instructor_stats()


    # ════════════════════════════════════════════
    #  HELPERS
    # ════════════════════════════════════════════
    def _make_tree(self, parent, cols, height=8):
        frame = ttk.Frame(parent)
        frame.pack(fill=BOTH, expand=YES, padx=20, pady=4)
        tree = ttk.Treeview(frame, columns=cols, show="headings", height=height)
        for col in cols:
            tree.heading(col, text=col, anchor=W)
            tree.column(col, anchor=W, width=max(80, len(col)*12))
        vsb = ttk.Scrollbar(frame, orient=VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=vsb.set)
        tree.pack(side=LEFT, fill=BOTH, expand=YES)
        vsb.pack(side=RIGHT, fill=Y)
        return tree

    def _notify(self, msg, bootstyle="success"):
        toast = ToastNotification(title="Success" if bootstyle == "success" else "Error", 
                                message=msg, duration=2500,
                                bootstyle=bootstyle, position=(20, 60, "se"))
        toast.show_toast()
        self.status_var.set(msg)

    def _on_exit(self):
        if messagebox.askyesno("Exit", "Are you sure you want to exit?"):
            self.destroy()
            
            
# ─────────────────────────────────────────────
if __name__ == "__main__":
    app = UniversityApp()
    app.mainloop()