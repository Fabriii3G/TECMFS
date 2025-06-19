import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import requests
import os

# Dirección del Controller Node
CONTROLLER_URL = "http://127.0.0.1:5000"


class TECMFSClientApp:
    def __init__(self, root):
        self.root = root
        self.root.title("TEC Media File System")
        self.root.geometry("600x400")

        self.search_var = tk.StringVar()

        # Widgets
        self.setup_widgets()

        # Cargar archivos iniciales
        self.update_file_list()

    def setup_widgets(self):
        # Botones
        tk.Button(self.root, text="Agregar PDF", command=self.upload_file).pack(pady=10)

        search_frame = tk.Frame(self.root)
        search_frame.pack(pady=5)

        tk.Label(search_frame, text="Buscar:").pack(side=tk.LEFT)
        tk.Entry(search_frame, textvariable=self.search_var).pack(side=tk.LEFT)
        tk.Button(search_frame, text="Buscar", command=self.search_files).pack(side=tk.LEFT)

        self.file_listbox = tk.Listbox(self.root, width=60, height=15)
        self.file_listbox.pack(pady=10)

        tk.Button(self.root, text="Eliminar seleccionado", command=self.delete_file).pack()
        tk.Button(self.root, text="Descargar seleccionado", command=self.download_file).pack()

    def upload_file(self):
        filepath = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
        if not filepath:
            return

        filename = os.path.basename(filepath)
        try:
            with open(filepath, "rb") as f:
                file_data = list(f.read())

            response = requests.post(f"{CONTROLLER_URL}/upload_file", json={
                "filename": filename,
                "data": file_data
            })

            if response.status_code == 200:
                messagebox.showinfo("Éxito", f"Archivo '{filename}' subido correctamente.")
                self.update_file_list()
            else:
                messagebox.showerror("Error", f"Error al subir archivo:\n{response.text}")

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo subir el archivo: {e}")

    def update_file_list(self):
        try:
            response = requests.get(f"{CONTROLLER_URL}/list_files")
            if response.status_code == 200:
                files = response.json().get("files", [])
                self.file_listbox.delete(0, tk.END)

                # Mostrar solo archivos que terminan en .pdf
                for name in files:
                    if name.lower().endswith('.pdf'):
                        self.file_listbox.insert(tk.END, name)
            else:
                messagebox.showerror("Error", "No se pudo obtener la lista de archivos.")
        except Exception as e:
            messagebox.showerror("Error", f"Conexión fallida: {e}")

    def search_files(self):
        term = self.search_var.get().lower()
        for i in range(self.file_listbox.size()):
            filename = self.file_listbox.get(i).lower()
            self.file_listbox.itemconfig(i, {'bg': 'white'})
            if term in filename:
                self.file_listbox.selection_clear(0, tk.END)
                self.file_listbox.selection_set(i)
                self.file_listbox.itemconfig(i, {'bg': '#b3ffb3'})

    def delete_file(self):
        selection = self.file_listbox.curselection()
        if not selection:
            messagebox.showwarning("Advertencia", "Seleccione un archivo para eliminar.")
            return

        filename = self.file_listbox.get(selection[0])
        confirm = messagebox.askyesno("Confirmar", f"¿Eliminar '{filename}'?")
        if not confirm:
            return

        try:
            response = requests.delete(f"{CONTROLLER_URL}/delete_file", params={"filename": filename})
            if response.status_code == 200:
                messagebox.showinfo("Éxito", "Archivo eliminado correctamente.")
                self.update_file_list()
            else:
                messagebox.showerror("Error", f"No se pudo eliminar:\n{response.text}")
        except Exception as e:
            messagebox.showerror("Error", f"Conexión fallida: {e}")

    def download_file(self):
        selection = self.file_listbox.curselection()
        if not selection:
            messagebox.showwarning("Advertencia", "Seleccione un archivo para descargar.")
            return

        filename = self.file_listbox.get(selection[0])
        save_path = filedialog.asksaveasfilename(defaultextension=".pdf", initialfile=filename)

        if not save_path:
            return

        try:
            response = requests.get(f"{CONTROLLER_URL}/download_file", params={"filename": filename})
            if response.status_code == 200:
                json_data = response.json()
                file_bytes = bytes(json_data.get("data"))
                with open(save_path, "wb") as f:
                    f.write(file_bytes)
                messagebox.showinfo("Éxito", f"Archivo '{filename}' descargado correctamente.")
            else:
                messagebox.showerror("Error", f"No se pudo descargar el archivo:\n{response.text}")
        except Exception as e:
            messagebox.showerror("Error", f"Conexión fallida: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = TECMFSClientApp(root)
    root.mainloop()
