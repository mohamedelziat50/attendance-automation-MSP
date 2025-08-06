"""
GUI Module for Attendance Automation Tool

This module contains the main GUI interface for the attendance tool.
It provides a user-friendly graphical interface to process CSV files
"""

import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image
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
        self.geometry("400x650")  # Keep current height but optimize spacing
        self.resizable(False, False)

        # Variables to store file path and title
        self.csv_file_path = None
        self.default_title = "Attendance Report"
        self.report_title = self.default_title

        # Create the UI
        self.__create_widgets()

    def __create_widgets(self):
        # Card-like container with white background - optimized padding
        self.card_frame = ctk.CTkFrame(self, corner_radius=20, fg_color="white")
        self.card_frame.pack(
            padx=10, pady=10, fill="both", expand=True
        )  # Reduced padding

        # Get the assets path using absolute path
        current_dir = os.path.dirname(os.path.abspath(__file__))
        assets_dir = os.path.join(current_dir, "assets")

        # MSP Logo - Handle large images by pre-processing with PIL
        logo_path = os.path.join(assets_dir, "msp_logo.png")

        if os.path.exists(logo_path):
            try:
                # Load with PIL first and resize to avoid memory issues
                pil_image = Image.open(logo_path)

                # Make logo smaller to save space
                target_size = (240, 240)  # Reduced from 270x270
                pil_image = pil_image.resize(target_size, Image.Resampling.LANCZOS)

                # Now create CustomTkinter image
                self.logo_img = ctk.CTkImage(light_image=pil_image, size=target_size)
                self.logo_label = ctk.CTkLabel(
                    self.card_frame, image=self.logo_img, text=""
                )
                self.logo_label.pack(pady=(0, 5))  # Small bottom padding

            except Exception as e:
                self.__create_logo_fallback()
        else:
            self.__create_logo_fallback()

        # Remove the separate title labels since the logo contains the text
        # (The original design has the text in the logo itself)

        # Report Title Input - Label and Entry on same line
        self.title_frame = ctk.CTkFrame(self.card_frame, fg_color="transparent")
        self.title_frame.pack(pady=(0, 8))  # Reduced padding

        self.title_label = ctk.CTkLabel(
            self.title_frame, text="Title:", font=("Arial", 14), text_color="black"
        )
        self.title_label.pack(side="left", padx=(0, 10))

        self.title_entry = ctk.CTkEntry(
            self.title_frame,
            placeholder_text="Enter report title...",
            width=150,
            height=32,  # Slightly smaller height
            font=("Arial", 12),
            fg_color="white",
            border_color="#e0e0e0",
            border_width=1,
            text_color="black",
        )
        self.title_entry.insert(0, self.default_title)
        self.title_entry.pack(side="left")

        # Instruction
        self.instruction_label = ctk.CTkLabel(
            self.card_frame,
            text="Select your Attendance Sheet:",
            font=("Arial", 14),
            text_color="black",
        )
        self.instruction_label.pack(pady=(8, 5))  # Reduced padding

        # Upload Button - Better styling to match the original
        upload_path = os.path.join(assets_dir, "upload_icon.png")
        if os.path.exists(upload_path):
            try:
                pil_image = Image.open(upload_path)

                # Resize image to smaller size
                image_size = (195, 50)
                button_size = (195, 50)

                pil_image = pil_image.resize(image_size, Image.Resampling.LANCZOS)
                self.upload_img = ctk.CTkImage(light_image=pil_image, size=image_size)
                self.upload_button = ctk.CTkButton(
                    self.card_frame,
                    image=self.upload_img,
                    text="",
                    width=button_size[0],
                    height=button_size[1],
                    fg_color="white",
                    hover_color="#f5f5f5",
                    # border_width=1, border_color="#c0c0c0",  # Thicker border, more visible color
                    command=self.__upload_file,
                )
            except Exception:
                self.__create_upload_fallback()
        else:
            self.__create_upload_fallback()
        self.upload_button.pack(pady=10)  # Reduced padding

        # Export Section
        self.export_label = ctk.CTkLabel(
            self.card_frame, text="Export as:", font=("Arial", 14), text_color="black"
        )
        self.export_label.pack(pady=(10, 5))  # Reduced padding

        # Export buttons frame
        self.export_frame = ctk.CTkFrame(self.card_frame, fg_color="transparent")
        self.export_frame.pack()

        # Word button - Icon with text label
        word_path = os.path.join(assets_dir, "word_icon.png")
        if os.path.exists(word_path):
            try:
                pil_image = Image.open(word_path)
                pil_image = pil_image.resize(
                    (45, 45), Image.Resampling.LANCZOS
                )  # Slightly smaller icon
                self.word_img = ctk.CTkImage(light_image=pil_image, size=(45, 45))
                self.word_button = ctk.CTkButton(
                    self.export_frame,
                    image=self.word_img,
                    text="Word",
                    width=90,
                    height=80,  # Smaller button
                    fg_color="white",
                    hover_color="#f0f0f0",
                    border_width=1,
                    border_color="#e0e0e0",
                    font=("Arial", 11, "bold"),  # Smaller font
                    text_color="#2196F3",
                    compound="top",  # Icon on top, text below
                    command=lambda: self.__export_file("word"),
                )
            except Exception:
                self.__create_word_fallback()
        else:
            self.__create_word_fallback()
        self.word_button.grid(row=0, column=0, padx=10)

        # PDF button - Icon with text label
        pdf_path = os.path.join(assets_dir, "pdf_icon.png")
        if os.path.exists(pdf_path):
            try:
                pil_image = Image.open(pdf_path)
                pil_image = pil_image.resize(
                    (45, 45), Image.Resampling.LANCZOS
                )  # Slightly smaller icon
                self.pdf_img = ctk.CTkImage(light_image=pil_image, size=(45, 45))
                self.pdf_button = ctk.CTkButton(
                    self.export_frame,
                    image=self.pdf_img,
                    text="PDF",
                    width=90,
                    height=80,  # Smaller button
                    fg_color="white",
                    hover_color="#f0f0f0",
                    border_width=1,
                    border_color="#e0e0e0",
                    font=("Arial", 11, "bold"),  # Smaller font
                    text_color="#f44336",
                    compound="top",  # Icon on top, text below
                    command=lambda: self.__export_file("pdf"),
                )
            except Exception:
                self.__create_pdf_fallback()
        else:
            self.__create_pdf_fallback()
        self.pdf_button.grid(row=0, column=1, padx=10)

        # Status - with multi-line support and better formatting
        self.status_label = ctk.CTkLabel(
            self.card_frame,
            text="Status:\nReady",
            text_color="green",
            font=("Arial", 13),  # Smaller font
            justify="center",
        )
        self.status_label.pack(pady=15)  # Reduced padding

    def __create_logo_fallback(self):
        """Create fallback logo when image fails to load."""
        self.logo_frame = ctk.CTkFrame(
            self.card_frame, width=140, height=140, corner_radius=70
        )
        self.logo_frame.pack(pady=(15, 8))
        self.logo_label = ctk.CTkLabel(
            self.logo_frame, text="MSP\nTech Club", font=("Arial", 16, "bold")
        )
        self.logo_label.pack(expand=True)

    def __create_upload_fallback(self):
        """Create fallback upload button when icon fails to load."""
        self.upload_button = ctk.CTkButton(
            self.card_frame,
            text="📤 Upload",
            width=140,
            height=40,  # Match the smaller size
            font=("Arial", 12, "bold"),  # Smaller font
            fg_color="transparent",
            hover_color="#f0f0f0",
            text_color="black",
            border_width=0,
            command=self.__upload_file,
        )

    def __create_word_fallback(self):
        """Create fallback Word button when icon fails to load."""
        self.word_button = ctk.CTkButton(
            self.export_frame,
            text="Word",
            width=90,
            height=80,  # Match the smaller size
            font=("Arial", 12, "bold"),  # Smaller font
            fg_color="white",
            hover_color="#f0f0f0",
            text_color="#2196F3",
            border_width=1,
            border_color="#e0e0e0",
            command=lambda: self.__export_file("word"),
        )

    def __create_pdf_fallback(self):
        """Create fallback PDF button when icon fails to load."""
        self.pdf_button = ctk.CTkButton(
            self.export_frame,
            text="PDF",
            width=90,
            height=80,  # Match the smaller size
            font=("Arial", 12, "bold"),  # Smaller font
            fg_color="white",
            hover_color="#f0f0f0",
            text_color="#f44336",
            border_width=1,
            border_color="#e0e0e0",
            command=lambda: self.__export_file("pdf"),
        )

    def __upload_file(self):
        """
        Handle CSV file selection dialog.

        Returns:
            None
        """
        file_path = filedialog.askopenfilename(
            title="Select CSV File",
            filetypes=[("CSV Files", "*.csv"), ("All files", "*.*")],
        )
        if file_path:
            self.csv_file_path = file_path
            filename = file_path.split("/")[-1].split("\\")[
                -1
            ]  # Handle both / and \ paths
            # Truncate long filenames
            if len(filename) > 55:
                display_name = filename[:17] + "..."
            else:
                display_name = filename
            self.status_label.configure(
                text=f"Selected File:\n{display_name}", text_color="#007BFF"
            )

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

        # Get the report title from user input, with fallback to default
        user_title = self.title_entry.get().strip()
        self.report_title = user_title if user_title else self.default_title

        # Update status
        self.status_label.configure(
            text=f"Status:\nExporting to {file_type.upper()}...", text_color="orange"
        )
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
            self.status_label.configure(
                text=f"Export Complete!\n{file_type.upper()} file created",
                text_color="green",
            )

            messagebox.showinfo(
                "Success", f"Export completed successfully!\nFile: {filename}"
            )

        except FileNotFoundError as e:
            error_msg = f"File not found: {e}"
            self.status_label.configure(
                text="Error:\nFile Not Found", text_color="#DC3545"
            )
            messagebox.showerror("File Error", error_msg)

        except ValueError as e:
            error_msg = f"Data validation error: {e}"
            self.status_label.configure(
                text="Error:\nData Validation Failed", text_color="#DC3545"
            )
            messagebox.showerror("Data Error", error_msg)

        except Exception as e:
            error_msg = f"Unexpected error: {e}"
            self.status_label.configure(
                text="Error:\nExport Failed", text_color="#DC3545"
            )
            messagebox.showerror("Error", error_msg)


def launch_gui():
    """Launch the MSP Attendance Exporter GUI application."""
    # Create and run the GUI
    app = AttendanceExporterApp()
    app.mainloop()


if __name__ == "__main__":
    # Allow running the GUI directly for testing
    launch_gui()
