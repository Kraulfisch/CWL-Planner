import tkinter
import tkinter.messagebox
import customtkinter
from tkinter import filedialog
import createPlan
customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue")


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("CWL LineupPlanner")
        self.geometry(f"{1100}x{580}")

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Lineup Planner", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.sidebar_button_1 = customtkinter.CTkButton(text='Generate', master=self.sidebar_frame, command=self.sidebar_button0_event)
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)
        self.sidebar_button_2 = customtkinter.CTkButton(text='Reset', master=self.sidebar_frame, command=self.sidebar_button1_event)
        self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="CWL Size: ", anchor="w")
        self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=['15', '30'], # add 1 for testing
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))

        # create main entry and button
        self.entry_name = customtkinter.CTkEntry(self, placeholder_text="Name")
        self.entry_name.grid(row=3, column=1, columnspan=1, padx=(20, 0), pady=(20, 20), sticky="nsew")
        self.entry_name.bind("<KeyPress>", self.shortcut)

        self.entry_days = customtkinter.CTkEntry(self, placeholder_text="Days")
        self.entry_days.grid(row=3, column=2, padx=(20, 0), pady=(20, 20), sticky="nsew")
        self.entry_days.bind("<KeyPress>", self.shortcut)

        self.main_button_1 = customtkinter.CTkButton(text='Add', master=self, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), command=self.add_button_event)
        self.main_button_1.grid(row=3, column=3, padx=(20, 20), pady=(20, 20), sticky="nsew")

        # create scrollable frame
        self.scrollable_frame = customtkinter.CTkScrollableFrame(self, label_text="Current Roster")
        self.scrollable_frame.grid(row=0, rowspan=3, column=1, columnspan=3, padx=(20, 20), pady=(20, 0), sticky="nsew")
        self.scrollable_frame.grid_columnconfigure(0, weight=1)  # Name column
        self.scrollable_frame.grid_columnconfigure(1, weight=1)  # Padding column (if needed)
        self.scrollable_frame.grid_columnconfigure(2, weight=1)  # Padding column (if needed)
        self.scrollable_frame.grid_columnconfigure(3, weight=1)  # Days column
        # list to hold dynamically added entries
        self.scrollable_frame_entries = []
        self.totalAmountofDaysEntry = 0
        # set default values
        self.appearance_mode_optionemenu.set("Dark")
        self.scaling_optionemenu.set("15")

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        #print(new_scaling)
        pass

    # generate button
    def sidebar_button0_event(self):
        self.totalAmoutofDaysNeeded = int(self.scaling_optionemenu.get()) * 7
        self.diff = self.totalAmountofDaysEntry - int(self.totalAmoutofDaysNeeded)
        if (self.diff == 0):
            file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", 
                                                 filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")])
            if file_path:
                # Call the create_excel_plan function and pass the roster entries and file path
                createPlan.create_excel_plan(self.scrollable_frame_entries, int(self.scaling_optionemenu.get()), file_path=file_path)
                tkinter.messagebox.showinfo("Success", "Excel file generated successfully!")

        elif self.diff < 0:
            tkinter.messagebox.showwarning("Input Error", f"You have not enough attacks yet. You need {abs(self.diff)} more attacks!")
        
        else:
            tkinter.messagebox.showwarning("Input Error", f"You have too much attacks. You need to remove {self.diff} attacks!")

    # reset button
    def sidebar_button1_event(self):
        if tkinter.messagebox.askyesno(title = 'Reset', message = 'Do you really want to reset the roster?'):
            for name_label, days_label in self.scrollable_frame_entries:
                name_label.destroy()
                days_label.destroy()

        # Clear the list
            self.scrollable_frame_entries.clear()
            self.totalAmountofDaysEntry = 0
    
    # add button
    def add_button_event(self):
        # Get the name and days from the entry fields
        name = self.entry_name.get()
        days = self.entry_days.get()

        if name and days and days.isdigit() and int(days) < 8:  # Only add entry if both fields have values
            # Create new labels in the scrollable frame
            new_label_name = customtkinter.CTkLabel(master=self.scrollable_frame, text=name, width=200, anchor="w")
            new_label_name.grid(row=len(self.scrollable_frame_entries), column=0, columnspan = 1, padx=10, pady=(0, 10), sticky="ew")

            new_label_days = customtkinter.CTkLabel(master=self.scrollable_frame, text=days, width=100, anchor="w")
            new_label_days.grid(row=len(self.scrollable_frame_entries), column=3, padx=10, pady=(0, 0), sticky="ew")

            new_button_delete = customtkinter.CTkButton(master=self.scrollable_frame, text="Delete", command=lambda index=len(self.scrollable_frame_entries): self.delete_entry(index))
            new_button_delete.grid(row=len(self.scrollable_frame_entries), column=4, padx=10, pady=(0, 0), sticky="ew")
            
            # Add labels to the list
            self.scrollable_frame_entries.append((new_label_name, new_label_days, new_button_delete))
            self.totalAmountofDaysEntry += int(days)
            # Clear the input fields after adding
            self.entry_name.delete(0, 'end')
            self.entry_days.delete(0, 'end')

            self.entry_name.focus()

        elif days: 
            tkinter.messagebox.showwarning("Input Error", "Please enter a valid number of days")
        else:
            tkinter.messagebox.showwarning("Input Error", "Please enter both Name and Days.")
    
    def delete_entry(self, index):
    # Ensure the index is valid
        if 0 <= index < len(self.scrollable_frame_entries):
        # Get the entry to delete
            name_label, days_label, delete_button = self.scrollable_frame_entries[index]
            #print(index)
        # Subtract the days from the total
            self.totalAmountofDaysEntry -= int(days_label.cget("text"))

        # Hide the widgets instead of destroying
            name_label.destroy()
            days_label.destroy()
            delete_button.destroy()

        # Remove the entry from the list
            del self.scrollable_frame_entries[index]

        # Re-grid the remaining entries to fill the gap
            for i in range(index, len(self.scrollable_frame_entries)):
                name_label, days_label, delete_button = self.scrollable_frame_entries[i]
                name_label.grid(row=i, column=0, padx=10, pady=(0, 10), sticky="ew")
                days_label.grid(row=i, column=3, padx=10, pady=(0, 0), sticky="ew")
                delete_button.grid(row=i, column=4, padx=10, pady=(0, 0), sticky="ew")
        
            for i in range(index, len(self.scrollable_frame_entries)):
                _, _, delete_button = self.scrollable_frame_entries[i]
                delete_button.configure(command=lambda index=i: self.delete_entry(index))

        else:
            tkinter.messagebox.showwarning("Big Error (should not happen)", f"Invalid index: {index}. Cannot delete entry. Please contact the author")
            #print(f"Invalid index: {index}. Cannot delete entry.")

    def shortcut(self, event):
        if event.keysym == "Return":
            self.add_button_event()

if __name__ == "__main__":
    app = App()
    app.mainloop()
