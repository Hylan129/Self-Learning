import tkinter as tk
from tkinter import messagebox

class verification_window(tk.Frame):

    # 调用时初始化
    def __init__(self):
        global root
        root = tk.Tk()
        # 窗口大小设置为150x150
        root.geometry('150x150+885+465')

        root.resizable(0, 0)  # 窗口大小固定

        super().__init__()
        self.username = tk.StringVar()
        self.password = tk.StringVar()
        self.pack()
        self.main_window()

        root.mainloop()

    # 窗口布局
    def main_window(self):
        global root
        username_label=tk.Label(root,text='Username:',font=('Arial',12)).place(x=35,y=10)
        username_input = tk.StringVar
        username_entry=tk.Entry(root,textvariable=self.username).place(x=2,y=35)

        password_label=tk.Label(root,text='Password:',font=('Arial',12)).place(x=35,y=58)
        password_input = tk.StringVar
        password_entry=tk.Entry(root,textvariable=self.password,show='*').place(x=2,y=83)

        # 在按下CONFIRM按钮时调用验证函数
        conformation_button = tk.Button(root,text='CONFIRM',command=self.verification,fg='white',bg='black', activeforeground='white', activebackground='navy',width=8,height=1)
        conformation_button.place(x=6,y=112)

        quit_button = tk.Button(root, text='QUIT', command=root.quit, fg='white', bg='black', activeforeground='white', activebackground='red', width=8, height=1)
        quit_button.place(x=78,y=112)

    # 验证函数
    def verification(self):
        global root

        # 检查用户名和密码 是否在user_dict字典中
        user_dict = {987654321:112233,123456789:332211}
        if user_dict.get(int(self.username.get())) == int(self.password.get()):
            # 成功提醒
            messagebox.showinfo(title='Correct', message=f'{int(self.username.get())}, welcome!')  

            # 验证成功后打开main_gui窗口
            #root.withdraw()
            #from gui import main_gui
            #main_gui.app()

        else:
            messagebox.showerror(title='Wrong inputs!', message='Please enter correct username or password.')  # 错误提醒

if __name__ == '__main__':
    verification_window()