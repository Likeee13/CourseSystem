from PIL import Image, ImageTk
import tkinter as tk


def set_background(root, image_path, width, height):

    # 打开并缩放背景图像
    image = Image.open("background2.jpg")
    resized_image = image.resize((width, height))
    background_image = ImageTk.PhotoImage(resized_image)

    # 创建背景标签并放置
    background_label = tk.Label(root, image=background_image)
    background_label.image = background_image  # 避免图像被垃圾回收
    background_label.place(x=0, y=0, relwidth=1, relheight=1)

    return background_label
