import tkinter as tk  # Import the tkinter library for creating graphical user interfaces
from tkinter import ttk, messagebox  # Import ttk for themed widgets and messagebox for displaying alerts
from db_connection import get_connection  # Import a custom function to establish a database connection
from mysql.connector import Error  # Import Error class to handle MySQL exceptions

# Define the main application class, inheriting from tkinter.Tk
class Application(tk.Tk):
    def __init__(self):
        super().__init__()  # Call the parent class (Tk) initializer
        self.title("Healthcare App")  # Set the title of the application window
        self.geometry("750x400")  # Define the initial size of the application window
        self.frames = {}  # Dictionary to store different frames (pages) of the application

        # Create instances of the RegistrationPage and SymptomSearchPage
        for F in (RegistrationPage, SymptomSearchPage):
            frame = F(parent=self, controller=self)  # Create an instance of each frame class
            self.frames[F] = frame  # Store the frame instance in the dictionary
            frame.grid(row=0, column=0, sticky="nsew")  # Place frames in the same grid (stacked layout)

        # Display the RegistrationPage by default
        self.show_frame(RegistrationPage)

    def show_frame(self, page_class):
        """
        Display the requested frame (page).
        Args:
            page_class: The class of the frame to display.
        """
        frame = self.frames[page_class]  # Retrieve the frame instance from the dictionary
        frame.tkraise()  # Bring the selected frame to the front

# Define the RegistrationPage class
class RegistrationPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)  # Call the parent class (Frame) initializer
        self.controller = controller  # Reference to the main Application class (controller)

        # Create the UI for the registration page
        ttk.Label(self, text="Register", font=("Helvetica", 16, "bold")).pack(pady=10)  # Title label

        # Name input field
        ttk.Label(self, text="Name").pack(anchor="w", padx=20)  # Label for the name input
        self.entry_name = ttk.Entry(self, width=30)  # Entry widget for name
        self.entry_name.pack(pady=5, padx=20)  # Pack the name entry widget

        # Email input field
        ttk.Label(self, text="Email").pack(anchor="w", padx=20)  # Label for the email input
        self.entry_email = ttk.Entry(self, width=30)  # Entry widget for email
        self.entry_email.pack(pady=5, padx=20)  # Pack the email entry widget

        # Password input field
        ttk.Label(self, text="Password").pack(anchor="w", padx=20)  # Label for the password input
        self.entry_password = ttk.Entry(self, width=30, show="*")  # Password entry (masked with asterisks)
        self.entry_password.pack(pady=5, padx=20)  # Pack the password entry widget

        # Register button
        ttk.Button(self, text="Register", command=self.register_user).pack(pady=20)

    def register_user(self):
        """
        Handle the user registration process.
        """
        name = self.entry_name.get()  # Retrieve the entered name
        email = self.entry_email.get()  # Retrieve the entered email
        password = self.entry_password.get()  # Retrieve the entered password

        # Check if all fields are filled
        if name and email and password:
            try:
                conn = get_connection()  # Establish a database connection
                cursor = conn.cursor()  # Create a cursor for executing SQL commands
                # Insert the user information into the 'users' table
                cursor.execute(
                    "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)",
                    (name, email, password)
                )
                conn.commit()  # Commit the changes to the database
                messagebox.showinfo("Success", "Registration successful!")  # Success message
                self.controller.show_frame(SymptomSearchPage)  # Navigate to the SymptomSearchPage
            except Error as e:  # Handle any database errors
                messagebox.showerror("Database Error", f"Error: {e}")  # Display an error message
            finally:
                if conn:  # Close the database connection
                    conn.close()
        else:
            messagebox.showwarning("Input Error", "All fields are required!")  # Warn if any field is empty

# Define the SymptomSearchPage class
class SymptomSearchPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)  # Call the parent class (Frame) initializer
        self.controller = controller  # Reference to the main Application class (controller)

        # Create the UI for the symptom search page
        ttk.Label(self, text="Search for Doctors", font=("Helvetica", 16, "bold")).pack(pady=10)  # Title label

        # Symptoms input field
        ttk.Label(self, text="Enter Symptoms").pack(anchor="w", padx=20)  # Label for symptom input
        self.entry_symptoms = ttk.Entry(self, width=40)  # Entry widget for symptoms
        self.entry_symptoms.pack(pady=5, padx=20)  # Pack the symptoms entry widget

        # Search button
        ttk.Button(self, text="Search", command=self.search_doctors).pack(pady=10)

        # Treeview for displaying search results
        ttk.Label(self, text="Search Results").pack(anchor="w", padx=20)  # Label for results
        columns = ("Name", "Specialty", "Rating", "Education", "Description", "Contact Number")  # Table columns
        self.result_text = ttk.Treeview(self, columns=columns, show="headings", height=10)  # Create the Treeview

        # Define column headings and widths
        for col in columns:
            self.result_text.heading(col, text=col)  # Set the column heading
            self.result_text.column(col, width=100 if col != "Description" else 200)  # Set column width

        self.result_text.pack(pady=10, padx=20, fill="x")  # Pack the Treeview widget

    def search_doctors(self):
        """
        Search for doctors based on symptoms.
        """
        symptoms = self.entry_symptoms.get()  # Get the symptoms entered by the user
        try:
            conn = get_connection()  # Establish a database connection
            cursor = conn.cursor()  # Create a cursor for executing SQL commands
            # Query to find doctors based on symptoms
            query = """
            SELECT name, specialty, rating, education, description, contact_number
            FROM doctors
            WHERE symptoms LIKE %s
            """
            cursor.execute(query, (f"%{symptoms}%",))  # Execute the query with the symptoms parameter
            results = cursor.fetchall()  # Fetch all matching results
        except Error as e:  # Handle database errors
            messagebox.showerror("Database Error", f"Error: {e}")  # Display an error message
            results = []  # Set results to an empty list on error
        finally:
            if conn:  # Close the database connection
                conn.close()

        # Display the search results in the Treeview
        self.result_text.delete(*self.result_text.get_children())  # Clear previous results
        if results:
            for doctor in results:  # Insert each doctor's details into the Treeview
                self.result_text.insert("", "end", values=doctor)
        else:
            messagebox.showinfo("No Results", "No matching doctors found.")  # Inform if no results found

# Run the application
if __name__ == "__main__":
    app = Application()  # Create an instance of the Application class
    app.mainloop()  # Start the application's main event loop
