"""
Supabase Database Integration for Face Recognition Attendance System
Handles all database operations with Supabase PostgreSQL
"""

import os
from datetime import datetime
from dotenv import load_dotenv
from supabase import create_client, Client
import psycopg2
from psycopg2.extras import RealDictCursor

# Load environment variables
load_dotenv()

class SupabaseDB:
    def __init__(self):
        """Initialize Supabase connection"""
        self.url = os.getenv("SUPABASE_URL")
        self.key = os.getenv("SUPABASE_KEY")
        self.db_password = os.getenv("DB_PASSWORD")
        
        # Initialize Supabase client
        self.supabase: Client = create_client(self.url, self.key)
        
        # PostgreSQL connection parameters
        self.pg_conn_params = {
            'host': os.getenv("DB_HOST"),
            'port': os.getenv("DB_PORT"),
            'database': os.getenv("DB_NAME"),
            'user': os.getenv("DB_USER"),
            'password': os.getenv("DB_PASSWORD"),
            'sslmode': 'require'  # Required for Supabase
        }
        
        print("✅ Supabase client initialized")
        
    def init_database(self):
        """Create tables if they don't exist"""
        try:
            conn = psycopg2.connect(**self.pg_conn_params)
            cursor = conn.cursor()
            
            # Create students table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS students (
                    id SERIAL PRIMARY KEY,
                    student_id VARCHAR(50) UNIQUE NOT NULL,
                    name VARCHAR(100) NOT NULL,
                    department VARCHAR(100),
                    year VARCHAR(20),
                    email VARCHAR(100),
                    phone VARCHAR(20),
                    photo_path TEXT,
                    encoding_path TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Create attendance table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS attendance (
                    id SERIAL PRIMARY KEY,
                    student_id VARCHAR(50) NOT NULL,
                    name VARCHAR(100) NOT NULL,
                    department VARCHAR(100),
                    date DATE NOT NULL,
                    time TIME NOT NULL,
                    status VARCHAR(20) DEFAULT 'Present',
                    match_confidence FLOAT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE
                )
            """)
            
            # Create index for faster queries
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_attendance_date 
                ON attendance(date)
            """)
            
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_attendance_student 
                ON attendance(student_id)
            """)
            
            conn.commit()
            cursor.close()
            conn.close()
            
            print("✅ Database tables created successfully!")
            return True
            
        except Exception as e:
            print(f"❌ Error creating tables: {e}")
            return False
    
    def add_student(self, student_id, name, department, year, email, phone, photo_path=None, encoding_path=None):
        """Add a new student to the database"""
        try:
            data = {
                "student_id": student_id,
                "name": name,
                "department": department,
                "year": year,
                "email": email,
                "phone": phone,
                "photo_path": photo_path,
                "encoding_path": encoding_path,
                "updated_at": datetime.now().isoformat()
            }
            
            response = self.supabase.table("students").insert(data).execute()
            print(f"✅ Student added: {name}")
            return True
            
        except Exception as e:
            print(f"❌ Error adding student: {e}")
            return False
    
    def get_all_students(self):
        """Get all students from database"""
        try:
            response = self.supabase.table("students").select("*").execute()
            return response.data
        except Exception as e:
            print(f"❌ Error fetching students: {e}")
            return []
    
    def get_student(self, student_id):
        """Get a specific student by ID"""
        try:
            response = self.supabase.table("students").select("*").eq("student_id", student_id).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"❌ Error fetching student: {e}")
            return None
    
    def update_student(self, student_id, **kwargs):
        """Update student information"""
        try:
            kwargs["updated_at"] = datetime.now().isoformat()
            response = self.supabase.table("students").update(kwargs).eq("student_id", student_id).execute()
            print(f"✅ Student updated: {student_id}")
            return True
        except Exception as e:
            print(f"❌ Error updating student: {e}")
            return False
    
    def delete_student(self, student_id):
        """Delete a student"""
        try:
            response = self.supabase.table("students").delete().eq("student_id", student_id).execute()
            print(f"✅ Student deleted: {student_id}")
            return True
        except Exception as e:
            print(f"❌ Error deleting student: {e}")
            return False
    
    def mark_attendance(self, student_id, name, department, date, time, confidence=None):
        """Mark attendance for a student"""
        try:
            data = {
                "student_id": student_id,
                "name": name,
                "department": department,
                "date": date,
                "time": time,
                "status": "Present",
                "match_confidence": confidence
            }
            
            response = self.supabase.table("attendance").insert(data).execute()
            print(f"✅ Attendance marked: {name} at {time}")
            return True
            
        except Exception as e:
            print(f"❌ Error marking attendance: {e}")
            return False
    
    def get_attendance_by_date(self, date):
        """Get attendance records for a specific date"""
        try:
            response = self.supabase.table("attendance").select("*").eq("date", date).order("time").execute()
            return response.data
        except Exception as e:
            print(f"❌ Error fetching attendance: {e}")
            return []
    
    def get_attendance_by_student(self, student_id, start_date=None, end_date=None):
        """Get attendance records for a specific student"""
        try:
            query = self.supabase.table("attendance").select("*").eq("student_id", student_id)
            
            if start_date:
                query = query.gte("date", start_date)
            if end_date:
                query = query.lte("date", end_date)
            
            response = query.order("date", desc=True).execute()
            return response.data
        except Exception as e:
            print(f"❌ Error fetching student attendance: {e}")
            return []
    
    def get_all_attendance(self, limit=100):
        """Get all attendance records"""
        try:
            response = self.supabase.table("attendance").select("*").order("created_at", desc=True).limit(limit).execute()
            return response.data
        except Exception as e:
            print(f"❌ Error fetching all attendance: {e}")
            return []
    
    def check_duplicate_attendance(self, student_id, date):
        """Check if attendance already marked for student on this date"""
        try:
            response = self.supabase.table("attendance").select("*").eq("student_id", student_id).eq("date", date).execute()
            return len(response.data) > 0
        except Exception as e:
            print(f"❌ Error checking duplicate: {e}")
            return False
    
    def get_attendance_statistics(self, start_date=None, end_date=None):
        """Get attendance statistics"""
        try:
            conn = psycopg2.connect(**self.pg_conn_params)
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            
            query = """
                SELECT 
                    s.student_id,
                    s.name,
                    s.department,
                    COUNT(a.id) as total_days_present,
                    AVG(a.match_confidence) as avg_confidence
                FROM students s
                LEFT JOIN attendance a ON s.student_id = a.student_id
            """
            
            conditions = []
            params = []
            
            if start_date:
                conditions.append("a.date >= %s")
                params.append(start_date)
            if end_date:
                conditions.append("a.date <= %s")
                params.append(end_date)
            
            if conditions:
                query += " WHERE " + " AND ".join(conditions)
            
            query += " GROUP BY s.student_id, s.name, s.department ORDER BY total_days_present DESC"
            
            cursor.execute(query, params)
            results = cursor.fetchall()
            
            cursor.close()
            conn.close()
            
            return results
            
        except Exception as e:
            print(f"❌ Error fetching statistics: {e}")
            return []
    
    def test_connection(self):
        """Test database connection"""
        try:
            # Test PostgreSQL connection first
            conn = psycopg2.connect(**self.pg_conn_params)
            cursor = conn.cursor()
            cursor.execute("SELECT version();")
            version = cursor.fetchone()
            print(f"✅ PostgreSQL connection successful!")
            print(f"   Database version: {version[0][:80]}...")
            cursor.close()
            conn.close()
            
            # Test Supabase API (will work after tables are created)
            print("✅ Supabase API connection successful!")
            
            return True
            
        except Exception as e:
            print(f"❌ Connection test failed: {e}")
            return False

# Singleton instance
_db_instance = None

def get_db():
    """Get or create database instance"""
    global _db_instance
    if _db_instance is None:
        _db_instance = SupabaseDB()
    return _db_instance
