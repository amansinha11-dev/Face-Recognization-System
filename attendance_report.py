"""
Attendance Report System with Excel Export
"""
from tkinter import *
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk
import os
import csv
from datetime import datetime
import pandas as pd

class AttendanceReport:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1530x790+0+0")
        self.root.title("Attendance Report System")
        
        # Title
        title_lbl = Label(self.root, text="ATTENDANCE REPORT SYSTEM", 
                         font=("times new roman", 35, "bold"), bg="white", fg="darkgreen")
        title_lbl.place(x=0, y=0, width=1530, height=45)
        
        # Main Frame
        main_frame = Frame(self.root, bd=2, bg="white")
        main_frame.place(x=10, y=55, width=1510, height=730)
        
        # Left Frame - Search & Filters
        Left_frame = LabelFrame(main_frame, bd=2, bg="white", relief=RIDGE, 
                               text="Search & Filter", font=("times new roman", 12, "bold"))
        Left_frame.place(x=10, y=10, width=400, height=710)
        
        # Search by Date
        date_label = Label(Left_frame, text="Search by Date:", font=("Arial", 12, "bold"), bg="white")
        date_label.grid(row=0, column=0, padx=10, pady=10, sticky=W)
        
        self.search_date = Entry(Left_frame, font=("Arial", 12), width=25)
        self.search_date.grid(row=0, column=1, padx=10, pady=10)
        self.search_date.insert(0, datetime.now().strftime("%d/%m/%Y"))
        
        # Search by Name
        name_label = Label(Left_frame, text="Search by Name:", font=("Arial", 12, "bold"), bg="white")
        name_label.grid(row=1, column=0, padx=10, pady=10, sticky=W)
        
        self.search_name = Entry(Left_frame, font=("Arial", 12), width=25)
        self.search_name.grid(row=1, column=1, padx=10, pady=10)
        
        # Search by ID
        id_label = Label(Left_frame, text="Search by ID:", font=("Arial", 12, "bold"), bg="white")
        id_label.grid(row=2, column=0, padx=10, pady=10, sticky=W)
        
        self.search_id = Entry(Left_frame, font=("Arial", 12), width=25)
        self.search_id.grid(row=2, column=1, padx=10, pady=10)
        
        # Search by Department
        dept_label = Label(Left_frame, text="Department:", font=("Arial", 12, "bold"), bg="white")
        dept_label.grid(row=3, column=0, padx=10, pady=10, sticky=W)
        
        self.search_dept = ttk.Combobox(Left_frame, font=("Arial", 12), width=23, state="readonly")
        self.search_dept['values'] = ("All", "Computer Science", "IT", "Electronics", "Mechanical", "Civil")
        self.search_dept.current(0)
        self.search_dept.grid(row=3, column=1, padx=10, pady=10)
        
        # Buttons
        btn_frame = Frame(Left_frame, bg="white")
        btn_frame.place(x=20, y=200, width=360, height=450)
        
        # Search Button
        search_btn = Button(btn_frame, text="Search Records", command=self.search_records,
                           font=("Arial", 13, "bold"), bg="blue", fg="white", cursor="hand2")
        search_btn.grid(row=0, column=0, padx=5, pady=10, sticky=W+E)
        
        # Show All Button
        show_all_btn = Button(btn_frame, text="Show All Records", command=self.fetch_data,
                             font=("Arial", 13, "bold"), bg="green", fg="white", cursor="hand2")
        show_all_btn.grid(row=1, column=0, padx=5, pady=10, sticky=W+E)
        
        # Export to Excel Button
        export_btn = Button(btn_frame, text="Export to Excel", command=self.export_to_excel,
                           font=("Arial", 13, "bold"), bg="orange", fg="white", cursor="hand2")
        export_btn.grid(row=2, column=0, padx=5, pady=10, sticky=W+E)
        
        # Generate Report Button
        report_btn = Button(btn_frame, text="Generate PDF Report", command=self.generate_pdf_report,
                           font=("Arial", 13, "bold"), bg="purple", fg="white", cursor="hand2")
        report_btn.grid(row=3, column=0, padx=5, pady=10, sticky=W+E)
        
        # Delete Record Button
        delete_btn = Button(btn_frame, text="Delete Record", command=self.delete_record,
                           font=("Arial", 13, "bold"), bg="red", fg="white", cursor="hand2")
        delete_btn.grid(row=4, column=0, padx=5, pady=10, sticky=W+E)
        
        # Reset Button
        reset_btn = Button(btn_frame, text="Reset Filters", command=self.reset_filters,
                          font=("Arial", 13, "bold"), bg="gray", fg="white", cursor="hand2")
        reset_btn.grid(row=5, column=0, padx=5, pady=10, sticky=W+E)
        
        # Statistics Frame
        stats_frame = LabelFrame(btn_frame, text="Statistics", font=("Arial", 11, "bold"),
                                bg="white", relief=RIDGE, bd=2)
        stats_frame.place(x=0, y=350, width=340, height=90)
        
        self.total_label = Label(stats_frame, text="Total Records: 0", font=("Arial", 10, "bold"),
                                bg="white", fg="blue")
        self.total_label.pack(pady=5)
        
        self.present_label = Label(stats_frame, text="Present: 0", font=("Arial", 10, "bold"),
                                  bg="white", fg="green")
        self.present_label.pack(pady=5)
        
        # Right Frame - Table
        Right_frame = LabelFrame(main_frame, bd=2, bg="white", relief=RIDGE, 
                                text="Attendance Records", font=("times new roman", 12, "bold"))
        Right_frame.place(x=420, y=10, width=1080, height=710)
        
        # Table Frame
        table_frame = Frame(Right_frame, bd=2, bg="white", relief=RIDGE)
        table_frame.place(x=5, y=5, width=1065, height=690)
        
        # Scrollbars
        scroll_x = ttk.Scrollbar(table_frame, orient=HORIZONTAL)
        scroll_y = ttk.Scrollbar(table_frame, orient=VERTICAL)
        
        # Table
        self.AttendanceReportTable = ttk.Treeview(table_frame, 
            columns=("id", "roll", "name", "department", "time", "date", "attendance"), 
            xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)
        
        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.config(command=self.AttendanceReportTable.xview)
        scroll_y.config(command=self.AttendanceReportTable.yview)
        
        # Table Headings
        self.AttendanceReportTable.heading("id", text="Student ID")
        self.AttendanceReportTable.heading("roll", text="Roll No")
        self.AttendanceReportTable.heading("name", text="Name")
        self.AttendanceReportTable.heading("department", text="Department")
        self.AttendanceReportTable.heading("time", text="Time")
        self.AttendanceReportTable.heading("date", text="Date")
        self.AttendanceReportTable.heading("attendance", text="Status")
        
        self.AttendanceReportTable["show"] = "headings"
        
        # Column Widths
        self.AttendanceReportTable.column("id", width=100)
        self.AttendanceReportTable.column("roll", width=100)
        self.AttendanceReportTable.column("name", width=200)
        self.AttendanceReportTable.column("department", width=150)
        self.AttendanceReportTable.column("time", width=100)
        self.AttendanceReportTable.column("date", width=100)
        self.AttendanceReportTable.column("attendance", width=100)
        
        self.AttendanceReportTable.pack(fill=BOTH, expand=1)
        self.AttendanceReportTable.bind("<ButtonRelease>", self.get_cursor)
        
        # Load data
        self.fetch_data()
    
    def fetch_data(self):
        """Fetch all attendance data"""
        self.AttendanceReportTable.delete(*self.AttendanceReportTable.get_children())
        
        try:
            if os.path.exists("attendance.csv"):
                with open("attendance.csv", "r") as file:
                    reader = csv.reader(file)
                    data = list(reader)
                    
                    if len(data) > 0:
                        for row in data:
                            if len(row) >= 7:
                                self.AttendanceReportTable.insert("", END, values=row)
                        
                        # Update statistics
                        total = len(data)
                        present = sum(1 for row in data if len(row) >= 7 and row[6] == "Present")
                        self.total_label.config(text=f"Total Records: {total}")
                        self.present_label.config(text=f"Present: {present}")
        except Exception as e:
            messagebox.showerror("Error", f"Error loading data: {str(e)}", parent=self.root)
    
    def search_records(self):
        """Search records based on filters"""
        self.AttendanceReportTable.delete(*self.AttendanceReportTable.get_children())
        
        try:
            if os.path.exists("attendance.csv"):
                with open("attendance.csv", "r") as file:
                    reader = csv.reader(file)
                    data = list(reader)
                    
                    search_date = self.search_date.get().strip()
                    search_name = self.search_name.get().strip().lower()
                    search_id = self.search_id.get().strip()
                    search_dept = self.search_dept.get()
                    
                    filtered_data = []
                    for row in data:
                        if len(row) >= 7:
                            match = True
                            
                            if search_date and row[5] != search_date:
                                match = False
                            if search_name and search_name not in row[2].lower():
                                match = False
                            if search_id and row[0] != search_id:
                                match = False
                            if search_dept != "All" and row[3] != search_dept:
                                match = False
                            
                            if match:
                                filtered_data.append(row)
                                self.AttendanceReportTable.insert("", END, values=row)
                    
                    # Update statistics
                    total = len(filtered_data)
                    present = sum(1 for row in filtered_data if row[6] == "Present")
                    self.total_label.config(text=f"Total Records: {total}")
                    self.present_label.config(text=f"Present: {present}")
                    
                    if total == 0:
                        messagebox.showinfo("Info", "No records found matching the criteria", parent=self.root)
        except Exception as e:
            messagebox.showerror("Error", f"Error searching data: {str(e)}", parent=self.root)
    
    def export_to_excel(self):
        """Export attendance data to Excel file"""
        try:
            if not os.path.exists("attendance.csv"):
                messagebox.showerror("Error", "No attendance data found!", parent=self.root)
                return
            
            # Read CSV data
            df = pd.read_csv("attendance.csv", names=["ID", "Roll", "Name", "Department", "Time", "Date", "Status"])
            
            # Ask user for save location
            file_path = filedialog.asksaveasfilename(
                defaultextension=".xlsx",
                filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")],
                initialfile=f"Attendance_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            )
            
            if file_path:
                # Export to Excel with formatting
                with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
                    df.to_excel(writer, sheet_name='Attendance', index=False)
                    
                    # Get the workbook and worksheet
                    workbook = writer.book
                    worksheet = writer.sheets['Attendance']
                    
                    # Adjust column widths
                    for column in worksheet.columns:
                        max_length = 0
                        column_letter = column[0].column_letter
                        for cell in column:
                            try:
                                if len(str(cell.value)) > max_length:
                                    max_length = len(cell.value)
                            except:
                                pass
                        adjusted_width = (max_length + 2)
                        worksheet.column_dimensions[column_letter].width = adjusted_width
                
                messagebox.showinfo("Success", f"Data exported successfully to:\n{file_path}", parent=self.root)
                
                # Ask if user wants to open the file
                if messagebox.askyesno("Open File", "Do you want to open the exported file?", parent=self.root):
                    os.startfile(file_path)
        except ImportError:
            messagebox.showerror("Error", "pandas and openpyxl are required for Excel export.\n\nInstall using:\npip install pandas openpyxl", parent=self.root)
        except Exception as e:
            messagebox.showerror("Error", f"Error exporting to Excel: {str(e)}", parent=self.root)
    
    def generate_pdf_report(self):
        """Generate PDF report (placeholder - requires reportlab)"""
        messagebox.showinfo("Info", "PDF report generation feature will be implemented with reportlab library.\n\nFor now, please use Excel export.", parent=self.root)
    
    def delete_record(self):
        """Delete selected record"""
        try:
            selected_item = self.AttendanceReportTable.selection()
            if not selected_item:
                messagebox.showerror("Error", "Please select a record to delete", parent=self.root)
                return
            
            values = self.AttendanceReportTable.item(selected_item)['values']
            
            if messagebox.askyesno("Confirm", f"Are you sure you want to delete this record?\n\nName: {values[2]}\nDate: {values[5]}", parent=self.root):
                # Read all data
                with open("attendance.csv", "r") as file:
                    data = file.readlines()
                
                # Write back without the deleted record
                with open("attendance.csv", "w") as file:
                    for line in data:
                        if not all(str(val) in line for val in values[:4]):
                            file.write(line)
                
                messagebox.showinfo("Success", "Record deleted successfully", parent=self.root)
                self.fetch_data()
        except Exception as e:
            messagebox.showerror("Error", f"Error deleting record: {str(e)}", parent=self.root)
    
    def reset_filters(self):
        """Reset all search filters"""
        self.search_date.delete(0, END)
        self.search_date.insert(0, datetime.now().strftime("%d/%m/%Y"))
        self.search_name.delete(0, END)
        self.search_id.delete(0, END)
        self.search_dept.current(0)
        self.fetch_data()
    
    def get_cursor(self, event=""):
        """Get selected row data"""
        cursor_row = self.AttendanceReportTable.focus()
        content = self.AttendanceReportTable.item(cursor_row)
        row = content['values']
        
        if row:
            self.search_id.delete(0, END)
            self.search_id.insert(0, row[0])
            self.search_name.delete(0, END)
            self.search_name.insert(0, row[2])


if __name__ == "__main__":
    root = Tk()
    app = AttendanceReport(root)
    root.mainloop()
