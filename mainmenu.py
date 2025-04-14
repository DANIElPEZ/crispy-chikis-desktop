import colors as cl
from customtkinter import CTk, CTkLabel, CTkButton, CTkImage, set_appearance_mode
from PIL import Image
#views
from payments import payments
from products import products
from reviews import reviews
from orders import orders

class MainMenu:
     def __init__(self, instance):
          self.instance=instance
          set_appearance_mode('light')
          self.app=CTk()
          window_width = 460
          window_height = 330
          screen_width = self.app.winfo_screenwidth()
          screen_height = self.app.winfo_screenheight()
          x = int((screen_width / 2) - (window_width / 2))
          y = int((screen_height / 2) - (window_height / 2))
          self.app.geometry(f"{window_width}x{window_height}+{x}+{y}")

          self.app.title('Menu principal')
          self.app.resizable(0,0)
          self.app.configure(fg_color=cl.colorsPalette['dark blue'])
          self.app.iconbitmap('assets/logo.ico')
          CTkLabel(self.app, text='Opciones', text_color=cl.colorsPalette['white'], font=('Nunito',22)).place(y=20, x=180)
          #labels
          CTkLabel(self.app, text='Pedidos', text_color=cl.colorsPalette['white'], font=('Nunito',19)).place(x=35, y=65)
          CTkLabel(self.app, text='Productos', text_color=cl.colorsPalette['white'], font=('Nunito',19)).place(x=310, y=65)
          CTkLabel(self.app, text='Pagos', text_color=cl.colorsPalette['white'], font=('Nunito',19)).place(x=35, y=180)
          CTkLabel(self.app, text='Reseñas', text_color=cl.colorsPalette['white'], font=('Nunito',19)).place(x=310, y=180)
          #buttons
          images=[
               Image.open('assets/orders.png'),
               Image.open('assets/products.png'),
               Image.open('assets/payments.png'),
               Image.open('assets/reviews.png')
                  ]
          imagesCtk=[
               CTkImage(light_image=images[0], dark_image=images[0], size=(70, 70)),
               CTkImage(light_image=images[1], dark_image=images[1], size=(70, 70)),
               CTkImage(light_image=images[2], dark_image=images[2], size=(70, 70)),
               CTkImage(light_image=images[3], dark_image=images[3], size=(70, 70))
               ]
          CTkButton(self.app, text='', image=imagesCtk[0], height=70, width=125, fg_color=cl.colorsPalette['light brown'], hover_color=cl.colorsPalette['light blue'], command=self.orders).place(x=35, y=100)
          CTkButton(self.app, text='', image=imagesCtk[1], height=70, width=125, fg_color=cl.colorsPalette['light brown'], hover_color=cl.colorsPalette['light blue'], command=self.products).place(x=310, y=100)
          CTkButton(self.app, text='', image=imagesCtk[2], height=70, width=125, fg_color=cl.colorsPalette['light brown'], hover_color=cl.colorsPalette['light blue'], command=self.payments).place(x=35, y=215)
          CTkButton(self.app, text='', image=imagesCtk[3], height=70, width=125, fg_color=cl.colorsPalette['light brown'], hover_color=cl.colorsPalette['light blue'], command=self.reviews).place(x=310, y=215)

          self.app.mainloop()

     def orders(self): orders(self.instance, self.app)

     def reviews(self): reviews(self.instance)

     def products(self): products(self.instance, self.app)

     def payments(self): payments(self.instance)