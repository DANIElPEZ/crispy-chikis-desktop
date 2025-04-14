from customtkinter import CTkToplevel, CTkLabel, CTkButton, CTkEntry, CTkTextbox, CTkImage, CTkOptionMenu, set_appearance_mode
from tkinter import messagebox, ttk, filedialog
import colors as cl
from PIL import Image
import re
import os
import requests
from io import BytesIO

class products:
     def __init__(self, instance, window):
          set_appearance_mode('light')
          self.instance = instance
          self.categories = []
          self.product = None

          self.app = CTkToplevel(window)
          self.app.grab_set()

          window_width = 925
          window_height = 400
          screen_width = self.app.winfo_screenwidth()
          screen_height = self.app.winfo_screenheight()
          x = int((screen_width / 2) - (window_width / 2))
          y = int((screen_height / 2) - (window_height / 2))
          self.app.geometry(f"{window_width}x{window_height}+{x}+{y}")

          self.app.title('Productos')
          self.app.resizable(0, 0)
          self.app.configure(fg_color=cl.colorsPalette['orange'])
          self.app.iconbitmap('assets/logo.ico')
          
          CTkLabel(self.app, text='Nombre', text_color=cl.colorsPalette['white'], font=('Nunito', 19)).place(x=20, y=20)
          CTkLabel(self.app, text='Descripción', text_color=cl.colorsPalette['white'], font=('Nunito', 19)).place(x=20, y=90)
          CTkLabel(self.app, text='Precio', text_color=cl.colorsPalette['white'], font=('Nunito', 19)).place(x=20, y=220)
          CTkLabel(self.app, text='Categoria', text_color=cl.colorsPalette['white'], font=('Nunito', 19)).place(x=20, y=290)
          CTkLabel(self.app, text='Imagen (PNG)', text_color=cl.colorsPalette['white'], font=('Nunito', 19)).place(x=280, y=20)

          self.entry_name = CTkEntry(self.app, width=210, height=33, font=('Nunito', 17),
                                        text_color=cl.colorsPalette['black'], fg_color=cl.colorsPalette['pink'])
          self.entry_name.place(x=20, y=50)

          self.entry_desciription = CTkTextbox(self.app, width=220, height=90, font=('Nunito', 17),
                                                  text_color=cl.colorsPalette['black'], fg_color=cl.colorsPalette['pink'])
          self.entry_desciription.place(x=20, y=120)

          self.entry_price = CTkEntry(self.app, width=210, height=33, font=('Nunito', 17),
                                        text_color=cl.colorsPalette['black'], fg_color=cl.colorsPalette['pink'])
          self.entry_price.place(x=20, y=247)

          self.entry_category = CTkOptionMenu(self.app, font=('Nunito', 17),
                                             text_color=cl.colorsPalette['black'], fg_color=cl.colorsPalette['pink'])
          self.entry_category.place(x=20, y=320)

          self.add_category_image = CTkImage(light_image=Image.open('assets/add.png'),
                                             dark_image=Image.open('assets/add.png'), size=(20, 20))
          CTkButton(self.app, text='', image=self.add_category_image, fg_color=cl.colorsPalette['light blue'],
                    hover_color=cl.colorsPalette['light green'], width=20, command=self.add_category).place(x=185, y=320)

          self.add_image = CTkImage(light_image=Image.open('assets/add.png'),
                                   dark_image=Image.open('assets/add.png'), size=(30, 30))
          CTkButton(self.app, text='', image=self.add_image, fg_color=cl.colorsPalette['light blue'],
                    hover_color=cl.colorsPalette['light green'], width=30, command=self.select_image).place(x=410, y=17)

          self.image_preview_label = CTkLabel(self.app, text="")
          self.image_preview_label.place(x=280, y=60)
          self.selected_image_path = None

          CTkButton(self.app, text='Guardar', font=('Nunito', 17), text_color=cl.colorsPalette['white'],
                    fg_color=cl.colorsPalette['dark brown'], hover_color=cl.colorsPalette['light brown'],
                    width=200, command=self.save_product).place(x=250, y=315)
          CTkButton(self.app, text='Eliminar', font=('Nunito', 17), text_color=cl.colorsPalette['white'],
                    fg_color=cl.colorsPalette['dark brown'], hover_color=cl.colorsPalette['light brown'],
                    width=200, command=self.delete_product).place(x=250, y=350)
          
          columns=('Nombre', 'Precio')
          self.tree = ttk.Treeview(self.app, columns=columns, show='headings', height=16)
          for col in columns:
               self.tree.heading(col, text=col.capitalize())
          self.tree.place(x=500, y=20)
          self.tree.bind('<<TreeviewSelect>>', self.load_product)
          self.load_products_and_categories()

     def select_image(self):
          file_path = filedialog.askopenfilename(filetypes=[("PNG files", "*.png")])
          if file_path:
               self.selected_image_path = file_path

               img = Image.open(file_path)
               img.thumbnail((120, 120))
               img_ctk = CTkImage(light_image=img, dark_image=img, size=(120, 120))
               self.image_preview_label.configure(image=img_ctk, text="")
               self.image_preview_label.image = img_ctk

     def save_product(self):
          name = self.sanitizeText(self.entry_name.get().strip())
          desc = self.entry_desciription.get("1.0", "end").strip()
          price = self.entry_price.get().strip()
          category = self.entry_category.get()

          name=self.sanitizeText(name)
          desc=self.sanitizeText(desc)

          if not (name and desc and price and category and self.selected_image_path):
               messagebox.showerror("Error", "Todos los campos son obligatorios.")
               return
          
          if not (self.sanitizePrice(price) or len(name)==0 or len(desc)==0):
               messagebox.showerror("Error", "Formato de texto no válido.")
               return

          try:
               price = float(price)
               if price < 0:
                    messagebox.showerror("Error", "El precio no puede ser negativo.")
                    return
               if price > 500000:
                    messagebox.showerror("Error", "El precio no puede ser mayor a 500.000.")
                    return
               if price == 0:
                    messagebox.showerror("Error", "El precio no puede ser cero.")
                    return
               
               category_id = next((c['tipo_producto_id'] for c in self.categories if c['nombre'] == category), None)
               if category_id is None:
                    raise Exception("Categoría no encontrada.")

               file_name = os.path.basename(self.selected_image_path)

               if self.selected_image_path.startswith("http"):
                    response=requests.get(self.selected_image_path)
                    response.raise_for_status()
                    data=response.content
               else:
                    with open(self.selected_image_path, 'rb') as f:
                         data=f.read()

               self.instance.supabase.storage.from_("products").upload(
                    file=data,
                    path=file_name,
                    file_options={"content-type": "image/png", "upsert": "true"}
               )

               url_img = self.instance.supabase.storage.from_("products").get_public_url(file_name)

               product_data = {
                    "nombre": name,
                    "descripcion": desc,
                    "precio": float(price),
                    "tipo_producto": category_id,
                    "imagen": url_img
               }

               if self.product is not None and "producto_id" in self.product:
                    self.instance.supabase.table("productos").update(product_data).eq("producto_id", self.product["producto_id"]).execute()
                    messagebox.showinfo("Éxito", "Producto actualizado correctamente.")
               else:
                    self.instance.supabase.table("productos").insert(product_data).execute()
                    messagebox.showinfo("Éxito", "Producto guardado correctamente.")

          except Exception as e:
               print(e)
               print(e.__dict__)
               messagebox.showerror("Error", "Error al guardar el producto.")

     def delete_product(self):
          selected_item=self.tree.selection()
          if not selected_item:return

          confirmar = messagebox.askyesno("Confirmar", "¿Estás seguro de eliminar este producto?")
          if not confirmar: return

          try:
               product_id = int(selected_item[0])
               product = next((p for p in self.instance.products if p['producto_id'] == product_id), None)
               
               if product:
                    self.instance.supabase.table("productos").delete().eq("producto_id", product["producto_id"]).execute()
                    if product.get("imagen"):
                         url_parts = product['imagen'].split('/')
                         file_name = url_parts[-1]
                         self.instance.supabase.storage.from_("products").remove([file_name])
                         
                    self.load_products_and_categories()
                    self.entry_name.delete(0, 'end')
                    self.entry_desciription.delete("1.0", "end")
                    self.entry_price.delete(0, 'end')
                    self.image_preview_label.configure(image=None, text="")
                    self.selected_image_path = None
                    self.product = None
                    messagebox.showinfo("Éxito", "Producto eliminado correctamente.")
          except Exception as e:
               print(e)
               messagebox.showerror("Error", "Error al eliminar el producto.")

     def load_product(self, event):
          selected_item=self.tree.selection()
          if not selected_item:return

          self.entry_name.delete(0, 'end')
          self.entry_desciription.delete("1.0", "end")
          self.entry_price.delete(0, 'end')
          self.image_preview_label.configure(image=None, text="")
          self.selected_image_path = None

          try:
               product_id = int(selected_item[0])
               product = next((p for p in self.instance.products if p['producto_id'] == product_id), None)
               
               if product:
                    self.product = product
                    
                    self.entry_name.insert(0, product['nombre'])
                    self.entry_desciription.insert('1.0', product['descripcion'])
                    self.entry_price.insert(0, str(product['precio']))
                    
                    category_name = next(
                         (c['nombre'] for c in self.categories 
                         if c['tipo_producto_id'] == product['tipo_producto']),
                         None
                    )
                    if category_name:
                         self.entry_category.set(category_name)

                    if 'imagen' in product and product['imagen']:
                         self.selected_image_path = product['imagen']
                         
                         response = requests.get(product['imagen'])
                         response.raise_for_status()
                         
                         img_data = BytesIO(response.content)
                         img = Image.open(img_data)
                         img.thumbnail((120, 120))
                         
                         img_ctk = CTkImage(light_image=img, dark_image=img, size=img.size)
                         self.image_preview_label.configure(image=img_ctk, text="")
                         self.image_preview_label.image = img_ctk
                         
          except Exception as e:
               print(f"Error al cargar producto: {str(e)}")
               messagebox.showerror("Error", "No se pudo cargar el producto seleccionado")

     def add_category(self):
          add_category = CTkToplevel(self.app)
          add_category.grab_set()
          window_width_category = 300
          window_height_category = 200
          screen_width_category = self.app.winfo_screenwidth()
          screen_height_category = self.app.winfo_screenheight()
          x_category = int((screen_width_category / 2) - (window_width_category / 2))
          y_category = int((screen_height_category / 2) - (window_height_category / 2))
          add_category.geometry(f"{window_width_category}x{window_height_category}+{x_category}+{y_category}")
          add_category.title('Agregar categoria')
          add_category.resizable(0, 0)
          add_category.configure(fg_color=cl.colorsPalette['orange'])
          add_category.iconbitmap('assets/logo.ico')
          CTkLabel(add_category, text='Nombre', text_color=cl.colorsPalette['white'], font=('Nunito', 19)).place(x=20, y=20)
          entry_name = CTkEntry(add_category, width=210, height=33, font=('Nunito', 17),
                                   text_color=cl.colorsPalette['black'], fg_color=cl.colorsPalette['pink'])
          entry_name.place(x=20, y=50)
          CTkButton(add_category, text='Agregar', text_color=cl.colorsPalette['white'], font=('Nunito', 19),
                    fg_color=cl.colorsPalette['dark brown'], width=190, hover_color=cl.colorsPalette['light brown'],
                    command=lambda: self.add_category_db(entry_name.get(), add_category)).place(x=20, y=100)
          CTkButton(add_category, text='Cancelar', text_color=cl.colorsPalette['white'], font=('Nunito', 19),
                    fg_color=cl.colorsPalette['dark brown'], width=190, hover_color=cl.colorsPalette['light brown'],
                    command=add_category.destroy).place(x=20, y=150)

     def add_category_db(self, name, window):
          name = self.sanitizeText(name)
          if name == '':
               return
          try:
               if name.strip() != "":
                    self.instance.supabase.table('tipo_producto').insert({"nombre": name}).execute()
                    messagebox.showinfo('Exito', 'Categoria agregada')
                    window.destroy()
                    self.load_products_and_categories()
               else:
                    messagebox.showerror('Error', 'Nombre invalido')
          except Exception as e:
               print(e)
               messagebox.showerror('Error', 'Error al agregar categoria.')

     def load_products_and_categories(self):
          try:
               self.instance.fetch_products()
               self.categories = self.instance.supabase.table('tipo_producto').select('*').execute().data
               self.entry_category.configure(values=[category['nombre'] for category in self.categories])
               if self.categories:
                    self.entry_category.set(self.categories[0]['nombre'])

               self.tree.delete(*self.tree.get_children())
               for product in self.instance.products:
                    self.tree.insert('', 'end', iid=product['producto_id'], values=(product['nombre'], product['precio']))
          except Exception as e:
               print(e)
               messagebox.showerror('Error', 'Error al cargar.')

     def sanitizeText(self, text):
          text = text.strip()
          if re.match(r'^[A-Za-zÀ-ÿ\s,\.]+$', text):
               return text
          else:
               messagebox.showerror('Error', 'Formato de texto no válido.')
               return ''

     def sanitizePrice(self, text):
          return bool(re.fullmatch(r'\d+(\.\d+)?', text.strip()))
