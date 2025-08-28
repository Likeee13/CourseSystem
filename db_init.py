### db_init.py
import sqlite3

def init_db():
    conn = sqlite3.connect('CourseSystem.db')
    cursor = conn.cursor()

    # 用户表
    cursor.execute('''CREATE TABLE IF NOT EXISTS user(
        sid TEXT PRIMARY KEY,
        password TEXT UNIQUE NOT NULL,
        is_admin INTEGER DEFAULT 0
    )''')

    # 课程表
    cursor.execute('''CREATE TABLE IF NOT EXISTS course (
        cid TEXT PRIMARY KEY,
        name TEXT,
        -- 假设课程的时间范围为第一节课到第十节课
        time_slot INTEGER CHECK (time_slot >=1 AND time_slot <=10),  
        -- 假设有3间教室
        room TEXT CHECK (room IN ('101', '102', '103')),   
        exam_time TEXT,
        UNIQUE(time_slot, room)
    )''')

    # 选课表
    cursor.execute('''CREATE TABLE IF NOT EXISTS enrollment (
        sid TEXT,
        cid TEXT,
        PRIMARY KEY (sid, cid)
    )''')

    # 成绩表
    cursor.execute('''CREATE TABLE IF NOT EXISTS score (
        sid TEXT,
        cid TEXT,
        score INTEGER DEFALUT NULL CHECK ((score >= 0 AND score <= 100) OR score is NULL),
        PRIMARY KEY (sid, cid)
    )''')

    # 预置一些数据
    try:
        cursor.execute("INSERT INTO user (sid, password, is_admin) VALUES (?, ?, ?)", ('admin', 'admin123', 1))
    except:
        pass
    try:
        cursor.executemany("INSERT INTO course VALUES (?, ?, ?, ?, ?)", [
            ('C001', 'Python编程', 1, '101', '2025-06-01 09:00'),
            ('C002', '数据库系统', 3, '102', '2025-06-05 14:00'),
            ('C003', '数值分析', 5, '101', '2025-06-07 09:00'),
            ('C004', '操作系统原理', 6, '101', '2025-06-08 09:00'),
            ('C005', '概率论与随机过程', 2, '103', '2025-06-07 15:00'),
            ('C006', '计算机组织与结构', 3, '101', '2025-06-11 09:00')
        ])
        cursor.executemany("INSERT INTO enrollment VALUES (?, ?)", [
            ('S001', 'C001'),
            ('S001', 'C002'),
            ('S001', 'C004'),
            ('S002', 'C003'),
            ('S002', 'C005')
        ])
        cursor.executemany("INSERT INTO score VALUES (?, ?, ?)", [
            ('S001', 'C001', 85),
            ('S001', 'C002', 70),
            ('S001', 'C004', 90),
            ('S002', 'C003', 66),
            ('S002', 'C005', 59),
            ('S002', 'C001', 51),
        ])
    except:
        pass

    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()