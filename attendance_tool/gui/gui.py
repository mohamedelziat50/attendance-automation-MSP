import os, ctypes, customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image

# Import the core functionality from the parent package
from ..processor import Processor
from ..exporter import Exporter

# Configure CustomTkinter
ctk.set_appearance_mode("light")  # For Light/Gray Background Behind The Root


class AttendanceExporterApp(ctk.CTk):
    """
    GUI application for processing CSV attendance files and exporting to Word/PDF.
    Inherits CustomTkinter's functionality.

    Attributes:
        csv_file_path (str): Path to the currently selected CSV file
        report_title (str): Current title for the report being exported

        # UI Container Elements
        card_frame (ctk.CTkFrame): Main white card container for all UI elements

        # Logo Elements
        logo_img (ctk.CTkImage): MSP logo image (created only when image loads successfully)
        logo_label (ctk.CTkLabel): Label displaying the logo image or text fallback
        logo_frame (ctk.CTkFrame): Fallback frame (created only when logo image fails to load)

        # Title Input Elements
        title_frame (ctk.CTkFrame): Container frame for title input section
        title_label (ctk.CTkLabel): "Title:" label
        title_entry (ctk.CTkEntry): Text input for custom report title

        # Instruction Elements
        instruction_label (ctk.CTkLabel): "Select your Attendance Sheet:" instruction

        # Upload Elements
        upload_img (ctk.CTkImage): Upload button icon (created only when image loads successfully)
        upload_button (ctk.CTkButton): File upload button

        # Export Elements
        export_label (ctk.CTkLabel): "Export as:" label
        export_frame (ctk.CTkFrame): Container frame for export buttons
        word_img (ctk.CTkImage): Word button icon (created only when image loads successfully)
        word_button (ctk.CTkButton): Word export button
        pdf_img (ctk.CTkImage): PDF button icon (created only when image loads successfully)
        pdf_button (ctk.CTkButton): PDF export button

        # Status Elements
        status_label (ctk.CTkLabel): Status display showing current operation state
    """

    # Window dimensions constants
    WINDOW_WIDTH = 400
    WINDOW_HEIGHT = 650

    def __init__(self):
        # Call the parent constructor
        super().__init__()

        # Window configuration
        self.title("MSP Attendance Exporter")  # Window Title
        self.geometry(f"{self.WINDOW_WIDTH}x{self.WINDOW_HEIGHT}")  # Use constants
        self.resizable(False, False)  # Disable resizing

        # Center the window on the screen
        self.__center_window()

        # Set up the application icon (Windows taskbar and window icon)
        self.__setup_app_icon()

        # Variables to store file path and title
        self.csv_file_path = None
        self.report_title = ""

        # Create the UI
        self.__create_widgets()

    def __center_window(self):
        """Center the window on the screen."""
        # Update the window to ensure geometry is calculated
        self.update_idletasks()

        # Get screen dimensions
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Calculate center position
        center_x = int((screen_width - self.WINDOW_WIDTH) / 2)
        center_y = int((screen_height - self.WINDOW_HEIGHT) / 2)

        # Set the window position
        self.geometry(f"{self.WINDOW_WIDTH}x{self.WINDOW_HEIGHT}+{center_x}+{center_y}")

    def __setup_app_icon(self):
        """Set up the application icon for Windows taskbar and window."""
        try:
            # Set the app user model ID for proper taskbar icon to work
            myappid = "msp.attendance.exporter.version"

            # Use Windows Shell32 API to properly identify your application to the Windows taskbar,
            # which should make the custom icon appear correctly in the taskbar.
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

            # Set window icon (favicon/taskbar icon)
            icon_path = os.path.join(
                os.path.dirname(os.path.abspath(__file__)), "assets", "app_icon.ico"
            )
            self.iconbitmap(icon_path)
        except Exception as e:
            print(f"Error setting application icon: {e}")

    def __create_widgets(self):
        """Create and initialize all UI components."""

        # Card-like (Root-like but is a child of the app itself) container with white background - optimized padding
        self.card_frame = ctk.CTkFrame(self, corner_radius=20, fg_color="white")
        self.card_frame.pack(
            padx=10, pady=10, fill="both", expand=True
        )  # Reduced padding

        # Get the assets path using absolute path
        current_dir = os.path.dirname(os.path.abspath(__file__))
        assets_dir = os.path.join(current_dir, "assets")

        # Create the MSP logo
        self.__create_logo(assets_dir)

        # Create the title input section
        self.__create_title_input()

        # Create the instruction label
        self.__create_instruction_label()

        # Create the upload button
        self.__create_upload_button(assets_dir)

        # Create export section
        self.__create_export_section(assets_dir)

        # Create status label
        self.__create_status_label()

    def __create_logo(self, assets_dir):
        """Create MSP logo with fallback handling."""
        logo_path = os.path.join(assets_dir, "msp_logo.png")

        if os.path.exists(logo_path):
            try:
                # Load with PIL first and resize to avoid memory issues
                pil_image = Image.open(logo_path)

                # Make logo smaller to save space
                target_size = (240, 240)
                pil_image = pil_image.resize(
                    target_size, Image.Resampling.LANCZOS
                )  # LANCZOS for high-quality

                # Now create CustomTkinter image
                self.logo_img = ctk.CTkImage(light_image=pil_image, size=target_size)
                self.logo_label = ctk.CTkLabel(
                    self.card_frame, image=self.logo_img, text=""
                )
                self.logo_label.pack(pady=(10, 20))  # Small bottom padding

            except Exception as e:
                self.__create_logo_fallback()
        else:
            self.__create_logo_fallback()

    def __create_title_input(self):
        """Create title input section."""
        # Report Title Container: Label and Input (e.g CTk.Entry) on same line
        self.title_frame = ctk.CTkFrame(self.card_frame, fg_color="transparent")
        self.title_frame.pack(pady=(0, 8))  # Reduced padding

        # Title Label
        self.title_label = ctk.CTkLabel(
            self.title_frame, text="Title:", font=("Arial", 14), text_color="black"
        )
        self.title_label.pack(
            side="left", padx=(0, 10)
        )  # Align label to left with padding

        # Title Entry/Input
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
        self.title_entry.pack(side="left")

    def __create_instruction_label(self):
        """Create file selection instruction label."""
        self.instruction_label = ctk.CTkLabel(
            self.card_frame,
            text="Select your Attendance Sheet:",
            font=("Arial", 14),
            text_color="black",
        )
        self.instruction_label.pack(pady=(8, 0))  # Reduced padding

    def __create_upload_button(self, assets_dir):
        """Create the upload button with icon and fallback handling."""
        upload_path = os.path.join(assets_dir, "upload_icon.png")

        if os.path.exists(upload_path):
            try:
                pil_image = Image.open(upload_path)

                # Resize image to smaller size
                image_size = (195, 50)
                button_size = (195, 50)

                pil_image = pil_image.resize(
                    image_size, Image.Resampling.LANCZOS
                )  # LANCZOS for high-quality
                self.upload_img = ctk.CTkImage(light_image=pil_image, size=image_size)
                self.upload_button = ctk.CTkButton(
                    self.card_frame,
                    image=self.upload_img,
                    text="",
                    width=button_size[0],
                    height=button_size[1],
                    fg_color="white",
                    hover_color="#f5f5f5",
                    command=self.__upload_file,
                )
            except Exception:
                self.__create_upload_fallback()
        else:
            self.__create_upload_fallback()

        self.upload_button.pack(pady=5)  # Reduced padding

    def __get_display_filename(self, file_path):
        """Extract and truncate filename for UI display purposes."""
        filename = file_path.split("/")[-1].split("\\")[-1]  # Handle both / and \ paths
        # Truncate long filenames
        if len(filename) > 55:
            return filename[:17] + "..."
        else:
            return filename

    def __show_selected_file_status(self):
        """Update status label with selected file information."""
        # After export, there will always be a selected file
        display_name = self.__get_display_filename(self.csv_file_path)
        self.status_label.configure(
            text=f"Selected File:\n{display_name}", text_color="#007BFF"
        )

    def __create_export_section(self, assets_dir):
        """Create export section with Label, Word and PDF buttons."""
        # Export Section Label
        self.export_label = ctk.CTkLabel(
            self.card_frame, text="Export as:", font=("Arial", 14), text_color="black"
        )
        self.export_label.pack(pady=(10, 5))  # Reduced padding

        # Export buttons frame
        self.export_frame = ctk.CTkFrame(self.card_frame, fg_color="transparent")
        self.export_frame.pack()

        # Create Word and PDF export buttons
        self.__create_word_button(assets_dir)
        self.__create_pdf_button(assets_dir)

    def __create_status_label(self):
        """Create status display label."""
        self.status_label = ctk.CTkLabel(
            self.card_frame,
            text="Status:\nReady",
            text_color="#5D9827",
            font=("Arial", 13),  # Smaller font
            justify="center",
        )
        self.status_label.pack(pady=20)  # Reduced padding

    def __create_word_button(self, assets_dir):
        """Create Word export button with icon and fallback handling."""
        word_path = os.path.join(assets_dir, "word_icon.png")

        if os.path.exists(word_path):
            try:
                pil_image = Image.open(word_path)
                pil_image = pil_image.resize(
                    (45, 45), Image.Resampling.LANCZOS
                )  # LANCZOS for high-quality
                self.word_img = ctk.CTkImage(light_image=pil_image, size=(45, 45))
                self.word_button = ctk.CTkButton(
                    self.export_frame,
                    image=self.word_img,  # Word Icon image
                    text="Word",  # Text below icon
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

    def __create_pdf_button(self, assets_dir):
        """Create PDF export button with icon and fallback handling."""
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
                    image=self.pdf_img,  # PDF Icon image
                    text="PDF",  # Text below icon
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

    def __create_logo_fallback(self):
        """Create text-based logo fallback."""
        self.logo_frame = ctk.CTkFrame(
            self.card_frame, width=140, height=140, corner_radius=70
        )
        self.logo_frame.pack(pady=(15, 8))
        self.logo_label = ctk.CTkLabel(
            self.logo_frame,
            text="MSP\nTech Club\nMisr International University",
            font=("Arial", 16, "bold"),
        )
        self.logo_label.pack(expand=True)

    def __create_upload_fallback(self):
        """Create text-based upload button fallback."""
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
        """Create text-based Word button fallback."""
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
        """Create text-based PDF button fallback."""
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
        """Handle CSV file selection dialog."""
        #  Only CSV files shown by default (unless user switches to "All files")
        file_path = filedialog.askopenfilename(
            title="Select CSV File",
            filetypes=[("CSV Files", "*.csv"), ("All files", "*.*")],
        )

        # If a file was selected, update the GUI's attribute for file path, and UI status label
        if file_path:
            self.csv_file_path = file_path
            self.__show_selected_file_status()  # Use existing function to update status

    def __export_file(self, file_type):
        """
        Process CSV file and export to specified format.

        Args:
            file_type (str): Export format ('word' or 'pdf')
        """
        if not self.csv_file_path:
            # Pop Up error if no file selected
            self.status_label.configure(
                text="Error:\nNo CSV file selected", text_color="#DC3545"
            )
            return

        # Get the report title from user input, with fallback to default
        user_title = self.title_entry.get()

        # Validate title - block if it's only spaces
        if user_title and user_title.isspace():
            self.status_label.configure(
                text="Error:\nTitle cannot be only spaces", text_color="#DC3545"
            )
            return
        
        # If user provided a valid title, use it; otherwise, keep the current report title empty (Exporter will handle empty titles)
        if user_title and user_title.strip():
            self.report_title = user_title

        # Update status
        self.status_label.configure(
            text=f"Status:\nExporting to {file_type.upper()}...", text_color="orange"
        )
        self.update()  # Force GUI update

        try:
            # Process file
            processor = Processor(self.csv_file_path)
            valid_rows, invalid_rows = processor.process()

            # Create exporter - pass title only if user provided one
            if self.report_title:
                exporter = Exporter(valid_rows, invalid_rows, self.report_title)
            else:
                # Let Exporter use its default title by not passing the title parameter
                exporter = Exporter(valid_rows, invalid_rows)

            # Export based on type
            if file_type == "word":
                filename = exporter.export_word()
            elif file_type == "pdf":
                filename = exporter.export_pdf()

            # Reset status to show selected file (export is complete)
            self.__show_selected_file_status()

            # Show success pop-up with filename
            display_filename = self.__get_display_filename(filename)
            messagebox.showinfo(
                "Export Complete!",
                f"Successfully exported {file_type.upper()} file:\n{display_filename}"
            )

        except FileNotFoundError as e:
            self.status_label.configure(
                text=f"File not found:\n {str(e)}", text_color="#DC3545"
            )

        except ValueError as e:
            self.status_label.configure(
                text=f"Data validation error:\n {str(e)}", text_color="#DC3545"
            )

        except Exception as e:
            self.status_label.configure(
                text=f"Unexpected error:\n {str(e)}", text_color="#DC3545"
            )


def launch_gui():
    """Launch the MSP Attendance Exporter GUI application."""
    # Create and run the GUI
    app = AttendanceExporterApp()
    app.mainloop()


if __name__ == "__main__":
    # Allow running the GUI directly for testing
    launch_gui()
