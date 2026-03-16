"""
PDF Utility Tool - Web Application

A Streamlit-based web application that provides PDF utilities:
1. Convert PDF to Images
2. Convert Images to PDF
3. Merge multiple PDF files

This app preserves the core logic from the original CLI tool (project.py)
and wraps it in a browser-based interface.
"""

import streamlit as st
from pdf2image import convert_from_path
from PIL import Image
from PyPDF2 import PdfMerger
import os
import io
import tempfile
import zipfile


# --- Page Configuration ---
st.set_page_config(page_title="PDF Utility Tool", layout="centered")
st.title("PDF Utility Tool")

# --- Sidebar Menu ---
st.sidebar.header("Choose a Tool")
tool = st.sidebar.radio(
    "Select an operation:",
    ["PDF to Images", "Images to PDF", "Merge PDFs"]
)


def pdf_to_images_tool():
    """Convert a PDF file to individual JPEG images."""
    st.header("1. PDF to Images")
    st.write("Upload a PDF file to convert each page into a JPEG image.")

    uploaded_pdf = st.file_uploader("Upload a PDF file", type=["pdf"], key="pdf_to_img")

    if uploaded_pdf is not None:
        if st.button("Convert to Images"):
            # Save uploaded PDF to a temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                tmp.write(uploaded_pdf.read())
                tmp_path = tmp.name

            try:
                # Core logic: convert PDF pages to images using pdf2image
                images = convert_from_path(tmp_path)

                st.success(f"PDF converted into {len(images)} image(s) successfully!")

                # Create a zip file containing all images for download
                zip_buffer = io.BytesIO()
                with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zf:
                    count = 1
                    for img in images:
                        # Save each page as JPEG (same logic as original)
                        name = "page_" + str(count) + ".jpg"
                        img_bytes = io.BytesIO()
                        img.save(img_bytes, "JPEG")
                        img_bytes.seek(0)
                        zf.writestr(name, img_bytes.read())
                        count = count + 1

                zip_buffer.seek(0)

                # Provide a download button for the zip of all images
                st.download_button(
                    label="Download All Images (ZIP)",
                    data=zip_buffer,
                    file_name="pdf_images.zip",
                    mime="application/zip",
                )

                # Show preview of each page
                st.subheader("Preview")
                count = 1
                for img in images:
                    st.image(img, caption=f"Page {count}", use_container_width=True)
                    count = count + 1

            except Exception as e:
                st.error(f"Error converting PDF: {e}")
            finally:
                os.unlink(tmp_path)


def images_to_pdf_tool():
    """Convert multiple images into a single PDF file."""
    st.header("2. Images to PDF")
    st.write("Upload one or more images to combine them into a single PDF.")

    uploaded_images = st.file_uploader(
        "Upload images",
        type=["jpg", "jpeg", "png", "bmp", "tiff"],
        accept_multiple_files=True,
        key="img_to_pdf",
    )

    output_name = st.text_input("Output PDF name", value="output.pdf", key="img_pdf_name")

    if uploaded_images:
        if st.button("Convert to PDF"):
            if not output_name.endswith(".pdf"):
                output_name_final = output_name + ".pdf"
            else:
                output_name_final = output_name

            try:
                # Core logic: open images and convert to RGB (same as original)
                images = []
                for uploaded_img in uploaded_images:
                    img = Image.open(uploaded_img)
                    img = img.convert("RGB")
                    images.append(img)

                if len(images) == 0:
                    st.error("No images uploaded.")
                    return

                # Core logic: save first image with remaining appended (same as original)
                first_img = images[0]
                other_img = []
                for j in range(1, len(images)):
                    other_img.append(images[j])

                pdf_buffer = io.BytesIO()
                first_img.save(pdf_buffer, format="PDF", save_all=True, append_images=other_img)
                pdf_buffer.seek(0)

                st.success("Images converted into PDF successfully!")

                # Provide download button for the generated PDF
                st.download_button(
                    label="Download PDF",
                    data=pdf_buffer,
                    file_name=output_name_final,
                    mime="application/pdf",
                )

                # Show preview of uploaded images
                st.subheader("Uploaded Images Preview")
                for i, uploaded_img in enumerate(uploaded_images):
                    st.image(uploaded_img, caption=f"Image {i + 1}", use_container_width=True)

            except Exception as e:
                st.error(f"Error converting images to PDF: {e}")


def merge_pdfs_tool():
    """Merge multiple PDF files into one."""
    st.header("3. Merge PDFs")
    st.write("Upload multiple PDF files to merge them into a single PDF.")

    uploaded_pdfs = st.file_uploader(
        "Upload PDF files",
        type=["pdf"],
        accept_multiple_files=True,
        key="merge_pdfs",
    )

    output_name = st.text_input("Output PDF name", value="merged.pdf", key="merge_pdf_name")

    if uploaded_pdfs:
        if st.button("Merge PDFs"):
            if not output_name.endswith(".pdf"):
                output_name_final = output_name + ".pdf"
            else:
                output_name_final = output_name

            try:
                # Core logic: use PdfMerger to merge files (same as original)
                merger = PdfMerger()

                for uploaded_pdf in uploaded_pdfs:
                    merger.append(uploaded_pdf)

                merged_buffer = io.BytesIO()
                merger.write(merged_buffer)
                merger.close()
                merged_buffer.seek(0)

                st.success("PDF files merged successfully!")

                # Provide download button for the merged PDF
                st.download_button(
                    label="Download Merged PDF",
                    data=merged_buffer,
                    file_name=output_name_final,
                    mime="application/pdf",
                )

            except Exception as e:
                st.error(f"Error merging PDFs: {e}")


# --- Route to the selected tool ---
if tool == "PDF to Images":
    pdf_to_images_tool()
elif tool == "Images to PDF":
    images_to_pdf_tool()
elif tool == "Merge PDFs":
    merge_pdfs_tool()
