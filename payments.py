from customtkinter import CTk, CTkButton, set_appearance_mode
from tkinter import messagebox, ttk
import colors as cl
from tkinter.filedialog import asksaveasfilename
import csv

class payments:
     def __init__(self, instance):
          self.instance=instance
          set_appearance_mode('light')
          self.app=CTk()
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

          columns=('Id','Fecha','Nombre','Metodo de pago', 'Monto')
          self.tree = ttk.Treeview(self.app, columns=columns, show='headings', height=16)
          for col in columns:
               self.tree.heading(col, text=col.capitalize())
          self.tree.place(x=20, y=20)

          CTkButton(self.app, text='Guardar csv', font=('Nunito', 17), text_color=cl.colorsPalette['white'],
                    fg_color=cl.colorsPalette['dark brown'], hover_color=cl.colorsPalette['light brown'], command=self.export).place(x=20, y=380)
          self.load_data()
          self.app.mainloop()

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
                    
                    headers = self.tree["columns"]
                    writer.writerow(headers)
                    
                    for row_id in self.tree.get_children():
                         row = self.tree.item(row_id)['values']
                         writer.writerow(row)
               messagebox.showinfo("Éxito", f"Datos exportados correctamente a {file_path}")
          except Exception as e:
               messagebox.showerror("Error", f"Error al exportar a CSV: {e}")

     def load_data(self):
          self.instance.fetch_users()
          try:
               pagos_response = self.instance.supabase.table("pagos").select("*").execute()
               if pagos_response.data:
                    orden_ids = [pago["orden_id"] for pago in pagos_response.data if pago["orden_id"] is not None]
                    
                    ordenes_response = self.instance.supabase.table("ordenes") \
                         .select("orden_id, fecha_creacion_pedido, usuario_id, precio_total") \
                         .in_("orden_id", orden_ids).execute()
                    ordenes_data = ordenes_response.data if ordenes_response.data else []
                    usuario_ids = [orden["usuario_id"] for orden in ordenes_data if orden["usuario_id"] is not None]
                    usuarios_response = self.instance.supabase.table("usuarios") \
                         .select("usuario_id, nombre, email, telefono") \
                         .in_("usuario_id", usuario_ids).execute()
                    
                    usuarios_data = usuarios_response.data if usuarios_response.data else []
                    usuarios_dict = {user["usuario_id"]: user["nombre"] for user in usuarios_data}
                    for pago in pagos_response.data:
                         orden = next((o for o in ordenes_data if o["orden_id"] == pago["orden_id"]), None)
                         
                         if orden:
                              nombre_usuario = usuarios_dict.get(orden["usuario_id"], "Desconocido")
                              metodo_pago = "efectivo" if pago["metodo"] == 1 else "tarjeta" if pago["metodo"] == 2 else "indefinido"
                              self.tree.insert(
                                   '',
                                   'end',
                                   values=(
                                        orden["orden_id"],
                                        orden["fecha_creacion_pedido"],
                                        nombre_usuario,
                                        metodo_pago,
                                        orden["precio_total"]
                                   )
                              )
               else:
                    messagebox.showinfo('Info', 'No hay pagos registrados')
          except Exception as e:
               messagebox.showerror('Error', f'Error al cargar datos: {e}')

