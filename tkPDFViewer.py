try:
    from tkinter import*
    import fitz
    from tkinter.ttk import Progressbar
    from threading import Thread
    import math
except Exception as e:
    print(f"This error occurred while importing necessary modules or library {e}")


class ShowPdf():
    img_object_li = []

    # Added zoomDPI parameter for flexibility
    def __init__(self):
        self.frame = None
        self.display_msg = None
        self.text = None

    def pdf_view(self, master, width=1200, height=600, pdf_location="", bar=True, load="after", zoom_dpi=72):

        self.frame = Frame(master, width=width, height=height, bg="white")

        scroll_y = Scrollbar(self.frame, orient="vertical")
        scroll_x = Scrollbar(self.frame, orient="horizontal")

        scroll_x.pack(fill="x", side="bottom")
        scroll_y.pack(fill="y", side="right")

        percentage_view = 0
        percentage_load = StringVar()

        if bar is True and load == "after":
            self.display_msg = Label(textvariable=percentage_load)
            self.display_msg.pack(pady=10)

            loading = Progressbar(self.frame, orient=HORIZONTAL, length=100, mode='determinate')
            loading.pack(side=TOP, fill=X)

        self.text = Text(self.frame, yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set, width=width, height=height)
        self.text.pack(side="left")

        scroll_x.config(command=self.text.xview)
        scroll_y.config(command=self.text.yview)

        def add_img():
            percentage_divide = 0
            open_pdf = fitz.open(pdf_location)

            for page in open_pdf:
                # Use zoomDPI parameter
                # getPixmap removed from class 'Page' after v1.19 - use 'get_pixmap'
                # pix = page.getPixmap(dpi=zoomDPI)
                pix = page.get_pixmap(dpi=zoom_dpi)
                pix1 = fitz.Pixmap(pix, 0) if pix.alpha else pix
                # 'getImageData' removed from class 'Pixmap' after v1.19 - use 'tobytes'
                # img = pix1.getImageData("ppm")
                img = pix1.tobytes("ppm")
                timg = PhotoImage(data=img)
                self.img_object_li.append(timg)
                if bar is True and load == "after":
                    percentage_divide = percentage_divide + 1
                    percentage_view = (float(percentage_divide)/float(len(open_pdf))*float(100))
                    loading['value'] = percentage_view
                    percentage_load.set(f"Please wait!, your pdf is loading {int(math.floor(percentage_view))}%")
            if bar is True and load == "after":
                loading.pack_forget()
                self.display_msg.pack_forget()

            for i in self.img_object_li:
                self.text.image_create(END, image=i)
                self.text.insert(END, "\n\n")
            self.text.configure(state="disabled")

        def start_pack():
            t1 = Thread(target=add_img)
            t1.start()

        if load == "after":
            master.after(250, start_pack)
        else:
            start_pack()

        return self.frame


def main():
    root = Tk()
    root.geometry("700x980")
    d = ShowPdf().pdf_view(root, pdf_location=r"D:\DELL\Documents\Encyclopedia GUI.pdf", width=50, height=200)
    d.pack()
    root.mainloop()


if __name__ == '__main__':
    main()
