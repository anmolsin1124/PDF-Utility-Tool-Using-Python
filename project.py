import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from pdf2image import convert_from_path
from PIL import Image
from PyPDF2 import PdfMerger, PdfReader, PdfWriter


class PdfUtilityApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("PDF Utility Tool")
        self.root.geometry("720x520")
        self.root.configure(bg="#f5f7fa")
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        style = ttk.Style()
        if "clam" in style.theme_names():
            style.theme_use("clam")
        style.configure("TFrame", background="#f5f7fa")
        style.configure(
            "Header.TLabel",
            background="#f5f7fa",
            font=("Segoe UI", 20, "bold"),
            foreground="#1f2937",
        )
        style.configure(
            "SubHeader.TLabel",
            background="#f5f7fa",
            font=("Segoe UI", 10),
            foreground="#4b5563",
        )
        style.configure("TLabelFrame", background="#f5f7fa")
        style.configure("TLabelFrame.Label", background="#f5f7fa")
        style.configure("TButton", font=("Segoe UI", 10), padding=8)
        style.configure(
            "Accent.TButton",
            font=("Segoe UI", 10, "bold"),
            foreground="#ffffff",
            background="#2563eb",
        )
        style.map(
            "Accent.TButton",
            background=[("active", "#1d4ed8"), ("disabled", "#93c5fd")],
        )

        self.rotation_var = tk.StringVar(value="90")
        self.status_var = tk.StringVar(value="Ready to manage your PDFs.")

        main_frame = ttk.Frame(self.root, padding=20)
        main_frame.grid(row=0, column=0, sticky="nsew")
        main_frame.columnconfigure(0, weight=1)

        header = ttk.Label(main_frame, text="PDF Utility Tool", style="Header.TLabel")
        header.grid(row=0, column=0, sticky="w")

        subtitle = ttk.Label(
            main_frame,
            text="Convert, merge, split, rotate, and extract PDF content with ease.",
            style="SubHeader.TLabel",
        )
        subtitle.grid(row=1, column=0, sticky="w", pady=(4, 16))

        tools_frame = ttk.LabelFrame(main_frame, text="Document Actions", padding=16)
        tools_frame.grid(row=2, column=0, sticky="ew")
        tools_frame.columnconfigure((0, 1), weight=1)

        ttk.Button(
            tools_frame,
            text="PDF to Images",
            command=self.pdf_to_images,
        ).grid(row=0, column=0, sticky="ew", padx=6, pady=6)
        ttk.Button(
            tools_frame,
            text="Images to PDF",
            command=self.images_to_pdf,
        ).grid(row=0, column=1, sticky="ew", padx=6, pady=6)
        ttk.Button(
            tools_frame,
            text="Merge PDFs",
            command=self.merge_pdfs,
        ).grid(row=1, column=0, sticky="ew", padx=6, pady=6)
        ttk.Button(
            tools_frame,
            text="Split PDF",
            command=self.split_pdf,
        ).grid(row=1, column=1, sticky="ew", padx=6, pady=6)
        ttk.Button(
            tools_frame,
            text="Rotate PDF",
            command=self.rotate_pdf,
        ).grid(row=2, column=0, sticky="ew", padx=6, pady=6)
        ttk.Button(
            tools_frame,
            text="Extract Text",
            command=self.extract_text,
        ).grid(row=2, column=1, sticky="ew", padx=6, pady=6)

        ttk.Button(
            tools_frame,
            text="Exit",
            style="Accent.TButton",
            command=self.root.destroy,
        ).grid(row=3, column=0, columnspan=2, sticky="ew", padx=6, pady=(12, 0))

        options_frame = ttk.LabelFrame(main_frame, text="Options", padding=12)
        options_frame.grid(row=3, column=0, sticky="ew", pady=16)
        options_frame.columnconfigure(1, weight=1)

        ttk.Label(options_frame, text="Rotation (degrees):").grid(
            row=0, column=0, sticky="w"
        )
        rotation_menu = ttk.Combobox(
            options_frame,
            textvariable=self.rotation_var,
            values=("90", "180", "270"),
            state="readonly",
            width=10,
        )
        rotation_menu.grid(row=0, column=1, sticky="w", padx=(8, 0))

        status_frame = ttk.Frame(main_frame)
        status_frame.grid(row=4, column=0, sticky="ew")
        status_frame.columnconfigure(0, weight=1)
        ttk.Separator(status_frame, orient="horizontal").grid(
            row=0, column=0, sticky="ew", pady=(0, 10)
        )
        status_label = ttk.Label(
            status_frame,
            textvariable=self.status_var,
            style="SubHeader.TLabel",
        )
        status_label.grid(row=1, column=0, sticky="w")

    def _set_status(self, message: str) -> None:
        self.status_var.set(message)
        self.root.update_idletasks()

    def _default_output_name(self, input_path: str, suffix: str) -> str:
        base_name = os.path.splitext(os.path.basename(input_path))[0]
        return f"{base_name}_{suffix}.pdf"

    def pdf_to_images(self) -> None:
        pdf_path = filedialog.askopenfilename(
            title="Select a PDF file",
            filetypes=[("PDF files", "*.pdf")],
        )
        if not pdf_path:
            self._set_status("PDF to Images cancelled.")
            return

        output_dir = filedialog.askdirectory(title="Select output folder")
        if not output_dir:
            self._set_status("PDF to Images cancelled.")
            return

        self._set_status("Converting PDF pages to images...")
        try:
            images = convert_from_path(pdf_path)
            base_name = os.path.splitext(os.path.basename(pdf_path))[0]
            for index, img in enumerate(images, start=1):
                filename = f"{base_name}_page_{index}.jpg"
                img.save(os.path.join(output_dir, filename), "JPEG")
        except Exception as exc:  # pragma: no cover - GUI messaging
            self._set_status("PDF to Images failed.")
            messagebox.showerror("Conversion failed", f"Unable to convert PDF.\n{exc}")
            return

        self._set_status("PDF converted to images successfully.")
        messagebox.showinfo("Success", "PDF pages were saved as JPG images.")

    def images_to_pdf(self) -> None:
        image_paths = filedialog.askopenfilenames(
            title="Select image files",
            filetypes=[
                ("Image files", "*.png *.jpg *.jpeg *.bmp *.tiff"),
                ("All files", "*.*"),
            ],
        )
        if not image_paths:
            self._set_status("Images to PDF cancelled.")
            return

        output_path = filedialog.asksaveasfilename(
            title="Save PDF as",
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")],
            initialfile="images.pdf",
        )
        if not output_path:
            self._set_status("Images to PDF cancelled.")
            return

        self._set_status("Converting images to PDF...")
        try:
            images = []
            for image_path in image_paths:
                with Image.open(image_path) as img:
                    images.append(img.convert("RGB").copy())
            first_image, remaining_images = images[0], images[1:]
            first_image.save(output_path, save_all=True, append_images=remaining_images)
        except Exception as exc:  # pragma: no cover - GUI messaging
            self._set_status("Images to PDF failed.")
            messagebox.showerror("Conversion failed", f"Unable to create PDF.\n{exc}")
            return

        self._set_status("Images converted to PDF successfully.")
        messagebox.showinfo("Success", "The images were converted into a PDF.")

    def merge_pdfs(self) -> None:
        pdf_paths = filedialog.askopenfilenames(
            title="Select PDF files to merge",
            filetypes=[("PDF files", "*.pdf")],
        )
        if not pdf_paths:
            self._set_status("Merge PDFs cancelled.")
            return

        output_path = filedialog.asksaveasfilename(
            title="Save merged PDF as",
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")],
            initialfile="merged.pdf",
        )
        if not output_path:
            self._set_status("Merge PDFs cancelled.")
            return

        self._set_status("Merging PDF files...")
        merger = PdfMerger()
        try:
            for pdf_path in pdf_paths:
                merger.append(pdf_path)
            merger.write(output_path)
        except Exception as exc:  # pragma: no cover - GUI messaging
            self._set_status("Merge PDFs failed.")
            messagebox.showerror("Merge failed", f"Unable to merge PDFs.\n{exc}")
            return
        finally:
            merger.close()

        self._set_status("PDF files merged successfully.")
        messagebox.showinfo("Success", "PDF files were merged into one document.")

    def split_pdf(self) -> None:
        pdf_path = filedialog.askopenfilename(
            title="Select a PDF file to split",
            filetypes=[("PDF files", "*.pdf")],
        )
        if not pdf_path:
            self._set_status("Split PDF cancelled.")
            return

        output_dir = filedialog.askdirectory(title="Select output folder")
        if not output_dir:
            self._set_status("Split PDF cancelled.")
            return

        self._set_status("Splitting PDF into individual pages...")
        try:
            reader = PdfReader(pdf_path)
            base_name = os.path.splitext(os.path.basename(pdf_path))[0]
            for index, page in enumerate(reader.pages, start=1):
                writer = PdfWriter()
                writer.add_page(page)
                output_file = os.path.join(output_dir, f"{base_name}_page_{index}.pdf")
                with open(output_file, "wb") as output_stream:
                    writer.write(output_stream)
        except Exception as exc:  # pragma: no cover - GUI messaging
            self._set_status("Split PDF failed.")
            messagebox.showerror("Split failed", f"Unable to split the PDF.\n{exc}")
            return

        self._set_status("PDF split into individual pages.")
        messagebox.showinfo("Success", "Each page was saved as a separate PDF.")

    def rotate_pdf(self) -> None:
        pdf_path = filedialog.askopenfilename(
            title="Select a PDF file to rotate",
            filetypes=[("PDF files", "*.pdf")],
        )
        if not pdf_path:
            self._set_status("Rotate PDF cancelled.")
            return

        output_path = filedialog.asksaveasfilename(
            title="Save rotated PDF as",
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")],
            initialfile=self._default_output_name(pdf_path, "rotated"),
        )
        if not output_path:
            self._set_status("Rotate PDF cancelled.")
            return

        try:
            rotation = int(self.rotation_var.get())
        except ValueError:
            rotation = 90

        self._set_status("Rotating PDF pages...")
        try:
            reader = PdfReader(pdf_path)
            writer = PdfWriter()
            for page in reader.pages:
                rotated_page = self._rotate_page(page, rotation)
                writer.add_page(rotated_page)
            with open(output_path, "wb") as output_stream:
                writer.write(output_stream)
        except Exception as exc:  # pragma: no cover - GUI messaging
            self._set_status("Rotate PDF failed.")
            messagebox.showerror("Rotation failed", f"Unable to rotate PDF.\n{exc}")
            return

        self._set_status("PDF rotated successfully.")
        messagebox.showinfo("Success", "PDF pages were rotated.")

    @staticmethod
    def _rotate_page(page, rotation: int):
        """Support multiple PyPDF2 rotation APIs across versions."""
        if hasattr(page, "rotate"):
            return page.rotate(rotation)
        if hasattr(page, "rotate_clockwise"):
            return page.rotate_clockwise(rotation)
        return page.rotateClockwise(rotation)

    def extract_text(self) -> None:
        pdf_path = filedialog.askopenfilename(
            title="Select a PDF file to extract text",
            filetypes=[("PDF files", "*.pdf")],
        )
        if not pdf_path:
            self._set_status("Extract Text cancelled.")
            return

        output_path = filedialog.asksaveasfilename(
            title="Save extracted text as",
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt")],
            initialfile="extracted_text.txt",
        )
        if not output_path:
            self._set_status("Extract Text cancelled.")
            return

        self._set_status("Extracting text from PDF...")
        try:
            reader = PdfReader(pdf_path)
            extracted_text = []
            for page in reader.pages:
                extracted_text.append(page.extract_text() or "")
            with open(output_path, "w", encoding="utf-8") as output_stream:
                output_stream.write("\n\n".join(extracted_text).strip())
        except Exception as exc:  # pragma: no cover - GUI messaging
            self._set_status("Extract Text failed.")
            messagebox.showerror("Extraction failed", f"Unable to extract text.\n{exc}")
            return

        self._set_status("Text extracted successfully.")
        messagebox.showinfo("Success", "Text was extracted into a .txt file.")


if __name__ == "__main__":
    root = tk.Tk()
    app = PdfUtilityApp(root)
    root.mainloop()
