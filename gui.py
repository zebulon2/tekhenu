from tkinter import *
import tekh
import numpy as np

win = Tk()  # creating the main window and storing the window object in 'win'
win.title('Tekhenu Bot Ra action')  # setting title of the window


# win.geometry('500x200')  # setting the size of the window


def update_scores(bplist, bhvlist, bhhlist, tpl, bldv, bldh):
    for i in range(5):
        if bhvlist[i]['text'] == 'B':
            bldv[i] = 9
        elif bhvlist[i]['text'] == 'P':
            bldv[i] = 1
        elif bhvlist[i]['text'] == '0':
            bldv[i] = 0
        if bhhlist[i]['text'] == 'B':
            bldh[i] = 9
        elif bhhlist[i]['text'] == 'P':
            bldh[i] = 1
        elif bhhlist[i]['text'] == '0':
            bldh[i] = 0

    tekh.set_base_scores(tpl)
    for i in range(5):
        for j in range(5):
            bplist[5 * i + j].config(bg='#F0F0F0')
            if bplist[5 * i + j]['text'] == 'I':
                tpl[i, j] = 9
                bplist[5 * i + j].config(bg='light green')
    tekh.update_scores(tpl, bldv, bldh)
    #tekh.display_all(tpl, bldv, bldh)
    for i in range(5):
        for j in range(5):
            if tpl[i,j] == 9:
                bplist[5 * i + j].config(text='I')
            else:
                bplist[5 * i + j].config(text=str(tpl[i,j]))

    return


def func_house(button, bplist, bhvlist, bhhlist, tpl, bldv, bldh):  # function of the button
    dialog = Toplevel()
    choice = StringVar()
    r1 = Radiobutton(dialog, text="Bot", variable=choice, value='B')
    r2 = Radiobutton(dialog, text="Player", variable=choice, value='P')
    r3 = Radiobutton(dialog, text="None", variable=choice, value='0')
    choice.set(button['text'])
    r1.pack(anchor=W)
    r2.pack(anchor=W)
    r3.pack(anchor=W)
    dialog.wait_visibility()
    dialog.grab_set()
    dialog.wait_window()
    button.config(text=choice.get())
    if choice.get() == 'B':
        button.config(bg = 'pink')
    elif choice.get() == 'P':
        button.config(bg='light blue')
    else:
        button.config(bg='#F0F0F0')
    update_scores(bplist, bhvlist, bhhlist, tpl, bldv, bldh)
    return


def func_pillar(button, btnpil_list, btnhv_list, btnhh_list, tpl, bldv, bldh):
    dialog = Toplevel()
    choice = StringVar()
    r1 = Radiobutton(dialog, text="Bot", variable=choice, value='I')
    r2 = Radiobutton(dialog, text="Player", variable=choice, value='I')
    r3 = Radiobutton(dialog, text="None", variable=choice, value='0')
    choice.set('0')
    r1.pack(anchor=W)
    r2.pack(anchor=W)
    r3.pack(anchor=W)
    dialog.wait_visibility()
    dialog.grab_set()
    dialog.wait_window()
    button.config(text=choice.get())
    if choice.get() == 'B':
        button.config(bg = 'pink')
    elif choice.get() == 'P':
        button.config(bg='light blue')
    else:
        button.config(bg='#F0F0F0')
    update_scores(btnpil_list, btnhv_list, btnhh_list, tpl, bldv, bldh)
    return


def choose(bplist, bhvlist, bhhlist, tpl, bldv, bldh, lbl):
    for i in range(5):
        if bhvlist[i]['text'] == 'B':
            bldv[i] = 9
        elif bhvlist[i]['text'] == 'P':
            bldv[i] = 1
        elif bhvlist[i]['text'] == '0':
            bldv[i] = 0
        if bhhlist[i]['text'] == 'B':
            bldh[i] = 9
        elif bhhlist[i]['text'] == 'P':
            bldh[i] = 1
        elif bhhlist[i]['text'] == '0':
            bldh[i] = 0
    tekh.set_base_scores(tpl)
    for i in range(5):
        for j in range(5):
            bplist[5 * i + j].config(bg='#F0F0F0')
            if bplist[5 * i + j]['text'] == 'I':
                tpl[i, j] = 9
                bplist[5 * i + j].config(bg='light green')
    tekh.update_scores(tpl, bldv, bldh)
    #tekh.display_all(tpl, bldv, bldh)
    (msg, choice) = tekh.choose_place(tpl, bldv, bldh)
    lbl.delete(1.0, END)
    lbl.insert(END, msg)
    bplist[5 * choice[0] + choice[1]].config(bg='red')
    return


# build temple
# tekh
tpl = np.zeros((5, 5), dtype=np.int8)
bldv = np.zeros(5, dtype=np.int8)
bldh = np.zeros(5, dtype=np.int8)
tekh.set_base_scores(tpl)

btnhv_list = []
btnhh_list = []
btnpil_list = []

top_frame = Frame(win)
temple_frame = Frame(top_frame, highlightbackground="blue", highlightthickness=2)
top_frame.grid(row=0)
temple_frame.grid(column=1, rowspan=5, columnspan=5)
# create vertical house buttons
for i in range(5):
    btn = Button(top_frame, text=str(bldv[i]), width=5, height=2)
    btn["command"] = lambda btn=btn: func_house(btn, btnpil_list, btnhv_list, btnhh_list, tpl, bldv, bldh)
    btnhv_list.append(btn)
    btn.grid(row=i, column=0)

# create horizontal house buttons
for i in range(5):
    btn = Button(top_frame, text=str(bldh[i]), width=5, height=2)
    btn["command"] = lambda btn=btn: func_house(btn, btnpil_list, btnhv_list, btnhh_list, tpl, bldv, bldh)
    btnhh_list.append(btn)
    btn.grid(row=5, column=i+1)

# create pillar tile buttons
for i in range(5):
    for j in range(1, 6):
        btn = Button(temple_frame, text=str(tpl[i,j-1]), width=5, height=2)
        btn["command"] = lambda btn=btn: func_pillar(btn, btnpil_list, btnhv_list, btnhh_list, tpl, bldv, bldh)
        btnpil_list.append(btn)
        btn.grid(row=i, column=j)

bottom_frame = Frame(win)
bottom_frame.grid(row=2)

lbl = Text(bottom_frame, width=60)
lbl.configure(font=("Helvetica", 8))
btn_choose = Button(bottom_frame, text='Find bot pillar place', height=2)
btn_choose["command"] = lambda btn_choose=btn_choose: choose(btnpil_list, btnhv_list, btnhh_list, tpl, bldv, bldh, lbl)
btn_choose.grid(row=6, columnspan=6)
lbl.grid(columnspan=6)

win.mainloop()  # running the loop that works as a trigger
