import sqlite3
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from PIL import Image, ImageTk
from student_interface import StudentInterface
from admin_interface import AdminInterface
import tkinter as tk
from db_utils import fetch_all
from db_utils import execute_query
import requests

def show_login_window():
    # 安全创建函数
    def safe_create(creator, *args, **kwargs):
        try:
            return creator(*args, **kwargs)
        except tk.TclError as e:
            if "application has been destroyed" in str(e):
                return None
            raise

    # 加载背景图片函数
    def load_background_image():
        try:
            # 使用PIL打开并调整图片大小以适应窗口
            bg_image = Image.open("background2.jpg")  # 替换为您的背景图片路径
            bg_image = bg_image.resize((720, 560), Image.Resampling.LANCZOS)
            return ImageTk.PhotoImage(bg_image)
        except Exception as e:
            print(f"背景图片加载失败: {e}")
            return None

    def login():
        sid = entry_id.get()
        pwd = entry_pwd.get()

        try:
            result = fetch_all("SELECT * FROM user WHERE sid=? AND password=?", (sid, pwd))
            if result:
                root.destroy()
                user = result[0]
                if user[2]:  # is_admin
                    AdminInterface(user[0])
                else:
                    StudentInterface(user[0])
            else:
                ttk.dialogs.Messagebox.show_error("登录失败", "用户名或密码错误", parent=root)
        except Exception as e:
            ttk.dialogs.Messagebox.show_error("连接失败", f"服务端错误: {e}", parent=root)



    def register():
        sid = entry_id.get()
        pwd = entry_pwd.get()

        # 新增输入验证
        if not sid or not pwd:
            ttk.dialogs.Messagebox.show_error("输入错误", "账号和密码不能为空", parent=root)
            return

        try:
            # 新增唯一性检查
            if fetch_all("SELECT sid FROM user WHERE sid=?", (sid,)):
                ttk.dialogs.Messagebox.show_error("注册失败", "该账号已被注册", parent=root)
                return

            # 明确指定插入字段
            execute_query("INSERT INTO user (sid, password) VALUES (?, ?)", (sid, pwd))
            ttk.dialogs.Messagebox.show_info("注册成功", "注册成功，请登录", parent=root)
            
        except requests.exceptions.RequestException as e:  # 捕获网络异常
            ttk.dialogs.Messagebox.show_error("连接失败", f"无法连接服务器: {e}", parent=root)
        except KeyError as e:  # 处理服务端响应格式错误
            ttk.dialogs.Messagebox.show_error("服务异常", "服务器返回数据格式错误", parent=root)
        except Exception as e:
            # 解析服务端返回的错误信息
            error_msg = str(e)
            if "UNIQUE constraint failed" in error_msg:
                error_msg = "该账号已被注册"
            ttk.dialogs.Messagebox.show_error("操作失败", f"错误原因: {error_msg}", parent=root)

    # 创建现代化登录窗口
    root = ttk.Window(themename="morph")
    root.title("课程信息管理系统 - 登录")
    root.geometry("720x560")
    
    # 加载背景图片
    bg_image = load_background_image()
    
    # 安全关闭处理
    def on_closing():
        if root and root.winfo_exists():
            root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    
    # ==== 界面美化优化 ====
    # 1. 添加背景图片
    if bg_image:
        bg_label = safe_create(ttk.Label, root, image=bg_image)
        if bg_label:
            bg_label.image = bg_image  # 保持引用
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)
    
    # 2. 创建半透明卡片式登录框
    card_frame = safe_create(ttk.Frame, root, padding=25)
    if card_frame:
        # 设置半透明效果
        card_frame.configure(style='TFrame')
        card_frame.place(relx=0.5, rely=0.5, anchor=CENTER)
        
    
        # 使用ttkbootstrap样式创建卡片效果
        style = ttk.Style()
        style.configure('Card.TFrame', background="#ffffff", 
                        borderwidth=2, relief="solid", 
                        bordercolor="#e0e0e0", 
                        borderradius=15)
        card_frame.configure(style='Card.TFrame')
    
    # 3. 标题美化
    title_label = safe_create(ttk.Label, card_frame, 
                             text="课程管理系统", 
                             font=("微软雅黑", 18, "bold"),
                             bootstyle=(PRIMARY, INVERSE))
    if title_label:
        title_label.pack(pady=(0, 20))
    
    # 4. 输入框美化
    input_frame = safe_create(ttk.Frame, card_frame)
    if input_frame:
        input_frame.pack(fill=X, pady=5)
    
    # 用户名输入
    id_label = safe_create(ttk.Label, input_frame, text="账号:", 
                          font=("微软雅黑", 10))
    if id_label:
        id_label.grid(row=0, column=0, sticky=W, pady=5)
    
    entry_id = safe_create(ttk.Entry, input_frame, width=25, 
                          font=("微软雅黑", 10))
    if entry_id:
        entry_id.grid(row=0, column=1, pady=5, padx=10)
        # 添加占位符
        entry_id.insert(0, "请输入学号/工号")
        entry_id.bind("<FocusIn>", lambda e: entry_id.delete(0, END) if entry_id.get() == "请输入学号/工号" else None)
    
    # 密码输入
    pwd_label = safe_create(ttk.Label, input_frame, text="密码:", 
                            font=("微软雅黑", 10))
    if pwd_label:
        pwd_label.grid(row=1, column=0, sticky=W, pady=5)
    
    entry_pwd = safe_create(ttk.Entry, input_frame, show='*', 
                            width=25, font=("微软雅黑", 10))
    if entry_pwd:
        entry_pwd.grid(row=1, column=1, pady=5, padx=10)
        # 添加占位符
        entry_pwd.insert(0, "请输入密码")
        entry_pwd.bind("<FocusIn>", lambda e: entry_pwd.delete(0, END) if entry_pwd.get() == "请输入密码" else None)
    
    # 5. 按钮美化
    btn_frame = safe_create(ttk.Frame, card_frame)
    if btn_frame:
        btn_frame.pack(pady=15)
    
    login_btn = safe_create(ttk.Button, btn_frame, 
                           text="登 录", 
                           command=login, 
                           bootstyle=SUCCESS, 
                           width=10,
                           padding=5)
    if login_btn:
        login_btn.pack(side=LEFT, padx=10)
        # 添加悬停效果
        login_btn.bind("<Enter>", lambda e: login_btn.configure(bootstyle=(SUCCESS, OUTLINE)))
        login_btn.bind("<Leave>", lambda e: login_btn.configure(bootstyle=SUCCESS))
    
    register_btn = safe_create(ttk.Button, btn_frame, 
                              text="注 册", 
                              command=register, 
                              bootstyle=INFO, 
                              width=10,
                              padding=5)
    if register_btn:
        register_btn.pack(side=LEFT, padx=10)
        # 添加悬停效果
        register_btn.bind("<Enter>", lambda e: register_btn.configure(bootstyle=(INFO, OUTLINE)))
        register_btn.bind("<Leave>", lambda e: register_btn.configure(bootstyle=INFO))
    
    # 6. 添加底部版权信息
    footer = safe_create(ttk.Label, root, 
                        text="© 2025 课程管理系统 | 版本 2.0",
                        font=("微软雅黑", 8),
                        bootstyle=SECONDARY)
    if footer:
        footer.pack(side=BOTTOM, pady=10)

    root.mainloop()