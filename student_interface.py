import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from db_utils import fetch_all
import tkinter as tk

def StudentInterface(sid):
    # 安全创建函数
    def safe_create(creator, *args, **kwargs):
        """安全创建GUI组件的封装函数"""
        if not root or not root.winfo_exists():
            return None
            
        try:
            return creator(*args, **kwargs)
        except tk.TclError as e:
            if "application has been destroyed" in str(e):
                return None
            raise

    # 表格创建函数（安全增强版）
    def create_table(parent, columns, query, params=()):
        """创建表格视图的通用函数"""
        # 检查父窗口有效性
        if not parent or not parent.winfo_exists():
            return None
            
        # 安全创建子窗口
        win = safe_create(ttk.Toplevel, parent)
        if not win: return None
        win.title("数据表格")
        win.geometry("960x720")
        
        # 安全创建框架
        frame = safe_create(ttk.Frame, win)
        if not frame: 
            win.destroy()
            return None
        frame.pack(fill=BOTH, expand=True, padx=20, pady=20)
        
        # 安全创建表格
        tree = safe_create(ttk.Treeview, frame,
                          columns=columns, 
                          show="headings",
                          bootstyle=PRIMARY,
                          height=15)
        if not tree: 
            win.destroy()
            return None
            
        # 设置列标题
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150, anchor=CENTER)
        
        # 安全创建滚动条（关键修复点）
        scrollbar = safe_create(ttk.Scrollbar, frame, 
                              orient=VERTICAL, 
                              command=tree.yview)
        
        if scrollbar:
            tree.configure(yscrollcommand=scrollbar.set)
            scrollbar.pack(side=RIGHT, fill=Y)
            tree.pack(fill=BOTH, expand=True)
        else:
            # 降级方案：无滚动条显示
            tree.pack(fill=BOTH, expand=True)
        
        # 查询并填充数据
        rows = fetch_all(query, params)
        for row in rows:
            tree.insert("", END, values=row)
        
        return win

    # 功能函数
    def view_courses():
        if not root or not root.winfo_exists(): return
        create_table(
            root, 
            columns=("课程名称", "上课时间", "教室"), 
            query="SELECT course.name, course.time_slot, course.room FROM enrollment " 
                  "JOIN course ON enrollment.cid=course.cid WHERE enrollment.sid=? " 
                  "ORDER BY course.time_slot",
            params=(sid,)
        )

    def view_exam_schedule():
        if not root or not root.winfo_exists(): return
        create_table(
            root, 
            columns=("课程名称", "考试时间", "考试地点"), 
            query="SELECT course.name, course.exam_time, course.room FROM enrollment " 
                  "JOIN course ON enrollment.cid=course.cid WHERE enrollment.sid=? " 
                  "ORDER BY course.exam_time",
            params=(sid,)
        )

    def view_empty_rooms():
        if not root or not root.winfo_exists(): return
        win = safe_create(ttk.Toplevel, root)
        if not win: return
            
        win.title("空闲教室")
        frame = safe_create(ttk.Frame, win, padding=20)
        if not frame: 
            win.destroy()
            return
        frame.pack(fill=BOTH, expand=True)
        
        # 获取数据
        busy = fetch_all("SELECT DISTINCT time_slot, room FROM course")
        all_rooms = ['101', '102', '103']
        all_slots = range(1, 11)
        used = set((slot, room) for slot, room in busy)
        empty_rooms_by_slot = {}
        
        for slot in all_slots:
            empty_rooms = []
            for room in all_rooms:
                if (slot, room) not in used:
                    empty_rooms.append(room)
            if empty_rooms:
                empty_rooms_by_slot[slot] = empty_rooms
        
        # 安全创建表格
        tree = safe_create(ttk.Treeview, frame,
                          columns=("时间段", "空闲教室"),
                          show="headings",
                          bootstyle=INFO,
                          height=10)
        if not tree:
            win.destroy()
            return
            
        tree.heading("时间段", text="时间段")
        tree.heading("空闲教室", text="空闲教室")
        tree.column("时间段", width=150, anchor=CENTER)
        tree.column("空闲教室", width=300, anchor=CENTER)
        
        # 填充数据
        for slot, rooms in empty_rooms_by_slot.items():
            tree.insert("", END, values=(f"第{slot}节课", ", ".join(rooms)))
        
        # 安全创建滚动条
        scrollbar = safe_create(ttk.Scrollbar, frame, 
                              orient=VERTICAL, 
                              command=tree.yview)
        if scrollbar:
            tree.configure(yscrollcommand=scrollbar.set)
            scrollbar.pack(side=RIGHT, fill=Y)
            tree.pack(fill=BOTH, expand=True)
        else:
            tree.pack(fill=BOTH, expand=True)

    def view_scores():
        if not root or not root.winfo_exists(): return
        create_table(
            root, 
            columns=("课程名称", "成绩"), 
            query="SELECT course.name, score.score FROM score " 
                  "JOIN course ON score.cid=course.cid WHERE score.sid=?",
            params=(sid,)
        )

    # 创建主窗口
    root = ttk.Window(themename="morph")
    root.title(f"学生功能界面 - {sid}")
    root.geometry("720x560")
    
    # 安全关闭处理
    def on_closing():
        if root and root.winfo_exists():
            root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    
    # 主界面布局
    main_frame = safe_create(ttk.Frame, root, padding=20)
    if not main_frame:
        root.destroy()
        return
    main_frame.pack(fill=BOTH, expand=True)
    
    # 标题
    title_label = safe_create(ttk.Label, main_frame, 
                             text=f"欢迎, {sid}",
                             font=("Helvetica", 16, "bold"),
                             bootstyle=PRIMARY)
    if title_label:
        title_label.pack(pady=20)
    
    # 功能按钮
    buttons = [
        ("查看课程表", view_courses, OUTLINE+PRIMARY),
        ("查看考试安排", view_exam_schedule, OUTLINE+INFO),
        ("查看今日空闲教室", view_empty_rooms, OUTLINE+WARNING),
        ("查看考试成绩", view_scores, OUTLINE+SUCCESS)
    ]
    
    for text, command, style in buttons:
        btn = safe_create(ttk.Button, main_frame, 
                         text=text, 
                         command=command, 
                         bootstyle=style,
                         width=20)
        if btn:
            btn.pack(pady=10)
    
    # 退出按钮
    exit_btn = safe_create(ttk.Button, main_frame, 
                          text="退出系统", 
                          command=on_closing, 
                          bootstyle=OUTLINE+DANGER,
                          width=20)
    if exit_btn:
        exit_btn.pack(pady=20)

    root.mainloop()