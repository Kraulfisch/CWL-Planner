import pandas as pd
import tkinter.messagebox
import customtkinter

def addEntrys(interface, roster_path):
    try:
        # Read the Excel file
        df = pd.read_excel(roster_path)

        # Ensure the first column exists
        if df.empty or df.columns[0] is None:
            tkinter.messagebox.showerror("Error", "The Excel file is empty or does not have a valid first column.")
            return

        imported_count = 0
        # Iterate through the rows and add each name as an entry
        for index, row in df.iterrows():
            name = str(row[df.columns[0]])  # Get the name from the first column
            if pd.notna(name) and name.strip():  # Ensure the name is not NaN and not empty
                # Add the name with default days (e.g., 1 day)
                interface.entry_name.delete(0, 'end')
                interface.entry_name.insert(0, name.strip())
                interface.entry_days.delete(0, 'end')
                interface.entry_days.insert(0, '1')  # Default days
                interface.add_button_event()
                imported_count += 1

        tkinter.messagebox.showinfo("Upload Confirmed", f"Successfully imported {imported_count} entries from the file.")

    except Exception as e:
        tkinter.messagebox.showerror("Error", f"Failed to import roster: {str(e)}")

def show_confirmation_window(interface, file_path):
        # Create a new Toplevel window for confirmation
        confirmation_window = customtkinter.CTkToplevel(interface)
        confirmation_window.title("Confirm Upload")
        confirmation_window.geometry("500x500")
        confirmation_window.grab_set()

        # Configure grid layout properly
        confirmation_window.grid_columnconfigure(0, weight=1)  # Left column (optional)
        confirmation_window.grid_columnconfigure(1, weight=1)  # Center column (for the content to expand)
        confirmation_window.grid_columnconfigure(2, weight=1)  # Right column
        confirmation_window.grid_rowconfigure((0,1,2,3,4,5,6,7,8,9,10), weight=1)  # Give the first row more weight for expansion

        # Option variable
        interface.option_var = customtkinter.StringVar(value="No")  # Default to unchecked

        # Checkbox for user option
        option_checkbox = customtkinter.CTkCheckBox(confirmation_window, text="Use custom settings?", variable=interface.option_var, onvalue="Yes", offvalue="No")
        option_checkbox.grid(row=0, column=1, padx=(20, 20), pady=(20, 20), sticky="n")
        
        label_eigth_days = customtkinter.CTkLabel(confirmation_window, text="Days for 8 Stars: ", anchor="n")
        label_eigth_days.grid(row=1, column=1, padx=5, pady=(10, 10), sticky="n")
        eight_days = customtkinter.CTkOptionMenu(confirmation_window, values=["3", "4"], 
                                                                       command=interface.change_appearance_mode_event)
        eight_days.grid(row=2, column=1, padx=5, pady=(10, 10), sticky="n")
        # Confirmation button at the bottom-right
        confirm_button = customtkinter.CTkButton(confirmation_window, text="Confirm",
                                                command=lambda: interface.confirm_upload(file_path, interface.option_var.get()))
        confirm_button.grid(row=10, column=2, padx=(20, 20), pady=(20, 20), sticky="se")  # Stick to bottom-right


        # Make sure the Toplevel window is modal (focus on it)
        confirmation_window.transient(interface)
        confirmation_window.grab_set()
        interface.wait_window(confirmation_window)

def confirm_upload(interface, roster_path):
        print(f"File: {roster_path}")
        addEntrys(interface, roster_path)