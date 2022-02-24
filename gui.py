from tkinter import *
import tekh

win = Tk()  # creating the main window and storing the window object in 'win'
win.title('Tekhenu Bot Ra action')  # setting title of the window


# win.geometry('500x200')  # setting the size of the window


def update_scores(bplist, bhvlist, bhhlist, tpl):
    for i in range(5):
        if bhvlist[i]['text'] == 'B':
            tpl.set_house_v(i, tekh.Owner.bot)
        elif bhvlist[i]['text'] == 'P':
            tpl.set_house_v(i, tekh.Owner.player)
        elif bhvlist[i]['text'] == '0':
            tpl.set_house_v(i, tekh.Owner.none)
        if bhhlist[i]['text'] == 'B':
            tpl.set_house_h(i, tekh.Owner.bot)
        elif bhhlist[i]['text'] == 'P':
            tpl.set_house_h(i, tekh.Owner.player)
        elif bhhlist[i]['text'] == '0':
            tpl.set_house_h(i, tekh.Owner.none)

    for i in range(5):
        for j in range(5):
            if bplist[5 * i + j]['text'] == 'B':
                tpl.set_tile(i, j, tekh.Owner.bot)
                bplist[5 * i + j].config(bg='pink')
                bplist[5 * i + j].config(text='I')  # replace pillar name with I regardless of ownership
            elif bplist[5 * i + j]['text'] == 'P':
                tpl.set_tile(i, j, tekh.Owner.player)
                bplist[5 * i + j].config(bg='light blue')
                bplist[5 * i + j].config(text='I')  # replace pillar name with I regardless of ownership
            elif bplist[5 * i + j]['text'] == '0':
                tpl.set_tile(i, j, tekh.Owner.none)
                bplist[5 * i + j].config(bg='#F0F0F0')

    for i in range(5):
        for j in range(5):
            if tpl.get_tile(i, j).owner == tekh.Owner.none:  # put new scores in non built tiles
                bplist[5 * i + j].config(text=str(tpl.get_score(i, j)))
                bplist[5 * i + j].config(bg='#F0F0F0')  # reset colour to grey (removes previous red)

    return


def func_house(button, bplist, bhvlist, bhhlist, tpl):  # function of the button
    dialog = Toplevel()
    dialog.title("Place a House")
    dialog.geometry('250x100')
    choice = StringVar()
    r1 = Radiobutton(dialog, text="Bot", variable=choice, value='B')
    r2 = Radiobutton(dialog, text="Player", variable=choice, value='P')
    r3 = Radiobutton(dialog, text="None", variable=choice, value='0')
    choice.set(button['text'])
    r1.pack(anchor=W)
    r2.pack(anchor=W)
    r3.pack(anchor=W)
    okButton = Button(dialog, text='OK', command=dialog.destroy)
    okButton.pack()
    dialog.wait_visibility()
    dialog.grab_set()
    dialog.wait_window()
    button.config(text=choice.get())
    if choice.get() == 'B':
        button.config(bg='pink')
    elif choice.get() == 'P':
        button.config(bg='light blue')
    else:
        button.config(bg='#F0F0F0')
    update_scores(bplist, bhvlist, bhhlist, tpl)

    return


def func_pillar(button, btnpil_list, btnhv_list, btnhh_list, tpl):
    dialog = Toplevel()
    dialog.title("Place a Pillar")
    dialog.geometry('250x100')
    choice = StringVar()
    r1 = Radiobutton(dialog, text="Bot", variable=choice, value='B')
    r2 = Radiobutton(dialog, text="Player", variable=choice, value='P')
    r3 = Radiobutton(dialog, text="None", variable=choice, value='0')
    choice.set('0')
    r1.pack(anchor=W)
    r2.pack(anchor=W)
    r3.pack(anchor=W)
    okButton = Button(dialog, text='OK', command=dialog.destroy)
    okButton.pack()
    dialog.wait_visibility()
    dialog.grab_set()
    dialog.wait_window()
    button.config(text=choice.get())
    if choice.get() == 'B':
        button.config(bg='pink')
    elif choice.get() == 'P':
        button.config(bg='light blue')
    else:
        button.config(bg='#F0F0F0')
    update_scores(btnpil_list, btnhv_list, btnhh_list, tpl)
    return


def choose(bplist, bhvlist, bhhlist, tpl, msgbox):
    for i in range(5):
        if bhvlist[i]['text'] == 'B':
            tpl.set_house_v(i, tekh.Owner.bot)
        elif bhvlist[i]['text'] == 'P':
            tpl.set_house_v(i, tekh.Owner.player)
        elif bhvlist[i]['text'] == '0':
            tpl.set_house_v(i, tekh.Owner.none)
        if bhhlist[i]['text'] == 'B':
            tpl.set_house_h(i, tekh.Owner.bot)
        elif bhhlist[i]['text'] == 'P':
            tpl.set_house_h(i, tekh.Owner.player)
        elif bhhlist[i]['text'] == '0':
            tpl.set_house_h(i, tekh.Owner.none)
    for i in range(5):
        for j in range(5):
            if bplist[5 * i + j]['text'] != 'I':
                bplist[5 * i + j].config(bg='#F0F0F0')
    (msg, choice) = tpl.choose_place()
    msgbox.delete(1.0, END)
    msgbox.insert(END, msg)
    bplist[5 * choice[0] + choice[1]].config(bg='red')
    return


# build temple
temple = tekh.Temple()

btn_house_v_list = []
btn_house_h_list = []
btn_pillar_list = []

top_frame = Frame(win)
temple_frame = Frame(top_frame, highlightbackground="blue", highlightthickness=2)
top_frame.grid(row=0)
temple_frame.grid(column=1, rowspan=5, columnspan=5)
# create vertical house buttons
for i in range(5):
    btn = Button(top_frame, text=str(temple.get_house_v(i)), width=5, height=2)
    btn["command"] = lambda btn=btn: func_house(btn, btn_pillar_list, btn_house_v_list, btn_house_h_list, temple)
    btn_house_v_list.append(btn)
    btn.grid(row=i, column=0)

# create horizontal house buttons
for i in range(5):
    btn = Button(top_frame, text=str(temple.get_house_h(i)), width=5, height=2)
    btn["command"] = lambda btn=btn: func_house(btn, btn_pillar_list, btn_house_v_list, btn_house_h_list, temple)
    btn_house_h_list.append(btn)
    btn.grid(row=5, column=i+1)

# create pillar tile buttons
for i in range(5):
    for j in range(1, 6):
        btn = Button(temple_frame, text=str(temple.get_tile(i, j - 1)), width=5, height=2)
        btn["command"] = lambda btn=btn: func_pillar(btn, btn_pillar_list, btn_house_v_list, btn_house_h_list, temple)
        btn_pillar_list.append(btn)
        btn.grid(row=i, column=j)

update_scores(btn_pillar_list, btn_house_v_list, btn_house_h_list, temple)
bottom_frame = Frame(win)
bottom_frame.grid(row=2)

msgbox = Text(bottom_frame, height=18, width=60)
msgbox.configure(font=("Helvetica", 8))
btn_choose = Button(bottom_frame, text='Find bot pillar place', height=2)
btn_choose["command"] = lambda btn_choose=btn_choose: choose(btn_pillar_list, btn_house_v_list, btn_house_h_list,
                                                             temple, msgbox)
btn_choose.grid(row=6, columnspan=6)
msgbox.grid(columnspan=6)

win.mainloop()  # running the loop that works as a trigger
