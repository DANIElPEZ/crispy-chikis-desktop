import colors as cl
from customtkinter import CTkToplevel, CTkImage, CTkLabel, CTkButton, CTkEntry, CTkOptionMenu, set_appearance_mode
from tkinter import messagebox, ttk
from PIL import Image
from tkinter.filedialog import asksaveasfilename
import csv
from collections import Counter

class orders:
     def __init__(self, instance, app):
          self.instance=instance
          self.orders_list=[]
          set_appearance_mode('light')
          self.app=CTkToplevel(app)
          self.app.grab_set()
          window_width = 1050
          window_height = 430
          screen_width = self.app.winfo_screenwidth()
          screen_height = self.app.winfo_screenheight()
          x = int((screen_width / 2) - (window_width / 2))
          y = int((screen_height / 2) - (window_height / 2))
          self.app.geometry(f"{window_width}x{window_height}+{x}+{y}")
          self.app.title('Menu principal')
          self.app.resizable(0,0)
          self.app.configure(fg_color=cl.colorsPalette['dark blue'])
          self.app.iconbitmap('assets/logo.ico')

          CTkLabel(self.app, text='Nombre', text_color=cl.colorsPalette['white'], font=('Nunito', 19)).place(x=20, y=20)
          CTkLabel(self.app, text='Telefono', text_color=cl.colorsPalette['white'], font=('Nunito', 19)).place(x=20, y=90)
          CTkLabel(self.app, text='Email', text_color=cl.colorsPalette['white'], font=('Nunito', 19)).place(x=20, y=160)
          CTkLabel(self.app, text='Estado', text_color=cl.colorsPalette['white'], font=('Nunito', 19)).place(x=20, y=230)
          CTkLabel(self.app, text='Ver Pedido', text_color=cl.colorsPalette['white'], font=('Nunito', 19)).place(x=280, y=20)
          CTkLabel(self.app, text='Filtrar estado', text_color=cl.colorsPalette['white'], font=('Nunito', 19)).place(x=730, y=20)

          self.entry_name = CTkEntry(self.app, width=210, height=33, font=('Nunito', 17),
                                        text_color=cl.colorsPalette['white'], fg_color=cl.colorsPalette['light brown'])
          self.entry_name.place(x=20, y=50)
          self.entry_number = CTkEntry(self.app, width=210, height=33, font=('Nunito', 17),
                                        text_color=cl.colorsPalette['white'], fg_color=cl.colorsPalette['light brown'])
          self.entry_number.place(x=20, y=120)
          self.entry_phone = CTkEntry(self.app, width=210, height=33, font=('Nunito', 17),
                                        text_color=cl.colorsPalette['white'], fg_color=cl.colorsPalette['light brown'])
          self.entry_phone.place(x=20, y=190)
          self.entry_status = CTkOptionMenu(self.app, font=('Nunito', 17), values=['Pendidente', 'Cancelado'],
                                             text_color=cl.colorsPalette['white'], fg_color=cl.colorsPalette['light brown'])
          self.entry_status.place(x=20, y=260)

          self.entry_status_tree = CTkOptionMenu(self.app, font=('Nunito', 17), values=['Todos','Pendidente', 'Cancelado'],
                                             text_color=cl.colorsPalette['white'], fg_color=cl.colorsPalette['light brown'], command=self.filter_orders)
          self.entry_status_tree.set('Todos')
          self.entry_status_tree.place(x=850, y=20)

          columns=('Id','Fecha','Estado')
          self.tree = ttk.Treeview(self.app, columns=columns, show='headings', height=13)
          for col in columns:
               self.tree.heading(col, text=col.capitalize())
          self.tree.place(x=430, y=70)
          self.tree.bind('<<TreeviewSelect>>', self.load_order)

          CTkButton(self.app, text='Actualizar tabla', font=('Nunito', 17), text_color=cl.colorsPalette['white'],
                    fg_color=cl.colorsPalette['dark brown'], hover_color=cl.colorsPalette['light brown'], width=160, height=40, command=self.update_data).place(x=250, y=300)
          
          CTkButton(self.app, text='Guardar csv', font=('Nunito', 17), text_color=cl.colorsPalette['white'],
                    fg_color=cl.colorsPalette['dark brown'], hover_color=cl.colorsPalette['light brown'], command=self.export).place(x=850, y=380)
          
          self.add_image = CTkImage(light_image=Image.open('assets/list.png'),
                                   dark_image=Image.open('assets/list.png'), size=(70, 70))
          CTkButton(self.app, text='', image=self.add_image, fg_color=cl.colorsPalette['light blue'],
                    hover_color=cl.colorsPalette['light green'], width=30, command=self.watch_order_client).place(x=280, y=50)
          CTkButton(self.app, text='Actualizar estado', font=('Nunito', 17), text_color=cl.colorsPalette['white'],
                    fg_color=cl.colorsPalette['dark brown'], hover_color=cl.colorsPalette['light brown'], width=160, height=40, command=self.update_order).place(x=20, y=370)
          self.load_data()

     def watch_order_client(self):
          selected_item = self.tree.selection()
          if selected_item:
               order_id = self.tree.item(selected_item)['values'][0]
               order = next((order for order in self.orders_list if order['orden_id'] == order_id), None)
               
               if not order: return

               order_list=order['productos']
               product_counts = Counter(order_list)

               watch_order=CTkToplevel(self.app)
               watch_order.grab_set()
               window_width =440
               window_height = 300
               screen_width = self.app.winfo_screenwidth()
               screen_height = self.app.winfo_screenheight()
               x = int((screen_width / 2) - (window_width / 2))
               y = int((screen_height / 2) - (window_height / 2))
               watch_order.geometry(f"{window_width}x{window_height}+{x}+{y}")
               watch_order.title('Orden del cliente')
               watch_order.resizable(0,0)
               watch_order.configure(fg_color=cl.colorsPalette['dark blue'])
               watch_order.iconbitmap('assets/logo.ico')
               columns=('Cantidad','Nombre')
               tree=ttk.Treeview(watch_order, columns=columns, show='headings', height=12)
               for col in columns:
                    tree.heading(col, text=col.capitalize())
               tree.place(x=20, y=20)
               for producto_id, cantidad in product_counts.items():
                    producto = next((p for p in self.instance.products if p['producto_id'] == producto_id), None)
                    if producto:
                         tree.insert('', 'end', values=(cantidad, producto['nombre']))

     def update_order(self):
          selected_item = self.tree.selection()
          if selected_item:
               order_id = self.tree.item(selected_item)['values'][0]
               order = next((order for order in self.orders_list if order['orden_id'] == order_id), None)
               if order:
                    new_status = 2 if order['estado'] == 1 else 1
                    print(f"Estado actual: {order['estado']}")
                    self.instance.supabase.table("ordenes").update({"estado": new_status}).eq("orden_id", order_id).execute()
                    messagebox.showinfo('Exito', 'Estado actualizado')
          else:
               messagebox.showerror('Error', 'Seleccione un pedido para actualizar')
          self.update_data()

     def load_data(self):
          self.instance.fetch_products()
          self.instance.fetch_users()
          self.orders_list=self.instance.supabase.table("ordenes").select("*").execute().data
          self.tree.delete(*self.tree.get_children())
          for order in self.orders_list:
               self.tree.insert('', 'end', iid=order['orden_id'] ,values=(order['orden_id'], order['fecha_creacion_pedido'], 'Pendiente' if order['estado']==1 else 'Cancelado'))

     def export(self):
          file_path = asksaveasfilename(
               defaultextension=".csv", 
               filetypes=[("Archivos CSV", "*.csv")],
               title="Guardar archivo CSV"
          )
          if not file_path: return

          try:
               with open(file_path, mode="w", newline="", encoding="utf-8") as csvfile:
                    writer = csv.writer(csvfile)
                    
                    writer.writerow(["Id", "Fecha", "Nombre usuario", "Teléfono", "Correo"])

                    for order in self.orders_list:
                         user = next((u for u in self.instance.users if u['usuario_id'] == order['usuario_id']), None)
                         if user:
                              row = [
                                   order['orden_id'],
                                   order['fecha_creacion_pedido'],
                                   user.get('nombre', ''),
                                   user.get('telefono', ''),
                                   user.get('email', '')
                              ]
                         writer.writerow(row)
               messagebox.showinfo("Éxito", f"Datos exportados correctamente a {file_path}")
          except Exception as e:
               messagebox.showerror("Error", f"Error al exportar a CSV: {e}")

     def update_data(self):
          self.load_data()

     def load_order(self, *_):
          self.entry_name.delete(0, 'end')
          self.entry_number.delete(0, 'end')
          self.entry_phone.delete(0, 'end')
          selected_item = self.tree.selection()
          if selected_item:
               order_id = self.tree.item(selected_item)['values'][0]
               order = next((order for order in self.orders_list if order['orden_id'] == order_id), None)
               user=next((user for user in self.instance.users if user['usuario_id'] == order['usuario_id']), None)
               if order:
                    self.entry_status.set('Pendiente' if order['estado'] == 1 else 'Cancelado')
                    if user:
                         self.entry_name.insert(0, user['nombre'])
                         self.entry_number.insert(0, user['telefono'])
                         self.entry_phone.insert(0, user['email'])

     def filter_orders(self, *_):
          self.tree.delete(*self.tree.get_children())
          filter_value = self.entry_status_tree.get()
          if filter_value == 'Todos':
               for order in self.orders_list:
                    self.tree.insert('', 'end', iid=order['orden_id'] ,values=(order['orden_id'], order['fecha_creacion_pedido'], 'Pendiente' if order['estado']==1 else 'Cancelado'))
          
          elif filter_value == 'Pendidente':
               for order in self.orders_list:
                    if order['estado'] == 1:
                         self.tree.insert('', 'end', iid=order['orden_id'] ,values=(order['orden_id'], order['fecha_creacion_pedido'], 'Pendiente'))
          
          elif filter_value == 'Cancelado':
               for order in self.orders_list:
                    if order['estado'] == 2:
                         self.tree.insert('', 'end', iid=order['orden_id'] ,values=(order['orden_id'], order['fecha_creacion_pedido'], 'Cancelado'))