from tkinter import *
from tkinter import filedialog, scrolledtext
import pandas as pd
import numpy as np
import tabulate
import credentials
import CV_processing

window = Tk()
window_height, window_width = window.winfo_screenheight(), window.winfo_screenwidth()

def resumeSelectionPage():
    file_paths = []
    global n, data_table
    n = 0

    def getFiles():
        paths = filedialog.askopenfilenames(parent=window, title='Select CVs')
        global n
        n = len(paths)
        names = ''
        for i in range(n):
            file_paths.append(paths[i])
            t = paths[i].split('/')
            names = names + t[-1] + '\n'
        l1.config(text='Process Files')
        l2.config(state=NORMAL)
        l2.insert(INSERT, names)
        l2.config(state=DISABLED)
        process_button.place(x=window_width//2, y=700)


    def processFiles():
        select_button.config(state=DISABLED)
        process_button.config(state=DISABLED)
        l3 = Label(frame,text='Extracted data: ', bg='#ffffff')
        l3.place(x=310, y=125)
        job_description = jd_text.get("1.0", "end-1c")
        data = []
        for i in range(n):
            data.append(CV_processing.readResume(file_paths[i], job_description))

        data_frame = pd.DataFrame(data)
        data_frame.sort_values(by='Match Score', ascending=False, inplace=True)
        data_frame['S.No.'] = range(1, n+1)
        data_frame.set_index('S.No.', inplace=True)
        global data_table
        data_table = tabulate.tabulate(data_frame, headers='keys', showindex='always', tablefmt='grid')
        l4 = Text(frame, bg='#ffffff', fg='#000000', width=150, height=32, wrap='none')
        l4.insert(INSERT, data_table)
        l4.config(state=DISABLED)
        l4.place(x=310, y=150)
        (Label(frame,
              text='Note: The records are sorted in descending order of matching score with job description.')
         .place(x=310, y=670))
        maximize_button.place(x=window_width-120, y=700)

    def maxView():
        max_window = Tk()
        max_window.attributes('-fullscreen', True)
        h = Scrollbar(max_window, orient='horizontal')
        h.pack(side=BOTTOM, fill='x')
        v = Scrollbar(max_window, orient='vertical')
        v.pack(side=RIGHT, fill='y')
        text = Text(max_window, height=window_height-25, width=window_width-25,
                    xscrollcommand=h.set, yscrollcommand=v.set,
                    wrap='none', pady=15, padx=15)
        h.config(command=text.xview)
        v.config(command=text.yview)
        text.insert(INSERT, data_table)
        text.config(state=DISABLED)
        text.pack()
        Button(max_window, text='CLOSE',
               command=max_window.destroy,
               bg='#ff0000', fg='#ffffff').place(x=window_width - 62, y=1)

    frame = Frame(window, bg='#ffffff', height=window_height, width=window_width)
    frame.place(x=0, y=0)

    l1 = Label(frame, text='Select Resume Files', font=('Comic Sans MS', 25),
               height=1, bg='#ffffff')
    l1.place(x=650, y=50)

    select_button = Button(frame, text='Select CV Files', command=getFiles)
    select_button.place(x=120, y=700)

    Label(frame, bg='#ffffff', text='Selected files: ').place(x=30, y=125)
    l2 = Text(frame, bg='#ffffff', fg='#0000ee', width=30, height=32)
    l2.config(state=DISABLED)
    l2.place(x=30, y=150)

    process_button = Button(frame, text='Process', command=processFiles)
    maximize_button = Button(frame, text='Enlarge', command=maxView)


def loadJD():
    with open(r'Data/Job Description.txt') as f:
        jd = f.read()
    return jd


def editJD():
    def doneEdit():
        done.place_forget()
        jd_text.config(state=DISABLED, bg='#aaaaaa')
        value = jd_text.get("1.0", "end-1c")
        # print(value)
        with open(r'Data/Job Description.txt', 'w') as f:
            f.write(value)
        edit_button.config(state=NORMAL)
        next_button.config(state=NORMAL)

    edit_button.config(state=DISABLED)
    next_button.config(state=DISABLED)
    jd_text.config(state='normal', bg='#fefefe')
    done = Button(window, text='Save', command=doneEdit)
    done.place(x=380, y=600)


def main():
    window.title(credentials.title)
    window.state('zoomed')
    # window.resizable(False, False)
    window_height, window_width = window.winfo_screenheight(), window.winfo_screenwidth()

    frame = Frame(window, bg='#ffffff', height=window_height, width=window_width)
    frame.place(x=0, y=0)

    heading_label = Label(window, text="RESUME RANKER", bg='#444444', fg="#00ff00",
                          font=('Comic Sans MS', 40), width=window_width, height=1)
    heading_label.pack(pady=20)

    global jd_text
    jd_text = Text(window, pady=10, width=150, height=25, bg='#aaaaaa')
    jd_text.insert(INSERT, loadJD())
    jd_text.pack()
    jd_text.config(state='disabled')

    global edit_button, next_button
    edit_button = Button(window, text='Edit Job Description', command=editJD)
    next_button = Button(window, text='Next', command=resumeSelectionPage)
    next_button.place(x=window_width - 300, y=600)
    edit_button.place(x=200, y=600)

    Label(window, text=credentials.signature,
          bg='#ffffff', fg='#00aaff',
          font=('Comic Sans MS', 14)).place(x=window_width//2-50, y=window_height-240)

    window.mainloop()


if __name__ == "__main__":
    main()
