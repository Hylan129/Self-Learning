import tkinter as tk
from PIL import Image, ImageTk
if __name__ == '__main__':
    root = tk.Tk()
    root.title("局域网文件夹WEB共享")
    root.maxsize(360,450)
    root.minsize(360,450)
    command1=tk.StringVar()
    img_open = Image.open('test.png')
    img_png = ImageTk.PhotoImage(img_open)
    label_img = tk.Label(root, text="当前文件夹已共享！",compound ="top",font= ('FangSong', '16'),image = img_png)
    label_img.pack()
    url = tk.Entry(root,textvariable = command1,width=30,font = ('FangSong', '14'))
    url.place(x=26,y=375)
    command1.set("http://192.168.0.105:8129/")
    button=tk.Button(root,text="请复制链接地址到浏览器打开！",width=30,bg="yellow",bd=2,font= ('FangSong', '14'))
    button.place(x=25,y=405)
    root.mainloop()