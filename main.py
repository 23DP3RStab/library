import customtkinter as ctk
import tkinter as tk
import tkinter.ttk as ttk
import os
import json
import random
import datetime

class library(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Library")
        self.resizable(False, False)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(4, weight=1)
        self._set_appearance_mode("dark")
        self.center(self, 625, 450)
        self.iconbitmap("icon.ico")
        self.frame = ctk.CTkFrame(self)
        self.frame.grid_columnconfigure(4, weight=1)
        self.frame.grid_columnconfigure(2, weight=1)
        self.frame.grid(pady= 10, padx= 10, column=1, columnspan=1, row=4, rowspan=1, sticky="sew")

        self.add_book_button = ctk.CTkButton(self.frame, text="Add Book", command=self.open_add_book_window)
        self.add_book_button.grid(pady=(10, 5), padx=(10, 5), column=0, columnspan=1, row=0, rowspan=1, sticky="sew")

        self.delete_book_button = ctk.CTkButton(self.frame, text="Delete Book", command=self.delete_book)
        self.delete_book_button.grid(pady=(5, 10), padx=(10, 5), column=0, columnspan=1, row=1, rowspan=1, sticky="sew")

        self.borrow_button = ctk.CTkButton(self.frame, text="Borrow Book", command=self.open_borrow_book_window)
        self.borrow_button.grid(pady=(10, 5), padx=5, column=1, columnspan=1, row=0, rowspan=1, sticky="sew")

        self.return_button = ctk.CTkButton(self.frame, text="Return Book", command=self.open_return_book_window)
        self.return_button.grid(pady=(5, 10), padx=5, column=1, columnspan=1, row=1, rowspan=1, sticky="sew")

        self.search_methods = ['Name', 'ID', 'Author', 'Year', 'Status']
        self.search_method = ctk.StringVar()
        self.search_method.set(self.search_methods[0])
        self.search_method_combobox = ctk.CTkComboBox(self.frame, variable=self.search_method, values=self.search_methods, state="readonly")
        self.search_method_combobox.grid(pady=(10, 5), padx=5, column=2, columnspan=1, row=0, rowspan=1, sticky="sew")

        self.search_query = tk.StringVar()
        self.search_entry = ctk.CTkEntry(self.frame, textvariable=self.search_query)
        self.search_entry.grid(pady=(5, 10), padx=5, column=2, columnspan=1, row=1, rowspan=1, sticky="sew")

        self.search_button = ctk.CTkButton(self.frame, text="Search Book", command=self.search_book)
        self.search_button.grid(pady=(10, 5), padx=(5, 10), column=3, columnspan=1, row=0, rowspan=1, sticky="sew")

        # self.history_button = ctk.CTkButton(self.frame, text="Book History", command=self.open_book_history_window)
        # self.history_button.grid()

        if not os.path.exists('books.json'):
            with open('books.json', 'w') as f:
                json.dump([], f)

        if not os.path.exists('borrow_history.json'):
            with open('borrow_history.json', 'w') as f:
                json.dump([], f)

        self.style = ttk.Style()
        self.style.theme_use("default")
        self.style.map("Custom.Treeview", background=[('selected', '#1f6aa5')], foreground=[('selected', '#ffffff')])
        self.style.configure("Custom.Treeview.Heading", background="#242424", foreground="#ffffff", borderwidth=0, highlightthickness=0)
        self.style.configure("Custom.Treeview", background="#242424", fieldbackground="#242424", foreground="#ffffff", borderwidth=0, highlightthickness=0)

        self.tree = ttk.Treeview(self, height=15, style="Custom.Treeview")  
        self.tree["columns"]=("ID", "author","year", "status")
        self.tree.column("#0", width=270, minwidth=270, stretch=tk.NO)
        self.tree.column("ID", width=50, minwidth=50, stretch=tk.NO)
        self.tree.column("author", width=150, minwidth=150, stretch=tk.NO)
        self.tree.column("year", width=50, minwidth=50, stretch=tk.NO)
        self.tree.column("status", width=150, minwidth=150, stretch=tk.NO)

        self.tree.heading("#0",text="Name",anchor=tk.W)
        self.tree.heading("ID", text="ID",anchor=tk.W)
        self.tree.heading("author", text="Author",anchor=tk.W)
        self.tree.heading("year", text="Year",anchor=tk.W)
        self.tree.heading("status", text="Status",anchor=tk.W)

        self.load_books_into_tree()

        self.tree.grid(padx=10, pady=10, column=1, columnspan=1, row=0, rowspan=4, sticky="nsew")


    def load_books_into_tree(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        with open('books.json', 'r') as f:
            books = json.load(f)
            print(books)
            for book in books:
                self.tree.insert("", 0, text=book["name"], values=(book["id"], book["author"], book["year"], book["status"]))


    def open_add_book_window(self):
        self.add_book_window = tk.Toplevel(self)
        self.add_book_window.title("Add Book")

        self.book_name_entry = ttk.Entry(self.add_book_window)
        self.book_name_entry.grid(row=0, column=1)
        self.book_name_label = ttk.Label(self.add_book_window, text="Book Name:")
        self.book_name_label.grid(row=0, column=0)

        self.author_entry = ttk.Entry(self.add_book_window)
        self.author_entry.grid(row=1, column=1)
        self.author_label = ttk.Label(self.add_book_window, text="Author:")
        self.author_label.grid(row=1, column=0)

        self.year_entry = ttk.Entry(self.add_book_window)
        self.year_entry.grid(row=2, column=1)
        self.year_label = ttk.Label(self.add_book_window, text="Year of Release:")
        self.year_label.grid(row=2, column=0)

        self.save_button = ttk.Button(self.add_book_window, text="Save Book", command=self.save_book)
        self.save_button.grid(row=3, column=0, columnspan=2)


    def delete_book(self):
        try:
            selected_item = self.tree.selection()[0]
            book_name = self.tree.item(selected_item)['text']
            with open('books.json', 'r+') as f:
                books = json.load(f)
                books = [book for book in books if book['name'] != book_name]
                f.seek(0)
                f.truncate()
                json.dump(books, f)
            self.tree.delete(selected_item)
        except IndexError:
            self.create_message_box("No book selected for deletion.")


    def save_book(self):
        book_name = self.book_name_entry.get()
        author = self.author_entry.get()
        year = self.year_entry.get()

        if not book_name or not author or not year:
            self.create_message_box("You need to fill out all fields.")
            return

        try:
            year = int(year)
        except ValueError:
            self.create_message_box("Year must be an integer.")
            return

        book_id = random.randint(10000, 99999)

        book = {
            "id": book_id,
            "name": book_name,
            "author": author,
            "year": year,
            "status": "Available"
        }

        with open('books.json', 'r+') as f:
            books = json.load(f)
            if any(b['id'] == book_id or b['name'] == book_name for b in books):
                self.create_message_box("Book already exists or ID conflict!")
            else:
                books.append(book)
                f.seek(0)
                json.dump(books, f)
                self.add_book_window.destroy()
                self.after(100, self.load_books_into_tree)


    def create_message_box(self, message):
        message_box = ctk.CTkToplevel(self)
        self.center(message_box, 200, 100)
        message_box.title("!")
        message_box.resizable(False, False)
        message_box.attributes("-topmost", True)

        message_label = ctk.CTkLabel(message_box, text=message)
        message_label.pack(padx=10, pady=(10, 5))

        ok_button = ctk.CTkButton(message_box, text="OK", command=message_box.destroy)
        ok_button.pack(padx=10, pady=(5, 10))


    def open_borrow_book_window(self):
        self.borrow_book_window = tk.Toplevel(self)
        self.borrow_book_window.title("Borrow Book")

        self.borrower_name_entry = ttk.Entry(self.borrow_book_window)
        self.borrower_name_entry.grid(row=0, column=1)
        self.borrower_name_label = ttk.Label(self.borrow_book_window, text="Your Name:")
        self.borrower_name_label.grid(row=0, column=0)

        self.book_id_entry = ttk.Entry(self.borrow_book_window)
        self.book_id_entry.grid(row=1, column=1)
        self.book_id_label = ttk.Label(self.borrow_book_window, text="Book ID:")
        self.book_id_label.grid(row=1, column=0)

        self.borrow_button = ttk.Button(self.borrow_book_window, text="Borrow", command=self.borrow_book)
        self.borrow_button.grid(row=2, column=1)

        try:
            selected_item = self.tree.selection()[0]
            book_id = self.tree.item(selected_item)['values'][0]
            self.book_id_entry.insert(0, book_id)
        except IndexError:
            pass


    def borrow_book(self):
        borrower_name = self.borrower_name_entry.get()
        book_id = int(self.book_id_entry.get())
    
        with open('books.json', 'r+') as f:
            books = json.load(f)
            for book in books:
                if book["id"] == book_id:
                    if book["status"] == "Available":
                        book["status"] = "Unavailable"
                        book["borrower"] = borrower_name
                        book["borrowed_at"] = str(datetime.datetime.now())
                        f.seek(0)
                        json.dump(books, f)
                        self.borrow_book_window.destroy()
                        self.after(100, self.load_books_into_tree)
    
                        with open('borrow_history.json', 'r+') as history_file:
                            history = json.load(history_file)
                            history.append({
                                'book_id': book_id,
                                'borrower': borrower_name,
                                'borrowed_at': str(datetime.datetime.now())
                            })
                            history_file.seek(0)
                            json.dump(history, history_file)
    
                        return
                    else:
                        self.create_message_box("Book is unavailable!")
                        return
            self.create_message_box("Book ID not found!")


    def open_return_book_window(self):
        self.return_book_window = tk.Toplevel(self)
        self.return_book_window.title("Return Book")
    
        self.returner_name_entry = ttk.Entry(self.return_book_window)
        self.returner_name_entry.grid(row=0, column=1)
        self.returner_name_label = ttk.Label(self.return_book_window, text="Your Name:")
        self.returner_name_label.grid(row=0, column=0)
    
        self.return_book_id_entry = ttk.Entry(self.return_book_window)
        self.return_book_id_entry.grid(row=1, column=1)
        self.return_book_id_label = ttk.Label(self.return_book_window, text="Book ID:")
        self.return_book_id_label.grid(row=1, column=0)
    
        try:
            selected_item = self.tree.selection()[0]
            book_id = self.tree.item(selected_item)['values'][0]
            self.return_book_id_entry.insert(0, book_id)
        except IndexError:
            pass

        self.return_button = ttk.Button(self.return_book_window, text="Return", command=self.return_book)
        self.return_button.grid(row=2, column=1)
    

    def return_book(self):
        returner_name = self.returner_name_entry.get()
        book_id = int(self.return_book_id_entry.get())

        with open('books.json', 'r+') as f:
            books = json.load(f)
            for book in books:
                if book["id"] == book_id:
                    if book["status"] != "Available" and book["borrower"] == returner_name:
                        book["status"] = "Available"
                        book["borrower"] = ""
                        f.seek(0)
                        f.truncate()
                        json.dump(books, f)
                        self.return_book_window.destroy()
                        self.after(100, self.load_books_into_tree)

                        with open('borrow_history.json', 'r+') as history_file:
                            history = json.load(history_file)
                            history.append({
                                'book_id': book_id,
                                'returner': returner_name,
                                'returned_at': str(datetime.datetime.now())
                            })
                            history_file.seek(0)
                            json.dump(history, history_file)

                        return
                    else:
                        self.create_message_box("Book is not borrowed by you!")
                        return
            self.create_message_box("Book ID not found!")


    def search_book(self):
        search_method = self.search_method.get().lower()
        search_query = self.search_query.get().lower()

        method_to_key = {
            'name': 'name',
            'id': 'id',
            'author': 'author',
            'year': 'year',
            'status': 'status'
        }

        with open('books.json', 'r') as f:
            books = json.load(f)
            search_results = [book for book in books if search_query in str(book[method_to_key[search_method]]).lower()]

        for i in self.tree.get_children():
            self.tree.delete(i)
        for book in search_results:
            self.tree.insert('', 'end', text=book['name'], values=(book['id'], book['author'], book['year'], book['status']))


    # def open_book_history_window(self):
    #     self.history_window = tk.Toplevel(self)
    #     self.history_window.title("Book History")

    #     self.book_id = tk.StringVar()
    #     self.book_id_entry = ttk.Entry(self.history_window, textvariable=self.book_id)
    #     self.book_id_entry.pack()

    #     self.show_history_button = ttk.Button(self.history_window, text="Show History", command=self.show_book_history)
    #     self.show_history_button.pack()


    # def show_book_history(self):
    #     book_id = self.book_id.get()

    #     with open('borrow_history.json', 'r') as f:
    #         borrow_history = json.load(f)
    #         book_history = [history for history in borrow_history if 'book_id' in history and history['book_id'] == book_id]

    #     history_text = "\n".join([f"Borrowed by {history["borrower"]}, returned by: {history["returner"]}" for history in book_history])

    #     self.history_label = tk.Label(self.history_window, text=history_text)
    #     self.history_label.pack()


    def center(self, window, width, height):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = int((screen_width/2) - (width/2))
        y = int((screen_height/2) - (height/2))
        window.geometry('%dx%d+%d+%d' % (width, height, x, y))



if __name__ == "__main__":
    app = library()
    app.mainloop()