from customtkinter import CTk, CTkLabel, CTkButton, CTkEntry, CTkTextbox, CTkOptionMenu, set_appearance_mode
from tkinter import ttk
import colors as cl
from tkinter import messagebox
import re

class reviews:
     def __init__(self, instance, is_admin):
          self.is_admin=is_admin
          self.instance=instance
          self.reviews=[]

          set_appearance_mode('light')
          self.app=CTk()
          window_width = 1140
          window_height = 380
          screen_width = self.app.winfo_screenwidth()
          screen_height = self.app.winfo_screenheight()
          x = int((screen_width / 2) - (window_width / 2))
          y = int((screen_height / 2) - (window_height / 2))
          self.app.geometry(f"{window_width}x{window_height}+{x}+{y}")

          self.app.title('Reseñas')
          self.app.resizable(0,0)
          self.app.configure(fg_color=cl.colorsPalette['dark brown'])
          self.app.iconbitmap('assets/logo.ico')

          CTkLabel(self.app, text='Nombre', text_color=cl.colorsPalette['white'], font=('Nunito',19)).place(y=20, x=20)
          CTkLabel(self.app, text='Descripción', text_color=cl.colorsPalette['white'], font=('Nunito',19)).place(x=20, y=100)
          CTkLabel(self.app, text='Puntuación', text_color=cl.colorsPalette['white'], font=('Nunito',19)).place(x=20, y=220)
          CTkLabel(self.app, text='Producto', text_color=cl.colorsPalette['white'], font=('Nunito',19)).place(x=270, y=20)
          CTkLabel(self.app, text='Reseñas', text_color=cl.colorsPalette['white'], font=('Nunito',19)).place(x=510, y=20)

          #inputs
          self.entry_name=CTkEntry(self.app, width=210, height=33, font=('Nunito',17), text_color=cl.colorsPalette['black'], fg_color=cl.colorsPalette['light blue'])
          self.entry_name.place(x=20, y=50)
          self.entry_description=CTkTextbox(self.app, width=220, height=90, font=('Nunito',17), text_color=cl.colorsPalette['black'], fg_color=cl.colorsPalette['light blue'])
          self.entry_description.place(x=20, y=130)
          self.entry_score=CTkOptionMenu(self.app, values=['0','0.5','1','1.5','2','2.5','3','3.5','4','4.5','5'], font=('Nunito',17), text_color=cl.colorsPalette['black'], fg_color=cl.colorsPalette['light blue'])
          self.entry_score.set('0')
          self.entry_score.place(x=20, y=250)
          self.entry_product=CTkOptionMenu(self.app, font=('Nunito',17), text_color=cl.colorsPalette['black'], fg_color=cl.colorsPalette['light blue'])
          self.entry_product.place(x=270, y=50)
          columns = ("nombre", "descripcion", "puntuacion")
          self.tree = ttk.Treeview(self.app, columns=columns, show='headings', height=13)
          for col in columns:
               self.tree.heading(col, text=col.capitalize())
          self.tree.place(x=510, y=50)
          self.tree.bind('<<TreeviewSelect>>', self.select_review) #event to load review by clicking on it
          CTkButton(self.app, text='Guardar reseña', font=('Nunito',17), text_color=cl.colorsPalette['white'], fg_color=cl.colorsPalette['dark blue'], width=190, hover_color=cl.colorsPalette['light brown'], command=self.save_review).place(x=270, y=290)
          CTkButton(self.app, text='Eliminar reseña', font=('Nunito',17), text_color=cl.colorsPalette['white'], fg_color=cl.colorsPalette['dark blue'], width=190, hover_color=cl.colorsPalette['light brown'], command=self.delete_review).place(x=270, y=335)

          self.fetch_reviews()
          self.app.mainloop()

     def select_review(self, event):
          selected_item=self.tree.selection()
          self.entry_name.delete(0, 'end')
          self.entry_description.delete('1.0', 'end')
          self.entry_score.set('0')

          if not selected_item: return
          values=self.tree.item(selected_item, 'values')
          self.entry_name.insert(0, values[0])
          self.entry_description.insert('1.0', values[1])
          self.entry_score.set(values[2])

     def save_review(self):
          name=self.sanatizeText(self.entry_name.get())
          description=self.sanatizeText(self.entry_description.get('1.0', 'end-1c'))

          if len(name)==0 or len(description)==0:
               messagebox.showwarning("Advertencia", "Los campos no pueden estar vacíos.")
               return
          
          data={
                    'nombre_user':name,
                    'descripcion':description,
                    'puntuacion':self.entry_score.get(),
                    'producto_id':next((p['producto_id'] for p in self.instance.products if p['nombre'] == self.entry_product.get()), None)
               }

          try:
               selected =self.tree.selection()

               if selected:
                    review_id = selected[0]
                    exists=self.instance.supabase.table('resenas').select('resena_id').eq('resena_id', review_id).execute().data

                    if exists:
                         self.instance.supabase.table('resenas').update(data).eq('resena_id', review_id).execute()
                    else:
                         result=self.instance.supabase.table('resenas').insert(data).execute()
                         new_review_id=result.data[0]['resena_id'] if result.data and len(result.data) else review_id
                         self.tree.insert('', 'end', iid=new_review_id, values=(data['nombre_user'], data['descripcion'], data['puntuacion']))
               else:
                    result = self.instance.supabase.table('resenas').insert(data).execute()
                    new_review_id = result.data[0]['resena_id'] if result.data and len(result.data) else None
                    if new_review_id is not None:
                         self.tree.insert('', 'end', iid=new_review_id, values=(data['nombre_user'], data['descripcion'], data['puntuacion']))

               messagebox.showinfo('Exito', 'Reseña guardada correctamente.')
          except Exception as e:
               print(e)
               messagebox.showerror('Error', 'Error al guardar la reseña.')

     def delete_review(self):
          selected = self.tree.selection()
          if not selected:
               messagebox.showwarning("Advertencia", "No se ha seleccionado ninguna reseña.")
               return

          try:
               review_id = selected[0]
               self.instance.supabase.table('resenas').delete().eq('resena_id', review_id).execute()
               self.tree.delete(review_id)
               
               messagebox.showinfo('Exito', 'Reseña eliminada correctamente.')
          except Exception as e:
               print(e)
               messagebox.showerror('Error', 'Error al eliminar la reseña.')
               return

     def load_review(self, *_):
          product=self.entry_product.get()
          self.tree.delete(*self.tree.get_children())
          product_id = next((p['producto_id'] for p in self.instance.products if p['nombre'] == product), None)
          filtered_reviews = [r for r in self.reviews if r['producto_id'] == product_id]

          for review in filtered_reviews:
               self.tree.insert('', 'end', iid=review['resena_id'] , values=(review['nombre_user'], review['descripcion'], review['puntuacion']))
          
     def fetch_reviews(self):
          try:
               productos=[p['nombre'] for p in self.instance.products]
               self.reviews=self.instance.supabase.table('resenas').select('*').execute().data
               self.entry_product.configure(values=productos, command=self.load_review)
               self.entry_product.set(productos[0])
          except Exception as e:
               print(e)
               messagebox.showerror('Error', f'error al cargar las reseñas.')

     def sanatizeText(self, text):
          text=text.strip()
          if re.match(r'^[A-Za-zÀ-ÿ ,\.]+$', text):
               return text
          else: 
               messagebox.showerror('Error', 'Formato de texto no válido.')
               return ''