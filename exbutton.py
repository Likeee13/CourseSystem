
from tkinter import *


class ExButton(Canvas):
    def __init__(self, master, command, height=0, width=0, text="", font="宋体", style="horizontal_color"):
        super().__init__(master, height=height, width=width, highlightthickness=0, cursor="hand2")
        self.height = height
        self.width = width
        self.text = text
        self.font = font
        self.command = command
        self.style = style
        self.click_effect = False
        self.button_list = None
        self.color_1 = None
        self.color_2 = None
        self.active_color_1 = None
        self.active_color_2 = None
        self.font_color = None
        self.active_font_color = None
        self.bind("<Button-1>", self.callback)
        self.set()

    def set(self, button_list=None, font_color=("#000000", "#000000"), color=("#FFFFFF", "#FFFFFF"),
            active_color=("#FFD1FC", "#F0F0F0")):
        self.font_color = font_color[0]
        self.active_font_color = font_color[1]
        self.button_list = button_list
        self.color_1 = color[0]
        self.color_2 = color[1]
        self.active_color_1 = active_color[0]
        self.active_color_2 = active_color[1]
        if self.button_list is not None:
            self.button_list.append(self)
            self.button_list[0].click_effect = True
        self.paint()

    def callback(self, event):
        if event:
            pass
        self.command()
        if self.button_list is not None:
            self.set_active()
            self.paint()

    def set_active(self):
        for i in range(0, len(self.button_list)):
            self.button_list[i].click_effect = False
        self.click_effect = True

    def paint(self):
        if self.button_list is not None:
            for i in range(0, len(self.button_list)):
                if self.button_list[i].style == "horizontal_color":
                    if self.button_list[i].click_effect is True:
                        self.button_list[i].create_rectangle(0, 0, 7, self.button_list[i].height,
                                                             fill=self.button_list[i].active_color_1, outline="")
                        self.button_list[i].create_rectangle(7, 0, self.button_list[i].width,
                                                             self.button_list[i].height,
                                                             fill=self.button_list[i].active_color_2, outline="")
                        self.button_list[i].create_text(self.button_list[i].width / 2, self.button_list[i].height / 2,
                                                        text=self.button_list[i].text, font=self.button_list[i].font,
                                                        fill=self.button_list[i].active_font_color)
                    else:
                        self.button_list[i].create_rectangle(0, 0, 7, self.button_list[i].height,
                                                             fill=self.button_list[i].color_1, outline="")
                        self.button_list[i].create_rectangle(7, 0, self.button_list[i].width,
                                                             self.button_list[i].height,
                                                             fill=self.button_list[i].color_2, outline="")
                        self.button_list[i].create_text(self.button_list[i].width / 2, self.button_list[i].height / 2,
                                                        text=self.button_list[i].text, font=self.button_list[i].font,
                                                        fill=self.button_list[i].font_color)
                elif self.button_list[i].style == "vertical_color":
                    if self.button_list[i].click_effect is True:
                        self.button_list[i].create_rectangle(0, 0, self.button_list[i].width, 5,
                                                             fill=self.button_list[i].active_color_1, outline="")
                        self.button_list[i].create_rectangle(0, 5, self.button_list[i].width,
                                                             self.button_list[i].height,
                                                             fill=self.button_list[i].active_color_2, outline="")
                        self.button_list[i].create_text(self.button_list[i].width / 2, self.button_list[i].height / 2,
                                                        text=self.button_list[i].text, font=self.button_list[i].font,
                                                        fill=self.button_list[i].active_font_color)
                    else:
                        self.button_list[i].create_rectangle(0, 0, self.button_list[i].width, 5,
                                                             fill=self.button_list[i].color_1, outline="")
                        self.button_list[i].create_rectangle(0, 5, self.button_list[i].width,
                                                             self.button_list[i].height,
                                                             fill=self.button_list[i].color_2, outline="")
                        self.button_list[i].create_text(self.button_list[i].width / 2, self.button_list[i].height / 2,
                                                        text=self.button_list[i].text, font=self.button_list[i].font,
                                                        fill=self.button_list[i].font_color)
        else:
            self.create_rectangle(0, 0, 8, self.height, fill=self.color_1, outline="")
            self.create_rectangle(8, 0, self.width, self.height, fill=self.color_2, outline="")
            self.create_text(self.width / 2, self.height / 2, text=self.text, font=self.font, fill=self.font_color)

