import tkinter

from tkinter import ttk
from funcs.calc import *





root = tkinter.Tk()
root.title("Net Calculator")
root.geometry("600x200")

result_frame=ttk.Frame(borderwidth=1, relief="solid", padding=[8, 10])
result_frame.grid(row=3, columnspan=3)
W=tkinter.IntVar()
H=tkinter.IntVar()
skf = "SKF"
simple = "Простая"
hooks = "С Крючками"
selected = tkinter.StringVar(value='skf')
add, store = net_storage()

inputW = ttk.Entry(textvariable=W)
inputH = ttk.Entry(textvariable=H)
btn_result = ttk.Button(text="Рассчитать", command=add([W.get(), H.get()]))
btn_skf = ttk.Radiobutton(text=skf, variable=selected, value='skf')
btn_simple = ttk.Radiobutton(text=simple, variable=selected, value='simple')
btn_hooks = ttk.Radiobutton(text=hooks, variable=selected, value='hooks')
label = ttk.Label(text="Расчет м/с по световому проему", font=("Arial", 16, "bold"), padding=[15,10])


label.grid(row=0, column=1, columnspan=2, sticky="n")
inputW.grid(row=2, column=1, padx=10, pady=10)
inputH.grid(row=2, column=2, padx=10, pady=10)
btn_result.grid(row=2, column=3, pady=10, padx=10)
btn_skf.grid(row=1, column=1, sticky="n")
btn_simple.grid(row=1, column=2, sticky="n")
btn_hooks.grid(row=1, column=3, sticky="n")

for net in store():
    print(f"net: {net}")
    lbl = ttk.Label(result_frame)
    # lbl['text']=net
    lbl.pack()
    lbl.config(text=net)
    lbl.update()
    

# root.update()
root.mainloop()



# root.mainloop()
    
