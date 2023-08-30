import os
from pypdf import PdfReader, PdfWriter, PdfMerger
import tkinter as tk
from tkinter import BOTH, LEFT, RIGHT, ttk, filedialog, Frame
import tkPDFViewer


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        # Set filetypes
        self.pdf_writer = None
        self.temp_file = None
        self.pages_to_rotate = None
        self.numof_pages = None
        self.status = 0
        self.output_file = None
        self.input_files = None
        self.pdf_merger = None
        self.variable2 = None
        self.variable1 = None
        self.pdf_name = None
        self.filename = None
        self.pdf_reader = None
        self.filetypes = (('pdf files', '*.pdf'), ('PDF Files', '.PDF'))
        self.slider_value = tk.DoubleVar()
        self.pdf_info = tk.StringVar()
        self.pdf_info.set('Pages')
        self.zoom_info = tk.StringVar()
        self.zoom_info.set('72 dpi')
        self.zoom_dpi = 72
        self.pdf_width = 150
        self.rotate_page = tk.StringVar()
        # Configure root window
        self.title("PDF-Tool")
        self.geometry('750x850')
        self.resizable(width=True, height=True)
        self.__create_widgets()

    def __create_widgets(self):
        # Create left and right frame
        self.frm_left = Frame(self)
        self.frm_left.pack(side=LEFT, fill=BOTH, expand=False)
        self.frm_right = Frame(self)
        self.frm_right.pack(side=RIGHT, expand=True)
        # Create Sizegrip
        self.sg = ttk.Sizegrip(self.frm_right)
        self.sg.pack(side='right', anchor='se')
        # Label
        self.lbl_title = ttk.Label(self.frm_left, text='PDF-Tool')
        self.lbl_title.pack(side='top')
        # Button
        self.btn_loadpdf = ttk.Button(self.frm_left, text='Load PDF File')
        self.btn_loadpdf['command'] = self.load_pdf
        self.btn_loadpdf.pack(fill=BOTH)
        # Display PDF Metadata
        self.lbl_numpages = ttk.Label(self.frm_left, text='Pages')
        self.lbl_numpages.pack(fill=BOTH)
        # Zoom Scale
        self.lbl_zoom_info = ttk.Label(self.frm_left, text='72 dpi')
        self.lbl_zoom_info.pack(fill=BOTH)
        # Zoom Button
        self.btn_zoom_in = ttk.Button(self.frm_left, text='Zoom +')
        self.btn_zoom_in['command'] = self.zoom_in
        self.btn_zoom_in.pack(fill=BOTH)
        self.btn_zoom_out = ttk.Button(self.frm_left, text='Zoom -')
        self.btn_zoom_out['command'] = self.zoom_out
        self.btn_zoom_out.pack(fill=BOTH)
        # Split PDF
        self.btn_split = ttk.Button(self.frm_left, text='Split to single files')
        self.btn_split['command'] = self.split_pdf
        self.btn_split.pack(fill=BOTH)
        self.btn_merge = ttk.Button(self.frm_left, text='Merge PDF Files')
        self.btn_merge['command'] = self.merge_pdf
        self.btn_merge.pack(fill=BOTH)
        # Rotate Page
        self.lbl_rotate_entry = ttk.Label(self.frm_left, text='Rotate Page Nr. (start with 0)')
        self.lbl_rotate_entry.pack(fill=BOTH)
        self.ent_rotate = ttk.Entry(self.frm_left, textvariable=self.rotate_page)
        self.ent_rotate.pack(fill=BOTH)
        self.btn_rotate = ttk.Button(self.frm_left, text='Rotate Page')
        self.btn_rotate['command'] = self.rotate_pdf_page
        self.btn_rotate.pack(fill=BOTH)
        # Save button
        self.btn_save = ttk.Button(self.frm_left, text='Save PDF')
        self.btn_save['command'] = self.save_pdf
        self.btn_save.pack(fill=BOTH)
        # Quit button
        self.btn_quit = ttk.Button(self.frm_left, text='Quit')
        self.btn_quit['command'] = self.end_prog
        self.btn_quit.pack(fill=BOTH)

    def flip_names(self):
        if self.status == 0:
            self.temp_file = 'temp_rotated.pdf'
            self.pdf_reader = PdfReader(open(self.pdf_name, 'rb'))
            self.status = 1
        elif self.status == 1:
            self.temp_file = 'temp_rotated1.pdf'
            self.pdf_name = 'temp_rotated.pdf'
            self.pdf_reader = PdfReader(open(self.pdf_name, 'rb'))
            self.status = 2
        elif self.status == 2:
            self.temp_file = 'temp_rotated.pdf'
            self.pdf_name = 'temp_rotated1.pdf'
            self.pdf_reader = PdfReader(open(self.pdf_name, 'rb'))
            self.status = 1
        else:
            print("oops this should not have been called!")

    def load_pdf(self):
        """Load pdf file, extract number of pages and display pdf"""
        self.pdf_reader = None
        self.pdf_name = self.open_filename()
        # Read PDF as binary file
        self.pdf_reader = PdfReader(open(self.pdf_name, 'rb'))
        self.lbl_numpages['text'] = str(len(self.pdf_reader.pages)) + " Page(s)"
        self.show_pdf()

    def merge_pdf(self):
        """Merge selected pdf files"""
        self.pdf_merger = PdfMerger()
        self.input_files = filedialog.askopenfilenames(initialdir=os.getcwd(), title="Open File",
                                                       filetypes=self.filetypes)
        self.output_file = filedialog.asksaveasfilename(initialdir=os.getcwd(), title="Save as",
                                                        filetypes=self.filetypes)
        print(self.input_files)
        print(self.output_file)
        for i in self.input_files:
            self.pdf_merger.append(i)
        with open(self.output_file, "wb") as f_out:
            self.pdf_merger.write(f_out)
        print('Merge complete!')

    def open_filename(self):
        """Get the filename from tkinter filedialog and return filename"""
        self.filename = filedialog.askopenfilename(initialdir=os.getcwd(), title="Open File",
                                                   filetypes=self.filetypes)
        print(self.filename)
        return self.filename

    def rotate_pdf_page(self):
        """check if there are page(s) to rotate and create list of pages to rotate"""
        if self.rotate_page.get():
            self.pages_to_rotate = [int(s) for s in self.rotate_page.get().split(',')]
        else:
            return
        print(f"main {self.status}")
        self.flip_names()
        # create new document
        self.pdf_writer = PdfWriter()
        # get number of pages in document
        self.numof_pages = len(self.pdf_reader.pages)
        if self.pdf_reader:
            print("pdf loaded")
            # iterate over range of pages and rotate by 90 degrees only those in self.pages
            for page in range(self.numof_pages):
                if page in self.pages_to_rotate:
                    self.pdf_writer.add_page(self.pdf_reader.pages[page])
                    self.pdf_writer.pages[page].rotate(90)
                else:
                    self.pdf_writer.add_page(self.pdf_reader.pages[page])
                    self.pdf_writer.pages[page].rotate(90)
            with open(self.temp_file, 'wb') as f_out:
                self.pdf_writer.write(f_out)
            # Reset everything
            self.rotate_page.set('')
            self.page_rotate = None
            self.pdf_name = self.temp_file
            self.show_pdf()
        else:
            print("load pdf first")

    def save_pdf(self):
        """Ask for filename and save pdf file"""
        self.output_file = filedialog.asksaveasfilename(initialdir=os.getcwd(), title='Save as',
                                                        filetypes=self.filetypes)
        with open(self.output_file, "wb") as f_out:
            self.pdf_writer.write(f_out)

    def show_pdf(self):
        """Display pdf file on screen"""
        # Destroy old instance in case a previous pdf is loaded
        if self.variable2:
            self.variable2.destroy()
        if self.variable1:
            self.variable1.img_object_li.clear()
        # Create object to ShowPdf from tkPDFViewer
        self.variable1 = tkPDFViewer.ShowPdf()
        # Set pdf location, width, height and standard zoom.
        self.variable2 = self.variable1.pdf_view(self.frm_right, pdf_location=self.pdf_name, width=144, height=100,
                                                 zoom_dpi=self.zoom_dpi)
        self.variable2.pack()

    def split_pdf(self):
        """Split entire pdf file in separate pages and save as Page_XX.pdf, where XX is
        replaced with the page number."""
        if self.pdf_reader:
            for page in range(len(self.pdf_reader.pages)):
                self.pdf_writer = PdfWriter()
                self.pdf_writer.add_page(self.pdf_reader.pages[page])
                with open(f"Page_{page}.pdf", "wb") as f_out:
                    self.pdf_writer.write(f_out)
        else:
            print("no document to split")

    def zoom_in(self):
        """Zoom into document in 15 dpi steps."""
        # Destroy existing old instance first
        if self.variable2:
            self.variable2.destroy()
        self.variable1 = tkPDFViewer.ShowPdf()
        self.zoom_dpi = self.zoom_dpi + 15
        self.pdf_width = self.pdf_width + 5
        self.lbl_zoom_info['text'] = str(self.zoom_dpi) + " dpi"
        # Clear image list
        self.variable1.img_object_li.clear()
        self.variable2 = self.variable1.pdf_view(self.frm_right, pdf_location=self.pdf_name, width=self.pdf_width,
                                                 height=100, zoom_dpi=self.zoom_dpi)
        self.variable2.pack()

    def zoom_out(self):
        """Zoom out document in 15 dpi steps."""
        # Destroy existing old instance first
        if self.variable2:
            self.variable2.destroy()
        self.variable1 = tkPDFViewer.ShowPdf()
        self.zoom_dpi = self.zoom_dpi - 15
        self.pdf_width = self.pdf_width - 5
        self.lbl_zoom_info['text'] = str(self.zoom_dpi) + " dpi"
        # Clear image list
        self.variable1.img_object_li.clear()
        self.variable2 = self.variable1.pdf_view(self.frm_right, pdf_location=self.pdf_name, width=self.pdf_width,
                                                 height=100, zoom_dpi=self.zoom_dpi)
        self.variable2.pack()

    def end_prog(self):
        """Clear up temporary files."""
        if os.path.exists('temp_rotated.pdf'):
            os.remove('temp_rotated.pdf')
        if os.path.exists('temp_rotated1.pdf'):
            os.remove('temp_rotated1.pdf')
        tk.Tk.destroy(self)


if __name__ == "__main__":
    app = App()
    app.mainloop()
