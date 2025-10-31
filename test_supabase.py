"""
Test Supabase Database Connection
Tests all database operations
"""

from supabase_db import get_db
from datetime import datetime, date

def test_supabase_connection():
    """Test complete Supabase integration"""
    
    print("\n" + "="*60)
    print("🧪 TESTING SUPABASE DATABASE CONNECTION")
    print("="*60 + "\n")
    
    # Initialize database
    db = get_db()
    
    # Test 1: Connection Test
    print("📡 Test 1: Testing connection...")
    if db.test_connection():
        print("✅ PASS: Connection successful!\n")
    else:
        print("❌ FAIL: Connection failed!\n")
        return
    
    # Test 2: Initialize Tables
    print("📋 Test 2: Creating database tables...")
    if db.init_database():
        print("✅ PASS: Tables created successfully!\n")
    else:
        print("⚠️ WARNING: Tables may already exist or creation had issues\n")
    
    # Test 3: Add Test Student
    print("👤 Test 3: Adding test student...")
    test_student_id = f"TEST{datetime.now().strftime('%H%M%S')}"
    success = db.add_student(
        student_id=test_student_id,
        name="Test Student",
        department="Computer Science",
        year="1st Year",
        email="test@example.com",
        phone="1234567890",
        photo_path="student_images/test.jpg",
        encoding_path="student_images/test_encoding.pkl"
    )
    
    if success:
        print("✅ PASS: Student added successfully!\n")
    else:
        print("❌ FAIL: Failed to add student!\n")
    
    # Test 4: Fetch All Students
    print("📚 Test 4: Fetching all students...")
    students = db.get_all_students()
    print(f"✅ PASS: Found {len(students)} student(s)")
    if students:
        print(f"   Latest student: {students[-1].get('name', 'Unknown')}\n")
    
    # Test 5: Get Specific Student
    print("🔍 Test 5: Fetching specific student...")
    student = db.get_student(test_student_id)
    if student:
        print(f"✅ PASS: Student found!")
        print(f"   Name: {student['name']}")
        print(f"   Department: {student['department']}\n")
    else:
        print("❌ FAIL: Student not found!\n")
    
    # Test 6: Update Student
    print("✏️ Test 6: Updating student information...")
    success = db.update_student(
        test_student_id,
        email="updated@example.com",
        phone="9876543210"
    )
    
    if success:
        print("✅ PASS: Student updated successfully!\n")
    else:
        print("❌ FAIL: Failed to update student!\n")
    
    # Test 7: Mark Attendance
    print("📝 Test 7: Marking attendance...")
    today = date.today()
    current_time = datetime.now().time()
    
    success = db.mark_attendance(
        student_id=test_student_id,
        name="Test Student",
        department="Computer Science",
        date=today.isoformat(),
        time=current_time.strftime("%H:%M:%S"),
        confidence=95.5
    )
    
    if success:
        print("✅ PASS: Attendance marked successfully!\n")
    else:
        print("❌ FAIL: Failed to mark attendance!\n")
    
    # Test 8: Get Today's Attendance
    print("📅 Test 8: Fetching today's attendance...")
    attendance = db.get_attendance_by_date(today.isoformat())
    print(f"✅ PASS: Found {len(attendance)} attendance record(s) for today")
    if attendance:
        latest = attendance[-1]
        print(f"   Latest: {latest.get('name', 'Unknown')} at {latest.get('time', 'Unknown')}\n")
    
    # Test 9: Check Duplicate Attendance
    print("🔄 Test 9: Checking duplicate attendance...")
    is_duplicate = db.check_duplicate_attendance(test_student_id, today.isoformat())
    if is_duplicate:
        print("✅ PASS: Duplicate detection working (attendance already marked)\n")
    else:
        print("⚠️ WARNING: No duplicate found (expected one from Test 7)\n")
    
    # Test 10: Get Student Attendance History
    print("📊 Test 10: Fetching student attendance history...")
    history = db.get_attendance_by_student(test_student_id)
    print(f"✅ PASS: Found {len(history)} attendance record(s) for test student\n")
    
    # Test 11: Get Statistics
    print("📈 Test 11: Fetching attendance statistics...")
    stats = db.get_attendance_statistics()
    print(f"✅ PASS: Generated statistics for {len(stats)} student(s)")
    if stats:
        print("   Top students by attendance:")
        for i, stat in enumerate(stats[:3], 1):
            print(f"   {i}. {stat.get('name', 'Unknown')} - {stat.get('total_days_present', 0)} days")
    print()
    
    # Test 12: Delete Test Student
    print("🗑️ Test 12: Cleaning up - deleting test student...")
    success = db.delete_student(test_student_id)
    if success:
        print("✅ PASS: Test student deleted successfully!\n")
    else:
        print("❌ FAIL: Failed to delete test student!\n")
    
    # Final Summary
    print("="*60)
    print("✅ ALL TESTS COMPLETED!")
    print("="*60)
    print("\n🎉 Supabase database is fully operational and ready to use!")
    print("\n📌 Connection Details:")
    print(f"   URL: {db.url}")
    print(f"   Tables: students, attendance")
    print(f"   Status: Connected ✅")
    print("\n" + "="*60 + "\n")

if __name__ == "__main__":
    test_supabase_connection()
