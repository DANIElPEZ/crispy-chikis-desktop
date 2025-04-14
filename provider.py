from supabase import create_client
import os
from dotenv import load_dotenv

class provider:
     def __init__(self):
          self.supabase=None
          self.__session_user=None
          self.__is_admin=False
          self.products=[]
          self.users=[]
          self.load_client()

     def load_client(self):
          load_dotenv()
          SUPABASE_URL=os.getenv("SUPABASE_URL")
          SUPABASE_KEY=os.getenv("SUPABASE_KEY")
          SUPABASE_KEY_ROLE=os.getenv("SUPABASE_KEY_ROLE")
          self.supabase=create_client(SUPABASE_URL, SUPABASE_KEY_ROLE)
     
     @property
     def session_user(self):
          return self.__session_user
     
     @session_user.setter
     def session_user(self, value):
          self.__session_user=value

     @property
     def is_admin(self):
          return self.__is_admin
     
     @is_admin.setter
     def is_admin(self, value):
          self.__is_admin=value

     def login_in(self, email:str, password:str):
          try:
               response=self.supabase.auth.sign_in_with_password({"email":email, "password":password})
               if response.user:
                    self.session_user=response.user.id
                    self.is_administrator()
          except Exception as e:
               print(f"Error al iniciar sesión: {e}")

     def is_administrator(self):
          try:
               response=self.supabase.table("usuarios").select("es_admin").eq("auth_id", self.session_user).execute()
               if response.data and response.data[0].get("es_admin"):
                    self.__is_admin=True
               else:
                    self.__is_admin=False
          except Exception as e:
               print(f"Error al verificar rol de administrador: {e}")
               self.__is_admin=False

     def fetch_products(self):
          try:
               response=self.supabase.table("productos").select('*').execute()
               if response.data:
                    self.products=response.data
               else:
                    self.products=[]
          except Exception as e:
               print(e)

     def fetch_users(self):
          try:
               response=self.supabase.table("usuarios").select('usuario_id,nombre,email,telefono').execute()
               if response.data:
                    self.users=response.data
               else:
                    self.users=[]
          except Exception as e:
               print(e)