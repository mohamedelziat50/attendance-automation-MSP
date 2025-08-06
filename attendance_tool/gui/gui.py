"""
GUI Module for Attendance Automation Tool

This module contains the main GUI interface for the attendance tool.
It provides a user-friendly graphical interface to process CSV files
"""

import customtkinter as ctk
from tkinter import filedialog, messagebox
import os

# Import the core functionality from the parent package
from ..processor import Processor
from ..exporter import Exporter

# Configure CustomTkinter
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")


class AttendanceExporterApp(ctk.CTk):
    """
    GUI application for processing CSV attendance files and exporting to Word/PDF.
    Inherits customtkinter's functionality.
    """
    def __init__(self):
        super().__init__()
        
        # Window configuration
        self.title("MSP Attendance Exporter")
        self.geometry("400x650")  # Made slightly taller to accommodate content
        self.resizable(False, False)
        
        # Variables to store file path and title
        self.csv_file_path = None
        self.report_title = "Attendance Report"
        
        # Create the UI
        self.__create_widgets()
        
    def __create_widgets(self):
        # Card-like container with white background - reduced padding
        self.card_frame = ctk.CTkFrame(self, corner_radius=20, fg_color="white")
        self.card_frame.pack(padx=15, pady=15, fill="both", expand=True)
        
        # Get the assets path using absolute path
        current_dir = os.path.dirname(os.path.abspath(__file__))
        assets_dir = os.path.join(current_dir, "assets")
        
        # MSP Logo - Handle large images by pre-processing with PIL
        logo_path = os.path.join(assets_dir, "msp_logo.png")
        
        if os.path.exists(logo_path):
            try:
                # Load with PIL first and resize to avoid memory issues
                from PIL import Image
                pil_image = Image.open(logo_path)
                
                # Make logo readable but not too large to push content down
                target_size = (270, 270)  # Reduced
                pil_image = pil_image.resize(target_size, Image.Resampling.LANCZOS)
                
                # Now create CustomTkinter image
                self.logo_img = ctk.CTkImage(light_image=pil_image, size=target_size)
                self.logo_label = ctk.CTkLabel(self.card_frame, image=self.logo_img, text="")
                self.logo_label.pack(pady=(0))  # Reduced padding
                
            except Exception as e:
                self.__create_logo_fallback()
        else:
            self.__create_logo_fallback()
        
        # Remove the separate title labels since the logo contains the text
        # (The original design has the text in the logo itself)
        
        # Instruction
        self.instruction_label = ctk.CTkLabel(self.card_frame, text="Select your Attendance Sheet:", 
                                            font=("Arial", 14), text_color="black")
        self.instruction_label.pack(pady=(0))  # Reduced padding
        
        # Upload Button - Better styling to match the original
        upload_path = os.path.join(assets_dir, "upload_icon.png")
        if os.path.exists(upload_path):
            try:
                from PIL import Image
                pil_image = Image.open(upload_path)
                # Get original dimensions to maintain aspect ratio
                original_width, original_height = pil_image.size
                
                # Since it's a square icon, keep it square but sized appropriately
                target_size = 50  # Square size that fits well in the button
                pil_image = pil_image.resize((target_size, target_size), Image.Resampling.LANCZOS)
                self.upload_img = ctk.CTkImage(light_image=pil_image, size=(target_size, target_size))
                self.upload_button = ctk.CTkButton(self.card_frame, image=self.upload_img, text="", 
                                                 width=120, height=60,  # Adjusted button size
                                                 fg_color="white", hover_color="#f5f5f5",
                                                 border_width=1, border_color="#ddd",
                                                 command=self.__upload_file)
            except Exception:
                self.__create_upload_fallback()
        else:
            self.__create_upload_fallback()
        self.upload_button.pack(pady=15)  # Reduced padding
        
        # Export Section
        self.export_label = ctk.CTkLabel(self.card_frame, text="Export as:", 
                                       font=("Arial", 14), text_color="black")
        self.export_label.pack(pady=(15, 8))  # Reduced padding
        
        # Export buttons frame
        self.export_frame = ctk.CTkFrame(self.card_frame, fg_color="transparent")
        self.export_frame.pack()
        
        # Word button - Icon only, no text
        word_path = os.path.join(assets_dir, "word_icon.png")
        if os.path.exists(word_path):
            try:
                from PIL import Image
                pil_image = Image.open(word_path)
                pil_image = pil_image.resize((60, 60), Image.Resampling.LANCZOS)
                self.word_img = ctk.CTkImage(light_image=pil_image, size=(60, 60))
                self.word_button = ctk.CTkButton(self.export_frame, image=self.word_img, text="",
                                               width=100, height=80,
                                               fg_color="white", hover_color="#f0f0f0",
                                               border_width=2, border_color="#e0e0e0",
                                               command=lambda: self.__export_file("word"))
            except Exception:
                self.__create_word_fallback()
        else:
            self.__create_word_fallback()
        self.word_button.grid(row=0, column=0, padx=10)
        
        # PDF button - Icon only, no text
        pdf_path = os.path.join(assets_dir, "pdf_icon.png")
        if os.path.exists(pdf_path):
            try:
                from PIL import Image
                pil_image = Image.open(pdf_path)
                pil_image = pil_image.resize((60, 60), Image.Resampling.LANCZOS)
                self.pdf_img = ctk.CTkImage(light_image=pil_image, size=(60, 60))
                self.pdf_button = ctk.CTkButton(self.export_frame, image=self.pdf_img, text="",
                                              width=100, height=80,
                                              fg_color="white", hover_color="#f0f0f0", 
                                              border_width=2, border_color="#e0e0e0",
                                              command=lambda: self.__export_file("pdf"))
            except Exception:
                self.__create_pdf_fallback()
        else:
            self.__create_pdf_fallback()
        self.pdf_button.grid(row=0, column=1, padx=10)
        
        # Status - with multi-line support and better formatting
        self.status_label = ctk.CTkLabel(self.card_frame, 
                                       text="Status:\nReady", 
                                       text_color="green", 
                                       font=("Arial", 12),
                                       justify="center")
        self.status_label.pack(pady=15)  # Reduced padding
        
    def __create_logo_fallback(self):
        """Create fallback logo when image fails to load."""
        self.logo_frame = ctk.CTkFrame(self.card_frame, width=140, height=140, corner_radius=70)
        self.logo_frame.pack(pady=(15, 8))
        self.logo_label = ctk.CTkLabel(self.logo_frame, text="MSP\nTech Club", font=("Arial", 16, "bold"))
        self.logo_label.pack(expand=True)
        
    def __create_upload_fallback(self):
        """Create fallback upload button when icon fails to load."""
        self.upload_button = ctk.CTkButton(self.card_frame, text="📤 Upload", 
                                         width=150, height=50,
                                         font=("Arial", 14, "bold"),
                                         fg_color="transparent", hover_color="#f0f0f0",
                                         text_color="black", border_width=0,
                                         command=self.__upload_file)
        
    def __create_word_fallback(self):
        """Create fallback Word button when icon fails to load."""
        self.word_button = ctk.CTkButton(self.export_frame, text="DOCX", 
                                       width=100, height=80,
                                       font=("Arial", 14, "bold"),
                                       fg_color="white", hover_color="#f0f0f0",
                                       text_color="#2196F3",
                                       border_width=2, border_color="#e0e0e0",
                                       command=lambda: self.__export_file("word"))
        
    def __create_pdf_fallback(self):
        """Create fallback PDF button when icon fails to load."""
        self.pdf_button = ctk.CTkButton(self.export_frame, text="PDF", 
                                      width=100, height=80,
                                      font=("Arial", 14, "bold"),
                                      fg_color="white", hover_color="#f0f0f0",
                                      text_color="#f44336",
                                      border_width=2, border_color="#e0e0e0",
                                      command=lambda: self.__export_file("pdf"))
        
    def __upload_file(self):
        """
        Handle CSV file selection dialog.
        
        Returns:
            None
        """
        file_path = filedialog.askopenfilename(
            title="Select CSV File",
            filetypes=[("CSV Files", "*.csv"), ("All files", "*.*")]
        )
        if file_path:
            self.csv_file_path = file_path
            filename = file_path.split('/')[-1].split('\\')[-1]  # Handle both / and \ paths
            # Truncate long filenames
            if len(filename) > 20:
                display_name = filename[:17] + "..."
            else:
                display_name = filename
            self.status_label.configure(text=f"Selected File:\n{display_name}", text_color="#007BFF")
            
    def __export_file(self, file_type):
        """
        Process CSV file and export to specified format.
        
        Args:
            file_type (str): Export format ('word' or 'pdf')
            
        Returns:
            None
        """
        if not self.csv_file_path:
            messagebox.showerror("Error", "Please select a CSV file first.")
            return
            
        # Update status
        self.status_label.configure(text=f"Status:\nExporting to {file_type.upper()}...", text_color="orange")
        self.update()  # Force GUI update
        
        try:
            # Process file
            processor = Processor(self.csv_file_path)
            valid_rows, invalid_rows = processor.process()
            
            # Create exporter
            exporter = Exporter(valid_rows, invalid_rows, self.report_title)
            
            # Export based on type
            if file_type == "word":
                filename = exporter.export_word()
            elif file_type == "pdf":
                filename = exporter.export_pdf()
                
            # Update status to success - shorter text
            self.status_label.configure(text=f"Export Complete!\n{file_type.upper()} file created", 
                                      text_color="green")
            
            messagebox.showinfo("Success", f"Export completed successfully!\nFile: {filename}")
            
        except FileNotFoundError as e:
            error_msg = f"File not found: {e}"
            self.status_label.configure(text="Error:\nFile Not Found", text_color="#DC3545")
            messagebox.showerror("File Error", error_msg)
            
        except ValueError as e:
            error_msg = f"Data validation error: {e}"
            self.status_label.configure(text="Error:\nData Validation Failed", text_color="#DC3545")
            messagebox.showerror("Data Error", error_msg)
            
        except Exception as e:
            error_msg = f"Unexpected error: {e}"
            self.status_label.configure(text="Error:\nExport Failed", text_color="#DC3545")
            messagebox.showerror("Error", error_msg)


def launch_gui():
    """Launch the MSP Attendance Exporter GUI application."""
    # Create and run the GUI
    app = AttendanceExporterApp()
    app.mainloop()


if __name__ == "__main__":
    # Allow running the GUI directly for testing
    launch_gui()
