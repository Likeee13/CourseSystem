import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from db_utils import fetch_all, execute_query
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from matplotlib import rcParams
import pandas as pd
import datetime
import tkinter as tk
from tkinter import messagebox, filedialog

# 设置中文字体，防止乱码
rcParams['font.family'] = 'Microsoft YaHei'  # 或 'SimHei'
def load_background_image():
    try:
        # 使用PIL打开并调整图片大小以适应窗口
        bg_image = Image.open("background2.jpg")  # 替换为您的背景图片路径
        bg_image = bg_image.resize((720, 560), Image.Resampling.LANCZOS)
        return ImageTk.PhotoImage(bg_image)
    except Exception as e:
        print(f"背景图片加载失败: {e}")
        return None

def AdminInterface(admin_id):
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
        win.geometry("800x500")
        
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
        
        # 查询并填充数据
        rows = fetch_all(query, params)
        for row in rows:
            tree.insert("", END, values=row)
        
        return win

    # 功能函数
    def add_course():
        if not root or not root.winfo_exists(): return
        
        win = safe_create(ttk.Toplevel, root)
        if not win: return
        win.title("添加课程")
        win.geometry("450x420")
        
        frame = safe_create(ttk.Frame, win, padding=20)
        if not frame: 
            win.destroy()
            return
        frame.pack(fill=BOTH, expand=True)
        
        # 表单布局
        form_frame = safe_create(ttk.Frame, frame)
        if not form_frame: return
        form_frame.pack(fill=X, pady=(0, 15))
        
        # 课程编号
        cid_label = safe_create(ttk.Label, form_frame, text="课程编号:")
        if cid_label: cid_label.grid(row=0, column=0, sticky=W, pady=5)
        entry_cid = safe_create(ttk.Entry, form_frame)
        if entry_cid: entry_cid.grid(row=0, column=1, sticky=EW, padx=5, pady=5)
        
        # 课程名称
        name_label = safe_create(ttk.Label, form_frame, text="课程名称:")
        if name_label: name_label.grid(row=1, column=0, sticky=W, pady=5)
        entry_name = safe_create(ttk.Entry, form_frame)
        if entry_name: entry_name.grid(row=1, column=1, sticky=EW, padx=5, pady=5)
        
        # 上课节次
        time_label = safe_create(ttk.Label, form_frame, text="上课节次 (1-10):")
        if time_label: time_label.grid(row=2, column=0, sticky=W, pady=5)
        entry_time = safe_create(ttk.Entry, form_frame)
        if entry_time: entry_time.grid(row=2, column=1, sticky=EW, padx=5, pady=5)
        
        # 教室
        room_label = safe_create(ttk.Label, form_frame, text="教室 (101, 102, 103):")
        if room_label: room_label.grid(row=3, column=0, sticky=W, pady=5)
        entry_room = safe_create(ttk.Entry, form_frame)
        if entry_room: entry_room.grid(row=3, column=1, sticky=EW, padx=5, pady=5)
        
        # 考试时间
        exam_label = safe_create(ttk.Label, form_frame, text="考试时间(格式: yyyy-mm-dd HH:MM):")
        if exam_label: exam_label.grid(row=4, column=0, sticky=W, pady=5)
        entry_exam = safe_create(ttk.Entry, form_frame)
        if entry_exam: entry_exam.grid(row=4, column=1, sticky=EW, padx=5, pady=5)
        
        # 按钮区域
        btn_frame = safe_create(ttk.Frame, frame)
        if not btn_frame: return
        btn_frame.pack(fill=X, pady=10)
        
        def submit():
            cid = entry_cid.get().strip() if entry_cid else ""
            name = entry_name.get().strip() if entry_name else ""
            time_str = entry_time.get().strip() if entry_time else ""
            room = entry_room.get().strip() if entry_room else ""
            exam = entry_exam.get().strip() if entry_exam else ""

            if not cid or not name or not time_str or not room or not exam:
                messagebox.showerror("错误", "所有字段都必须填写")
                return
            try:
                time = int(time_str)
                if time < 1 or time > 10:
                    messagebox.showerror("错误", "节次必须在1到10之间")
                    return
            except Exception:
                messagebox.showerror("错误", "节次必须是数字")
                return
            if room not in ('101', '102', '103'):
                messagebox.showerror("错误", "教室必须是101、102或103")
                return

            conflict = fetch_all("SELECT * FROM course WHERE time_slot=? AND room=?", (time, room))
            if conflict:
                messagebox.showerror("错误", "时间段和教室冲突")
                return

            try:
                execute_query("INSERT INTO course VALUES (?, ?, ?, ?, ?)", (cid, name, time, room, exam))
                messagebox.showinfo("成功", "课程添加成功")
                if win and win.winfo_exists():
                    win.destroy()
            except Exception as e:
                messagebox.showerror("错误", f"添加课程失败\n{e}")

        def cancel():
            if win and win.winfo_exists():
                win.destroy()

        submit_btn = safe_create(ttk.Button, btn_frame, 
                                 text="确认添加", 
                                 command=submit, 
                                 bootstyle=OUTLINE+SUCCESS,
                                 width=12)
        if submit_btn: submit_btn.pack(side=LEFT, padx=10)
        
        cancel_btn = safe_create(ttk.Button, btn_frame, 
                               text="返回", 
                               command=cancel, 
                               bootstyle=OUTLINE+DANGER,
                               width=12)
        if cancel_btn: cancel_btn.pack(side=RIGHT, padx=10)

    def enroll_student():
        if not root or not root.winfo_exists(): return
        
        win = safe_create(ttk.Toplevel, root)
        if not win: return
        win.title("为学生加课")
        win.geometry("450x250")
        
        frame = safe_create(ttk.Frame, win, padding=20)
        if not frame: 
            win.destroy()
            return
        frame.pack(fill=BOTH, expand=True)
        
        # 表单布局
        form_frame = safe_create(ttk.Frame, frame)
        if not form_frame: return
        form_frame.pack(fill=X, pady=(0, 15))
        
        # 学生学号
        sid_label = safe_create(ttk.Label, form_frame, text="学生学号:")
        if sid_label: sid_label.grid(row=0, column=0, sticky=W, pady=5)
        entry_sid = safe_create(ttk.Entry, form_frame)
        if entry_sid: entry_sid.grid(row=0, column=1, sticky=EW, padx=5, pady=5)
        
        # 课程编号
        cid_label = safe_create(ttk.Label, form_frame, text="课程编号:")
        if cid_label: cid_label.grid(row=1, column=0, sticky=W, pady=5)
        entry_cid = safe_create(ttk.Entry, form_frame)
        if entry_cid: entry_cid.grid(row=1, column=1, sticky=EW, padx=5, pady=5)
        
        # 按钮区域
        btn_frame = safe_create(ttk.Frame, frame)
        if not btn_frame: return
        btn_frame.pack(fill=X, pady=10)
        
        def submit():
            sid = entry_sid.get().strip() if entry_sid else ""
            cid = entry_cid.get().strip() if entry_cid else ""
            
            if not sid or not cid:
                messagebox.showerror("错误", "学生学号和课程编号不能为空")
                return

            course = fetch_all("SELECT time_slot FROM course WHERE cid=?", (cid,))
            if not course:
                messagebox.showerror("错误", "课程不存在")
                return
            course_time = course[0][0]

            conflict = fetch_all(
                "SELECT course.cid FROM enrollment JOIN course ON enrollment.cid=course.cid WHERE enrollment.sid=? AND course.time_slot=?",
                (sid, course_time))
            if conflict:
                messagebox.showerror("错误", "该学生在此时间段已有其他课程，选课冲突")
                return

            try:
                execute_query("INSERT INTO enrollment VALUES (?, ?)", (sid, cid))
                execute_query("INSERT INTO score (sid, cid, score) VALUES (?, ?, NULL)", (sid, cid))
                messagebox.showinfo("成功", f"学生 {sid} 选课 {cid} 成功")
                if win and win.winfo_exists():
                    win.destroy()
            except Exception as e:
                messagebox.showerror("错误", f"选课失败，可能是重复选课或学号课程号错误\n{e}")

        def cancel():
            if win and win.winfo_exists():
                win.destroy()

        submit_btn = safe_create(ttk.Button, btn_frame, 
                                 text="确认选课", 
                                 command=submit, 
                                 bootstyle=OUTLINE+SUCCESS,
                                 width=12)
        if submit_btn: submit_btn.pack(side=LEFT, padx=10)
        
        cancel_btn = safe_create(ttk.Button, btn_frame, 
                               text="返回", 
                               command=cancel, 
                               bootstyle=OUTLINE+DANGER,
                               width=12)
        if cancel_btn: cancel_btn.pack(side=RIGHT, padx=10)

    def modify_score():
        if not root or not root.winfo_exists(): return
        
        win = safe_create(ttk.Toplevel, root)
        if not win: return
        win.title("修改/添加成绩")
        win.geometry("450x300")
        
        frame = safe_create(ttk.Frame, win, padding=20)
        if not frame: 
            win.destroy()
            return
        frame.pack(fill=BOTH, expand=True)
        
        # 表单布局
        form_frame = safe_create(ttk.Frame, frame)
        if not form_frame: return
        form_frame.pack(fill=X, pady=(0, 15))
        
        # 学生学号
        sid_label = safe_create(ttk.Label, form_frame, text="学生学号:")
        if sid_label: sid_label.grid(row=0, column=0, sticky=W, pady=5)
        entry_sid = safe_create(ttk.Entry, form_frame)
        if entry_sid: entry_sid.grid(row=0, column=1, sticky=EW, padx=5, pady=5)
        
        # 课程编号
        cid_label = safe_create(ttk.Label, form_frame, text="课程编号:")
        if cid_label: cid_label.grid(row=1, column=0, sticky=W, pady=5)
        entry_cid = safe_create(ttk.Entry, form_frame)
        if entry_cid: entry_cid.grid(row=1, column=1, sticky=EW, padx=5, pady=5)
        
        # 成绩
        score_label = safe_create(ttk.Label, form_frame, text="成绩(0-100):")
        if score_label: score_label.grid(row=2, column=0, sticky=W, pady=5)
        entry_score = safe_create(ttk.Entry, form_frame)
        if entry_score: entry_score.grid(row=2, column=1, sticky=EW, padx=5, pady=5)
        
        # 按钮区域
        btn_frame = safe_create(ttk.Frame, frame)
        if not btn_frame: return
        btn_frame.pack(fill=X, pady=10)
        
        def submit():
            sid = entry_sid.get().strip() if entry_sid else ""
            cid = entry_cid.get().strip() if entry_cid else ""
            score_str = entry_score.get().strip() if entry_score else ""
            
            if not sid or not cid or not score_str:
                messagebox.showerror("错误", "所有字段不能为空")
                return
            try:
                score = int(score_str)
                if score < 0 or score > 100:
                    messagebox.showerror("错误", "成绩必须在0到100之间")
                    return
            except Exception:
                messagebox.showerror("错误", "成绩必须是整数")
                return

            enrollment = fetch_all("SELECT * FROM enrollment WHERE sid=? AND cid=?", (sid, cid))
            if not enrollment:
                messagebox.showerror("错误", "该学生未选这门课程")
                return

            existing = fetch_all("SELECT * FROM score WHERE sid=? AND cid=?", (sid, cid))
            try:
                if existing:
                    execute_query("UPDATE score SET score=? WHERE sid=? AND cid=?", (score, sid, cid))
                else:
                    execute_query("INSERT INTO score (sid, cid, score) VALUES (?, ?, ?)", (sid, cid, score))
                messagebox.showinfo("成功", "成绩修改成功")
                if win and win.winfo_exists():
                    win.destroy()
            except Exception as e:
                messagebox.showerror("错误", f"成绩修改失败\n{e}")

        def cancel():
            if win and win.winfo_exists():
                win.destroy()

        submit_btn = safe_create(ttk.Button, btn_frame, 
                                 text="确认修改", 
                                 command=submit, 
                                 bootstyle=OUTLINE+SUCCESS,
                                 width=12)
        if submit_btn: submit_btn.pack(side=LEFT, padx=10)
        
        cancel_btn = safe_create(ttk.Button, btn_frame, 
                               text="返回", 
                               command=cancel, 
                               bootstyle=OUTLINE+DANGER,
                               width=12)
        if cancel_btn: cancel_btn.pack(side=RIGHT, padx=10)

    def stat_course():
        if not root or not root.winfo_exists(): return
        
        win = safe_create(ttk.Toplevel, root)
        if not win: return
        win.title("课程成绩统计")
        win.geometry("550x700")
        
        frame = safe_create(ttk.Frame, win, padding=20)
        if not frame: 
            win.destroy()
            return
        frame.pack(fill=BOTH, expand=True)
        
        # 课程ID输入
        input_frame = safe_create(ttk.Frame, frame)
        if not input_frame: return
        input_frame.pack(fill=X, pady=(0, 15))
        
        cid_label = safe_create(ttk.Label, input_frame, text="课程编号:")
        if cid_label: cid_label.pack(side=LEFT, padx=5)
        
        entry_cid = safe_create(ttk.Entry, input_frame)
        if entry_cid: entry_cid.pack(side=LEFT, padx=5, fill=X, expand=True)
        
        # 查询按钮
        btn_frame = safe_create(ttk.Frame, input_frame)
        if not btn_frame: return
        btn_frame.pack(side=RIGHT)
        
        # 结果标签
        result_label = safe_create(ttk.Label, frame, text="")
        if result_label: result_label.pack(pady=10)
        
        # 图表容器
        chart_frame = safe_create(ttk.Frame, frame)
        if not chart_frame: return
        chart_frame.pack(fill=BOTH, expand=True, pady=10)
        
        # 按钮容器
        action_frame = safe_create(ttk.Frame, frame)
        if not action_frame: return
        action_frame.pack(fill=X, pady=10)
        
        def show_pie_chart(frame, cid, passed, failed):
            # 清除现有图表
            for widget in frame.winfo_children():
                widget.destroy()
                
            # 创建新图表
            fig = plt.figure(figsize=(5, 4), facecolor='white')
            ax = fig.add_subplot(111, facecolor='white')

            labels, sizes, colors = [], [], []
            if passed > 0:
                labels.append("及格")
                sizes.append(passed)
                colors.append('#4CAF50')  # 绿色
            if failed > 0:
                labels.append("不及格")
                sizes.append(failed)
                colors.append('#F44336')  # 红色

            if sizes:
                ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors)
                ax.axis('equal')
                ax.set_title(f"课程 {cid} 及格率")

                canvas = FigureCanvasTkAgg(fig, master=frame)
                canvas_widget = canvas.get_tk_widget()
                canvas.draw()
                canvas_widget.pack(fill=BOTH, expand=True)
            else:
                no_data = safe_create(ttk.Label, frame, text="没有数据可显示", font=("Helvetica", 12))
                if no_data: no_data.pack(pady=20)

        def submit():
            cid = entry_cid.get().strip() if entry_cid else ""
            if not cid:
                messagebox.showerror("错误", "请输入课程编号")
                return

            count = fetch_all("SELECT COUNT(*) FROM score WHERE cid=?", (cid,))
            if count[0][0] == 0:
                if result_label:
                    result_label.config(text="该课程暂无成绩记录")
                show_pie_chart(chart_frame, cid, 0, 0)
                return

            passed = fetch_all("SELECT COUNT(*) FROM score WHERE cid=? AND score >= 60", (cid,))[0][0]
            failed = fetch_all("SELECT COUNT(*) FROM score WHERE cid=? AND score < 60", (cid,))[0][0]
            total = passed + failed

            if total == 0:
                if result_label:
                    result_label.config(text="该课程暂无成绩记录")
                show_pie_chart(chart_frame, cid, 0, 0)
                return

            if result_label:
                result_label.config(text=f"总人数: {total} 及格: {passed} 不及格: {failed}")
            show_pie_chart(chart_frame, cid, passed, failed)

        def cancel():
            if win and win.winfo_exists():
                win.destroy()

        # 添加查询按钮
        query_btn = safe_create(ttk.Button, btn_frame, 
                               text="查询", 
                               command=submit, 
                               bootstyle=OUTLINE+PRIMARY)
        if query_btn: query_btn.pack(side=LEFT, padx=5)
        
        # 添加关闭按钮
        close_btn = safe_create(ttk.Button, action_frame, 
                              text="返回", 
                              command=cancel, 
                              bootstyle=OUTLINE+DANGER,
                              width=12)
        if close_btn: close_btn.pack(pady=10)

    def import_courses_from_file():
        file_path = filedialog.askopenfilename(filetypes=[("Excel Files", "*.xlsx;*.xls")])
        if not file_path:
            return

        success_count = 0
        error_count = 0
        errors = []

        try:
            # 使用 pandas 读取 Excel 文件
            df = pd.read_excel(file_path, engine='openpyxl')
            for index, row in df.iterrows():
                cid = str(row.get('课程编号', '')).strip()
                name = str(row.get('课程名称', '')).strip()
                time_str = str(row.get('上课节次', '')).strip()
                room = str(row.get('教室', '')).strip()
                exam_raw = row.get('考试时间', '')
                
                # 处理考试时间格式
                try:
                    if isinstance(exam_raw, datetime.datetime):
                        exam = exam_raw.strftime('%Y-%m-%d %H:%M')
                    else:
                        exam = str(exam_raw).strip()
                except Exception as e:
                    error_count += 1
                    errors.append(f"第 {index + 1} 行考试时间格式错误: {exam_raw}")
                    continue

                # 验证字段
                if not cid or not name or not time_str or not room or not exam:
                    error_count += 1
                    errors.append(f"第 {index + 1} 行数据缺失字段")
                    continue

                # 验证上课节次
                try:
                    time = int(time_str)
                    if time < 1 or time > 10:
                        error_count += 1
                        errors.append(f"第 {index + 1} 行节次必须在1到10之间")
                        continue
                except ValueError:
                    error_count += 1
                    errors.append(f"第 {index + 1} 行节次必须是数字")
                    continue

                # 验证教室
                if room not in ('101', '102', '103'):
                    error_count += 1
                    errors.append(f"第 {index + 1} 行教室必须是101、102或103")
                    continue

                # 检查时间冲突
                conflict = fetch_all("SELECT * FROM course WHERE time_slot=? AND room=?", (time, room))
                if conflict:
                    error_count += 1
                    errors.append(f"第 {index + 1} 行时间段和教室冲突")
                    continue

                # 插入数据
                try:
                    execute_query("INSERT INTO course VALUES (?, ?, ?, ?, ?)", (cid, name, time, room, exam))
                    success_count += 1
                except Exception as e:
                    error_count += 1
                    errors.append(f"第 {index + 1} 行添加课程失败: {e}")

        except Exception as e:
            messagebox.showerror("错误", f"文件读取失败: {e}")
            return

        # 显示导入结果
        if success_count > 0:
            messagebox.showinfo("成功", f"成功导入 {success_count} 条课程记录")
        if error_count > 0:
            error_msg = "\n".join(errors[:10])  # 最多显示10条错误
            if len(errors) > 10:
                error_msg += f"\n...还有 {len(errors) - 10} 条错误未显示"
            messagebox.showerror("错误", f"导入失败 {error_count} 条记录:\n{error_msg}")

    # 创建主窗口
    root = ttk.Window(themename="morph")
    root.title(f"管理员功能界面 - {admin_id}")
    root.geometry("720x560")
    
    # 安全关闭处理
    def on_closing():
        if root and root.winfo_exists():
            root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    
    # 主界面布局
    load_background_image();
    main_frame = safe_create(ttk.Frame, root, padding=30)
    if not main_frame:
        root.destroy()
        return
    main_frame.pack(fill=BOTH, expand=True)
    
    # 标题
    title_label = safe_create(ttk.Label, main_frame, 
                             text=f"管理员 {admin_id}",
                             font=("Helvetica", 16, "bold"),
                             bootstyle=PRIMARY)
    if title_label:
        title_label.pack(pady=(0, 20))
    
    # 功能按钮
    buttons = [
        ("添加课程", add_course, OUTLINE+PRIMARY),
        ("为学生加课", enroll_student, OUTLINE+INFO),
        ("修改/添加成绩", modify_score, OUTLINE+WARNING),
        ("统计课程及格率", stat_course, OUTLINE+SUCCESS),
        ("从文件导入课程", import_courses_from_file, OUTLINE+SECONDARY)
    ]
    
    for text, command, style in buttons:
        btn = safe_create(ttk.Button, main_frame, 
                         text=text, 
                         command=command, 
                         bootstyle=style,
                         width=25)
        if btn:
            btn.pack(pady=8)
    
    # 退出按钮
    exit_btn = safe_create(ttk.Button, main_frame, 
                          text="退出系统", 
                          command=on_closing, 
                          bootstyle=OUTLINE+DANGER,
                          width=25)
    if exit_btn:
        exit_btn.pack(pady=20)

    root.mainloop()