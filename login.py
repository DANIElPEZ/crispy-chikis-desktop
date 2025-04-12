from customtkinter import CTk, CTkLabel, CTkEntry, CTkButton, set_appearance_mode
from tkinter import messagebox
import colors as cl
import re
from provider import provider
#import views
from mainmenu import MainMenu

class login:
     def __init__(self):
          set_appearance_mode('light')
          self.intance=provider()
          self.app=CTk()
          
          window_width = 280
          window_height = 340
          screen_width = self.app.winfo_screenwidth()
          screen_height = self.app.winfo_screenheight()
          x = int((screen_width / 2) - (window_width / 2))
          y = int((screen_height / 2) - (window_height / 2))
          self.app.geometry(f"{window_width}x{window_height}+{x}+{y}")

          self.app.title('Iniciar sesión')
          self.app.resizable(0,0)
          self.app.configure(fg_color=cl.colorsPalette['orange'])
          self.app.iconbitmap('assets/logo.ico')
          #inputs
          CTkLabel(self.app, text='Correo electronico', text_color=cl.colorsPalette['white'], font=('Nunito',19)).place(y=70, x=50)
          self.entry_email=CTkEntry(self.app, width=190, height=33, font=('Nunito',17), text_color=cl.colorsPalette['black'], fg_color=cl.colorsPalette['pink'])
          self.entry_email.place(x=50, y=98)
          
          CTkLabel(self.app, text='Clave de acceso', text_color=cl.colorsPalette['white'], font=('Nunito',19)).place(y=150, x=50)
          self.entry_password=CTkEntry(self.app, width=190, height=33, font=('Nunito',17), text_color=cl.colorsPalette['black'], fg_color=cl.colorsPalette['pink'], show='🍗')
          self.entry_password.place(x=50, y=180)
          
          CTkButton(self.app, text='Acceder', text_color=cl.colorsPalette['white'], font=('Nunito', 19), fg_color=cl.colorsPalette['dark brown'], width=190, hover_color=cl.colorsPalette['light brown'], command=self.login).place(x=50, y=230)
          self.app.mainloop()

     def login(self):
          email=self.entry_email.get()
          password=self.entry_password.get()

          #test credentials:
          email="fordowhilem@gmail.com"
          password="The794613$"

          if self.sanatizeEmail(email) and self.sanatizePassword(password):
               self.intance.login_in(email, password)
               if self.intance.session_user:
                    self.app.destroy()
                    MainMenu(self.intance)
          else:
               messagebox.showerror('Error', 'Credenciales invalidas o formato incorrecto')

     def sanatizeEmail(self, text):
          text=text.strip()
          if any(char in text for char in ['<', '>', '"', "'", ';', '`']):
               return False

          regex = r'^[\w\.-]+@(gmail\.com|hotmail\.com)$'
          return bool(re.fullmatch(regex, text))
          
     def sanatizePassword(self, text):
          text=text.strip()
          if any(char in text for char in ['<', '>', '"', "'", ';', '`', '=', '\\']):
               return False
          
          regex = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@#$%^&+=!¡?*_])[A-Za-z\d@#$%^&+=!¡?*_]{8,32}$"
          return bool(re.fullmatch(regex, text))

if __name__ == '__main__':
     login()

#test credentials:
#email: fordowhilem@gmail.com
#password: The794613$