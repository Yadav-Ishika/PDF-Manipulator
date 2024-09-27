import io
import os
import fitz
import PyPDF2
import tempfile
import pdfplumber
import pytesseract
import pandas as pd
import streamlit as st

from io import BytesIO
from PyPDF2 import PdfWriter
from docx2pdf import convert
from datetime import datetime
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from PIL import Image, ImageEnhance
from PyPDF2 import PdfReader, PdfWriter
from pdf2image import convert_from_path
from pdf2image import convert_from_bytes
from reportlab.lib.pagesizes import letter
from streamlit_sortables import sort_items
from reportlab.lib.utils import ImageReader

st.markdown(
    """
    <style>
    .stButton > button {
        width: 100%;
    }
    </style>
    """,
    unsafe_allow_html=True
)


placeholder = st.empty()

placeholder.markdown("""
    <style>
        .header-container {
            display: flex;
            flex-direction: column;
            gap: 0.5vw;
            align-items: center;
            padding: 20px;
            background-color: #f8f9fa; /* Light background for contrast */
            border-radius: 8px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            margin-bottom: 10px;
            margin-top: -3.604vw;
        }
        .header-title {
            text-align: center;
            font-size: 4.2vw;
            margin: 0;
        }
        .header-subtitle {
            color: green;
            font-weight: bold;
        }
        .description {
            text-align: center;
            font-size: 1.2vw;
            color: #555;
            max-width: 600px; /* Limit width for readability */
        }
        hr {
            width: 80%; /* Horizontal rule width */
            border: 1px solid #ccc;
        }
    </style>
    <div class="header-container">
        <h1 class="header-title">"PDF Manipulator"<br /><span class="header-subtitle">Welcomes</span> You!</h1>
        <hr />
        <p class="description">
            Our service offers seamless manipulations of PDF in various ways, including:
            <ul>
                <li>Merging & Splitting PDF(s)</li>
                <li>Adding, Deleting & Re-arranging PDF Pages)</li>
                <li>Watermarking PDF & Rotating PDF Pages</li>
                <li>Extracting and Editing PDF Metadata</li>
                <li>PDF-OCR Extraction</li>
                <li>Encryption & Decryption of PDF</li>
            </ul>
            Experience fast, reliable, and user-friendly PDF Manipulator to meet all your needs!
        </p>
    </div>
""", unsafe_allow_html=True)

if 'conversion_type' not in st.session_state:
    st.session_state.conversion_type = None

if 'merge_pdf_paths' not in st.session_state:
    st.session_state.merge_paths = None

if 'split_pdf_paths' not in st.session_state:
    st.session_state.split_paths = None

if 'rearrang_pdf_paths' not in st.session_state:
    st.session_state.rearrang_paths = None

if 'watermark_pdf_paths' not in st.session_state:
    st.session_state.watermark_paths = None

if 'add_del_pdf_paths' not in st.session_state:
    st.session_state.add_del_paths = []

if 'metadetaext_pdf_paths' not in st.session_state:
    st.session_state.metadetaext_paths = []

if 'metadetaedt_pdf_paths' not in st.session_state:
    st.session_state.metadetaedt_paths = []

if 'enc_dec_pdf_paths' not in st.session_state:
    st.session_state.enc_dec_paths = []

if 'ocr_pdf_paths' not in st.session_state:
    st.session_state.ocr_paths = []

if 'rotate_pdf_paths' not in st.session_state:
    st.session_state.rotate_paths = []


st.sidebar.markdown("<div style='position: relative; top: -30px;'><h1 style='text-align: center; color: #000; font-size: 3.5vw;'>Services</h1></div>", unsafe_allow_html=True)

if st.button("Reload"):
    st.session_state.conversion_type = "reload_content"

if st.sidebar.button("Merge PDFs"):
    st.session_state.conversion_type = "mpdf"
    placeholder.empty()

if st.sidebar.button("Split PDF"):
    st.session_state.conversion_type = "spdf"
    placeholder.empty()

if st.sidebar.button("Rearrang PDF Pages"):
    st.session_state.conversion_type = "rapdf"
    placeholder.empty()

if st.sidebar.button("Watermark PDF"):
    st.session_state.conversion_type = "wpdf"
    placeholder.empty()

if st.sidebar.button("Add or Delete PDF Pages"):
    st.session_state.conversion_type = "adpdf"
    placeholder.empty()

if st.sidebar.button("Extract PDF Metadata"):
    st.session_state.conversion_type = "exmdpdf"
    placeholder.empty()

if st.sidebar.button("Edit PDF Metadata"):
    st.session_state.conversion_type = "edmdpdf"
    placeholder.empty()

if st.sidebar.button("Encrypt / Decrypt PDF"):
    st.session_state.conversion_type = "edpdf"
    placeholder.empty()

if st.sidebar.button("Extract Text - OCR PDF"):
    st.session_state.conversion_type = "ocrpdf"
    placeholder.empty()

if st.sidebar.button("Rotate PDF Pages"):
    st.session_state.conversion_type = "rtpdf"
    placeholder.empty()


if st.session_state.conversion_type == "reload_content":
    
    placeholder.markdown("""
        <style>
            .header-container {
                display: flex;
                flex-direction: column;
                gap: 0.5vw;
                align-items: center;
                padding: 20px;
                background-color: #f8f9fa; /* Light background for contrast */
                border-radius: 8px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                margin-bottom: 10px;
                margin-top: -3.604vw;
            }
            .header-title {
                text-align: center;
                font-size: 4.2vw;
                margin: 0;
            }
            .header-subtitle {
                color: green;
                font-weight: bold;
            }
            .description {
                text-align: center;
                font-size: 1.2vw;
                color: #555;
                max-width: 600px; /* Limit width for readability */
            }
            hr {
                width: 80%; /* Horizontal rule width */
                border: 1px solid #ccc;
            }
        </style>
        <div class="header-container">
            <h1 class="header-title">"PDF Manipulator"<br /><span class="header-subtitle">Welcomes</span> You!</h1>
            <hr />
            <p class="description">
                Our service offers seamless manipulations of PDF in various ways, including:
                <ul>
                    <li>Merging & Splitting PDF(s)</li>
                    <li>Adding, Deleting & Re-arranging PDF Pages)</li>
                    <li>Watermarking PDF & Rotating PDF Pages</li>
                    <li>Extracting and Editing PDF Metadata</li>
                    <li>PDF-OCR Extraction</li>
                    <li>Encryption & Decryption of PDF</li>
                </ul>
                Experience fast, reliable, and user-friendly PDF Manipulator to meet all your needs!
            </p>
        </div>
    """, unsafe_allow_html=True)





# Handle Merge PDF
if st.session_state.conversion_type == "mpdf":

    st.title("PDF Merger with Drag-and-Drop Order Selection")

    st.write("Upload multiple PDF files and drag to select the order in which to merge them.")

    uploaded_files = st.file_uploader("Choose PDFs to merge", accept_multiple_files=True, type="pdf")

    placeholder.empty()

    if uploaded_files:

        pdf_names = [uploaded_file.name for uploaded_file in uploaded_files]
        selected_order = sort_items(pdf_names)
        st.write("Selected order of PDFs:", selected_order)
        new_file_name = st.text_input("Enter a name for the merged PDF:", value="merged_output.pdf")

        if new_file_name and not new_file_name.endswith(".pdf"):
            new_file_name += ".pdf"

        if st.button("Merge PDFs", key="merge_button"):

            if len(selected_order) < 2:
                st.warning("Please select at least two PDFs for merging.")

            else:
                pdf_writer = PdfWriter()

                for pdf_name in selected_order:
                    for uploaded_file in uploaded_files:
                        if uploaded_file.name == pdf_name:
                            reader = PyPDF2.PdfReader(uploaded_file)
                            for page_num in range(len(reader.pages)):
                                page = reader.pages[page_num]
                                pdf_writer.add_page(page)

                merged_pdf = BytesIO()
                pdf_writer.write(merged_pdf)
                merged_pdf.seek(0)

                st.success("PDFs merged successfully in the selected order!")

                st.download_button(
                    label="Download Merged PDF",
                    data=merged_pdf,
                    file_name=new_file_name,
                    mime="application/pdf"
                )




# Handle Split PDF
if st.session_state.conversion_type == "spdf":
    
    def split_pdf(pdf_file, split_option, start_page=None, end_page=None):
        pdf_reader = PdfReader(pdf_file)
        total_pages = len(pdf_reader.pages)

        output_files = []

        if split_option == 'One file per page':

            for page_num in range(total_pages):
                pdf_writer = PdfWriter()
                pdf_writer.add_page(pdf_reader.pages[page_num])
                output_filename = os.path.join(tempfile.gettempdir(), f"page_{page_num + 1}.pdf")
            
                with open(output_filename, 'wb') as output_pdf:
                    pdf_writer.write(output_pdf)
                output_files.append(output_filename)

        elif split_option == 'Range of pages':
            
            if start_page is not None and end_page is not None:
            
                pdf_writer = PdfWriter()
            
                for page_num in range(start_page - 1, end_page):
                    pdf_writer.add_page(pdf_reader.pages[page_num])
                output_filename = os.path.join(tempfile.gettempdir(), f"pages_{start_page}_to_{end_page}.pdf")
            
                with open(output_filename, 'wb') as output_pdf:
                    pdf_writer.write(output_pdf)
                output_files.append(output_filename)

        return output_files

    @st.cache_data
    def display_pdf_pages(pdf_file):
        pdf_images = convert_from_bytes(pdf_file.read())
        return pdf_images

    st.title("PDF Splitter")

    uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])

    placeholder.empty()

    if 'output_files' not in st.session_state:
        st.session_state.output_files = []

    if 'new_file_names' not in st.session_state:
        st.session_state.new_file_names = []

    if uploaded_file:
        st.subheader("Preview PDF Pages")
        pdf_images = display_pdf_pages(uploaded_file)

        cols = st.columns(len(pdf_images))
        
        for idx, image in enumerate(pdf_images):
            with cols[idx]:
                st.image(image, caption=f"Page {idx + 1}", use_column_width=True)

        pdf_reader = PdfReader(uploaded_file)
        total_pages = len(pdf_reader.pages)
        st.write(f"The PDF has {total_pages} pages.")

        split_option = st.radio(
            "Choose how to split the PDF",
            ('One file per page', 'Range of pages'),
            key='split_option'
        )

        if split_option == 'One file per page':
            if st.button('Split PDF', key="split_button_1"):
                st.session_state.output_files = split_pdf(uploaded_file, split_option)
                st.session_state.new_file_names = [f"page_{i + 1}.pdf" for i in range(len(st.session_state.output_files))]
        elif split_option == 'Range of pages':
            start_page = st.number_input("Start Page", min_value=1, max_value=total_pages, value=1)
            end_page = st.number_input("End Page", min_value=start_page, max_value=total_pages, value=total_pages)

            if st.button('Split PDF',  key="split_button_2"):
                if start_page <= end_page:
                    st.session_state.output_files = split_pdf(uploaded_file, split_option, start_page, end_page)
                    st.session_state.new_file_names = [f"pages_{start_page}_to_{end_page}.pdf"]
                else:
                    st.error("Start Page must be less than or equal to End Page")

    if st.session_state.output_files:
        st.write("### Download your split PDFs:")

        for idx, file in enumerate(st.session_state.output_files):

            new_file_name = st.text_input(f"Rename {os.path.basename(file)}", value=st.session_state.new_file_names[idx], key=f"rename_{idx}")  

            if new_file_name and not new_file_name.endswith(".pdf"):
                new_file_name += ".pdf"

            with open(file, "rb") as f:
                st.download_button(
                    label=f"Download {new_file_name}",
                    data=f,
                    file_name=new_file_name
                )



# Handle Rearrange PDF
if st.session_state.conversion_type == "rapdf":
    
    def pdf_to_images(pdf_file_path):
        images = convert_from_path(pdf_file_path)
        return images

    def save_rearranged_pdf(images, page_order, output_file):
        writer = PyPDF2.PdfWriter()
        for page in page_order:
            index = int(page.split(" ")[1]) - 1
            temp_pdf_path = tempfile.NamedTemporaryFile(suffix=".pdf", delete=False).name
            images[index].save(temp_pdf_path, "PDF")
            
            with open(temp_pdf_path, "rb") as temp_pdf:
                writer.add_page(PyPDF2.PdfReader(temp_pdf).pages[0])
            os.remove(temp_pdf_path)
        
        with open(output_file, "wb") as f:
            writer.write(f)

    st.title("PDF Page Rearranger")

    pdf_file = st.file_uploader("Upload a PDF file", type="pdf")

    placeholder.empty()

    if pdf_file:

        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf_file:
            temp_pdf_file.write(pdf_file.read())
            temp_pdf_path = temp_pdf_file.name

        images = pdf_to_images(temp_pdf_path)

        page_order = st.multiselect(
            "Rearrange the pages by selecting and ordering:",
            options=[f"Page {i+1}" for i in range(len(images))],
            default=[f"Page {i+1}" for i in range(len(images))],
            format_func=lambda x: x
        )

        cols = st.columns(len(page_order))
        for col, page in zip(cols, page_order):
            index = int(page.split(" ")[1]) - 1
            with col:
                st.image(images[index], caption=page)

        output_file_name = st.text_input("Enter output file name:", "rearranged_pdf.pdf")

        if st.button("Save Rearranged PDF", key="rearrange_button") and output_file_name:
            save_rearranged_pdf(images, page_order, output_file_name)
            st.success(f"Rearranged PDF saved as {output_file_name}")

            with open(output_file_name, "rb") as f:
                st.download_button(
                    label="Download Rearranged PDF",
                    data=f,
                    file_name=output_file_name,
                    mime="application/pdf"
                )




# Handle PDF Watermarking
if st.session_state.conversion_type == "wpdf":
    
    def create_text_watermark(text, opacity, rotation):
        buffer = io.BytesIO()
        c = canvas.Canvas(buffer, pagesize=letter)
        c.setFont("Helvetica", 60)
        c.setFillAlpha(opacity)

        c.saveState()
        c.translate(300, 400)
        c.rotate(rotation)
        c.drawCentredString(0, 0, text)
        c.restoreState()

        c.save()
        buffer.seek(0)
        return buffer

    def create_image_watermark(image, opacity, rotation):
        buffer = io.BytesIO()
        c = canvas.Canvas(buffer, pagesize=letter)
        c.setFillAlpha(opacity)
        
        c.saveState()
        c.translate(300, 400)
        c.rotate(rotation)

        c.drawImage(ImageReader(image), -150, -100, width=300, height=200)
        c.restoreState()

        c.save()
        buffer.seek(0)
        return buffer
    
    def add_watermark_to_pdf(input_pdf, watermark, page_selection):
        reader = PdfReader(input_pdf)
        writer = PdfWriter()

        watermark_pdf = PdfReader(watermark)
        watermark_page = watermark_pdf.pages[0]

        total_pages = len(reader.pages)
        pages_to_watermark = []

        if page_selection == "All":
            pages_to_watermark = range(total_pages)

        elif page_selection == "Single Page":
            selected_page = st.number_input(f"Select page (1-{total_pages})", min_value=1, max_value=total_pages, value=1)
            pages_to_watermark = [selected_page - 1]

        elif page_selection == "Page Range":
            start_page, end_page = st.slider(f"Select page range (1-{total_pages})", 1, total_pages, (1, total_pages))
            pages_to_watermark = range(start_page - 1, end_page)

        for i, page in enumerate(reader.pages):
            if i in pages_to_watermark:
                page.merge_page(watermark_page)
            writer.add_page(page)

        output_pdf = io.BytesIO()
        writer.write(output_pdf)
        output_pdf.seek(0)

        return output_pdf

    st.title("PDF Watermarking")

    st.write("Upload a PDF file and add a text or image watermark to specific pages, with rotation and opacity control.")

    uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])

    placeholder.empty()

    if uploaded_file:
        watermark_type = st.selectbox("Watermark Type", ["Text", "Image"])
        rotation = st.slider("Watermark Rotation (degrees)", min_value=0, max_value=360, value=0)
        opacity = st.slider("Watermark Opacity (0: transparent, 1: opaque)", min_value=0.0, max_value=1.0, value=0.3)
        page_selection = st.radio("Select Pages to Watermark", ("All", "Single Page", "Page Range"))

        if watermark_type == "Text":
            watermark_text = st.text_input("Enter Watermark Text", value="Confidential")
            if watermark_text:
                st.write(f"Watermark: {watermark_text}")
                watermark = create_text_watermark(watermark_text, opacity, rotation)
                watermarked_pdf = add_watermark_to_pdf(uploaded_file, watermark, page_selection)

                st.download_button(
                    label="Download Watermarked PDF",
                    data=watermarked_pdf,
                    file_name="watermarked_output.pdf",
                    mime="application/pdf"
                )

        elif watermark_type == "Image":
            uploaded_image = st.file_uploader("Upload Image for Watermark", type=["png", "jpg", "jpeg"])
            if uploaded_image:
                st.success("Image Watermarking in progress...")

                watermark = create_image_watermark(uploaded_image, opacity, rotation)
                watermarked_pdf = add_watermark_to_pdf(uploaded_file, watermark, page_selection)

                st.download_button(
                    label="Download Watermarked PDF",
                    data=watermarked_pdf,
                    file_name="watermarked_output.pdf",
                    mime="application/pdf"
                )


# Handle Add & Delete PDF Pages
if st.session_state.conversion_type == "adpdf":

    def pdf_to_images(pdf_path):
        pdf_document = fitz.open(pdf_path)
        images = []

        for page_num in range(pdf_document.page_count):
            page = pdf_document.load_page(page_num)
            pix = page.get_pixmap()
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            images.append(img)

        return images

    def save_pdf(doc, output_pdf_path):
        doc.save(output_pdf_path)

    def add_pages_to_pdf(main_pdf_path, additional_files, position):
        main_pdf = fitz.open(main_pdf_path)
        
        for uploaded_file in additional_files:
            
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                tmp_file.write(uploaded_file.read())
                tmp_file_path = tmp_file.name

            new_pdf = fitz.open(tmp_file_path)
        
            for page in new_pdf:
                main_pdf.insert_pdf(new_pdf, from_page=page.number, to_page=page.number, start_at=position)
        
        return main_pdf

    def delete_pages_from_pdf(main_pdf_path, pages_to_delete):
        main_pdf = fitz.open(main_pdf_path)
        for page in sorted(pages_to_delete, reverse=True):
            main_pdf.delete_page(page)
        return main_pdf

    st.title("Add or Delete PDF Pages")

    st.header("Add Pages to PDF")

    uploaded_pdf = st.file_uploader("Upload Main PDF", type=["pdf"])

    placeholder.empty()

    if uploaded_pdf:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_main_pdf:
            tmp_main_pdf.write(uploaded_pdf.read())
            main_pdf_path = tmp_main_pdf.name

        st.subheader("Pages in the Main PDF:")
        main_pdf_images = pdf_to_images(main_pdf_path)
        cols = st.columns(len(main_pdf_images))
        for i, img in enumerate(main_pdf_images):
            cols[i].image(img, caption=f"Page {i + 1}")

        st.subheader("Upload PDF or Images to Add")
        additional_files = st.file_uploader("Select files to add (PDF or Images)", type=["pdf", "jpg", "jpeg", "png"], accept_multiple_files=True)

        if additional_files:
            position = st.number_input(f"Where to insert pages (1 to {len(main_pdf_images) + 1})", min_value=1, max_value=len(main_pdf_images) + 1)

            if "output_pdf_name_add" not in st.session_state:
                st.session_state.output_pdf_name_add = "output"

            output_pdf_name_add = st.text_input("Enter new PDF file name (without .pdf)", 
                                                 value=st.session_state.output_pdf_name_add, 
                                                 key="output_pdf_name_add")

            if st.button("Add Pages", key="add_button"):
                added_pdf = add_pages_to_pdf(main_pdf_path, additional_files, position - 1)

                output_pdf_path_add = os.path.join(tempfile.gettempdir(), f"{output_pdf_name_add}.pdf")
                save_pdf(added_pdf, output_pdf_path_add)

                st.success(f"Pages added successfully! Download your new PDF:")
                with open(output_pdf_path_add, "rb") as file:
                    st.download_button(label="Download PDF", data=file, file_name=f"{output_pdf_name_add}.pdf")

    st.header("Delete Pages from PDF")

    uploaded_pdf_delete = st.file_uploader("Upload Main PDF for Deletion", type=["pdf"], key="delete_pdf")

    placeholder.empty()

    if uploaded_pdf_delete:
        
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_main_pdf_delete:
            tmp_main_pdf_delete.write(uploaded_pdf_delete.read())
            main_pdf_path_delete = tmp_main_pdf_delete.name

        st.subheader("Pages in the Main PDF:")
        main_pdf_images_delete = pdf_to_images(main_pdf_path_delete)
        cols_delete = st.columns(len(main_pdf_images_delete))
        for i, img in enumerate(main_pdf_images_delete):
            cols_delete[i].image(img, caption=f"Page {i + 1}")

        pages_to_delete = st.multiselect("Select pages to delete", list(range(1, len(main_pdf_images_delete) + 1)))

        if "output_pdf_name_delete" not in st.session_state:
            st.session_state.output_pdf_name_delete = "output"

        output_pdf_name_delete = st.text_input("Enter new PDF file name (without .pdf)", 
                                                value=st.session_state.output_pdf_name_delete, 
                                                key="output_pdf_name_delete")

        if st.button("Delete Pages", key="delete_button"):
            modified_pdf_delete = delete_pages_from_pdf(main_pdf_path_delete, [p - 1 for p in pages_to_delete])

            output_pdf_path_delete = os.path.join(tempfile.gettempdir(), f"{output_pdf_name_delete}.pdf")
            save_pdf(modified_pdf_delete, output_pdf_path_delete)

            st.success(f"Pages deleted successfully! Download your new PDF:")

            with open(output_pdf_path_delete, "rb") as file:
                st.download_button(label="Download PDF", data=file, file_name=f"{output_pdf_name_delete}.pdf")


# Handle PDF Metadata Extractor
if st.session_state.conversion_type == "exmdpdf":
    
    def extract_pdf_details(pdf_file):
        details = {}

        with open(pdf_file, "rb") as file:
            pdf_reader = PdfReader(file)
            details['metadata'] = pdf_reader.metadata

            details['date_created'] = details['metadata'].get('/CreationDate', 'N/A')
            details['date_modified'] = details['metadata'].get('/ModDate', 'N/A')
            details['size'] = os.path.getsize(pdf_file)
            details['embedded_files'] = []

            if '/EmbeddedFiles' in pdf_reader.trailer['/Root']:
                embedded_files_dict = pdf_reader.trailer['/Root']['/EmbeddedFiles']
            
                if '/Names' in embedded_files_dict:
                    names_list = embedded_files_dict['/Names']
            
                    for i in range(0, len(names_list), 2):
                        file_name = names_list[i]
                        file_dict = names_list[i + 1]
                        details['embedded_files'].append(file_name)

        with pdfplumber.open(pdf_file) as pdf:
            details['text'] = ""
            details['images'] = []
            details['pages'] = []

            for i, page in enumerate(pdf.pages):
                details['pages'].append({
                    'page_number': i + 1,
                    'width': page.width,
                    'height': page.height,
                    'rotation': page.rotation
                })
                details['text'] += page.extract_text() or ""

                images = page.images
                for img in images:
                    image = page.to_image()
                    details['images'].append(image.original)

                if hasattr(page, 'annots'):
                    details['pages'][i]['annotations'] = page.annots if page.annots else []
                else:
                    details['pages'][i]['annotations'] = []

        return details


    def wrap_text(text, c, x, y, max_width):
        lines = []
        words = text.split(' ')
        current_line = ""

        for word in words:
            test_line = current_line + word + ' '
            width = c.stringWidth(test_line, "Helvetica", 10)

            if width > max_width:
                lines.append(current_line.strip())
                current_line = word + ' '
            else:
                current_line = test_line

        lines.append(current_line.strip())
        for line in lines:
            c.drawString(x, y, line)
            y -= 15

        return y


    def generate_pdf(details, output_path):
        c = canvas.Canvas(output_path, pagesize=letter)
        width, height = letter
        margin = 50

        c.setFont("Helvetica-Bold", 16)
        c.setFillColorRGB(0.1, 0.2, 0.8)
        c.drawString(100, height - margin, "PDF Details Extractor")

        c.setStrokeColorRGB(0.1, 0.2, 0.8)
        c.line(100, height - margin - 10, width - 100, height - margin - 10)

        y_position = height - margin - 20

        def check_page_space(space_required):
            nonlocal y_position
            if y_position - space_required < 0:
                c.showPage()
                y_position = height - margin - 20

        c.setFont("Helvetica-Bold", 12)
        c.setFillColor(colors.black)
        c.drawString(100, y_position, "Metadata:")
        y_position -= 20

        c.setFont("Helvetica", 10)
        for key, value in details['metadata'].items():
            line = f"{key}: {value}"
            check_page_space(15)
            y_position = wrap_text(line, c, 120, y_position, width - 140)

        c.setFont("Helvetica-Bold", 12)
        check_page_space(20)
        c.drawString(100, y_position, "Additional Details:")
        y_position -= 20

        c.setFont("Helvetica", 10)
        c.drawString(120, y_position, f"Date Created: {details['date_created']}")
        y_position -= 15
        c.drawString(120, y_position, f"Date Modified: {details['date_modified']}")
        y_position -= 15
        c.drawString(120, y_position, f"Size: {details['size']} bytes")
        y_position -= 20

        c.setFont("Helvetica-Bold", 12)
        check_page_space(20)
        c.drawString(100, y_position, "Extracted Text:")
        y_position -= 20

        c.setFont("Helvetica", 10)
        for line in details['text'].splitlines():
            check_page_space(15)
            y_position = wrap_text(line, c, 120, y_position, width - 140)

        c.setFont("Helvetica-Bold", 12)
        check_page_space(20)
        c.drawString(100, y_position, "Page Information:")
        y_position -= 20

        c.setFont("Helvetica", 10)
        for page in details['pages']:
            line = f"Page {page['page_number']}: Width = {page['width']}, Height = {page['height']}, Rotation = {page['rotation']}"
            check_page_space(15)
            y_position = wrap_text(line, c, 120, y_position, width - 140)
            if page['annotations']:
                check_page_space(15)
                y_position = wrap_text(f"Annotations: {page['annotations']}", c, 140, y_position, width - 140)

        c.setFont("Helvetica-Bold", 12)
        check_page_space(20)
        c.drawString(100, y_position, "Embedded Files:")
        y_position -= 20

        c.setFont("Helvetica", 10)
        if details['embedded_files']:
            for file in details['embedded_files']:
                check_page_space(15)
                y_position = wrap_text(f"Embedded File: {file}", c, 120, y_position, width - 140)
        else:
            check_page_space(15)
            y_position = wrap_text("No embedded files found.", c, 120, y_position, width - 140)

        y_position -= 10
        c.setStrokeColorRGB(0.1, 0.2, 0.8)
        c.line(100, y_position, width - 100, y_position)

        y_position -= 20
        c.setFont("Helvetica-Oblique", 10)
        footer_text = f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        c.drawString(100, y_position, footer_text)

        c.save()


    st.title("PDF Metadata Extractor")
    
    st.write("Upload a PDF file to extract its details.")
    
    pdf_file = st.file_uploader("Upload PDF", type=["pdf"])
    
    placeholder.empty()

    if pdf_file is not None:
    
        pdf_file_path = os.path.join(pdf_file.name)
    
        with open(pdf_file_path, "wb") as f:
            f.write(pdf_file.getbuffer())
    
        details = extract_pdf_details(pdf_file_path)
    
        st.subheader("Metadata")
        st.json(details['metadata'])
    
        st.subheader("Extracted Text")
        st.text_area("Extracted Text", details['text'], height=300)
    
        st.subheader("Page Information")
        for page in details['pages']:
            st.write(f"Page {page['page_number']}: Width = {page['width']}, Height = {page['height']}, Rotation = {page['rotation']}")
    
        st.subheader("Embedded Files")
        if details['embedded_files']:
            for file in details['embedded_files']:
                st.write(f"Embedded File: {file}")
        else:
            st.write("No embedded files found.")
    
        output_pdf_path = "extracted_details.pdf"
        generate_pdf(details, output_pdf_path)
    
        with open(output_pdf_path, "rb") as f:
            st.download_button("Download Extracted Details PDF", f, file_name="extracted_details.pdf")



# Handle PDF Metadata Editing
if st.session_state.conversion_type == "edmdpdf":
    
    st.title("PDF Metadata Editor")

    uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")

    placeholder.empty()

    if uploaded_file is not None:
        reader = PdfReader(uploaded_file)
        writer = PdfWriter()

        metadata = reader.metadata
        st.subheader("Current Metadata:")
        st.write(metadata)

        author = st.text_input("Author", value=metadata.get('/Author', ''))
        title = st.text_input("Title", value=metadata.get('/Title', ''))
        subject = st.text_input("Subject", value=metadata.get('/Subject', ''))
        keywords = st.text_input("Keywords", value=metadata.get('/Keywords', ''))

        if st.button("Update Metadata", key="update_metadata_button"):

            writer.add_metadata({
                '/Author': author,
                '/Title': title,
                '/Subject': subject,
                '/Keywords': keywords
            })

            output = io.BytesIO()
            writer.write(output)
            output.seek(0)
            st.download_button(
                label="Download updated PDF",
                data=output,
                file_name="updated_pdf.pdf",
                mime="application/pdf"
            )

# Handle PDF Encryption & Decryption
if st.session_state.conversion_type == "edpdf":

    def encrypt_pdf(input_pdf, password):
        pdf_writer = PdfWriter()
        pdf_reader = PdfReader(input_pdf)

        for page in range(len(pdf_reader.pages)):
            pdf_writer.add_page(pdf_reader.pages[page])

        output_pdf = f"encrypted_{os.path.basename(input_pdf)}"
        with open(output_pdf, 'wb') as f:
            pdf_writer.encrypt(password)
            pdf_writer.write(f)

        return output_pdf

    def decrypt_pdf(input_pdf, password):
        pdf_reader = PdfReader(input_pdf)
        if pdf_reader.is_encrypted:
            pdf_reader.decrypt(password)

        output_pdf = f"decrypted_{os.path.basename(input_pdf)}"
        pdf_writer = PdfWriter()
        for page in range(len(pdf_reader.pages)):
            pdf_writer.add_page(pdf_reader.pages[page])

        with open(output_pdf, 'wb') as f:
            pdf_writer.write(f)

        return output_pdf

    st.title("PDF Security : Encryption & Decryption")

    st.header("Encrypt PDF")

    uploaded_file_encrypt = st.file_uploader("Upload PDF to Encrypt", type=["pdf"])

    placeholder.empty()

    if uploaded_file_encrypt:
        password_encrypt = st.text_input("Enter Password for Encryption", type="password")

        if st.button("Encrypt PDF", key="enc_button"):
            if password_encrypt:

                temp_input_file = f"temp_{uploaded_file_encrypt.name}"

                with open(temp_input_file, "wb") as f:
                    f.write(uploaded_file_encrypt.getbuffer())
                output_pdf = encrypt_pdf(temp_input_file, password_encrypt)
                st.success("PDF encrypted successfully!")

                with open(output_pdf, "rb") as f:
                    st.download_button("Download Encrypted PDF", f, file_name=output_pdf, mime="application/pdf")

    st.header("Decrypt PDF")
    uploaded_file_decrypt = st.file_uploader("Upload Encrypted PDF", type=["pdf"], key="decrypt")

    if uploaded_file_decrypt:
        password_decrypt = st.text_input("Enter Password for Decryption", type="password", key="decrypt_password")

        if st.button("Decrypt PDF", key="dec_button"):
            if password_decrypt:
                temp_input_file = f"temp_{uploaded_file_decrypt.name}"
                
                with open(temp_input_file, "wb") as f:
                    f.write(uploaded_file_decrypt.getbuffer())
                
                try:
                    output_pdf = decrypt_pdf(temp_input_file, password_decrypt)
                    st.success("PDF decrypted successfully!")
                
                    with open(output_pdf, "rb") as f:
                        st.download_button("Download Decrypted PDF", f, file_name=output_pdf, mime="application/pdf")
                
                except Exception as e:
                    st.error("Failed to decrypt PDF. Please check your password.")


# Handle PDF OCR
if st.session_state.conversion_type == "ocrpdf":
    
    extracted_text = "Null"

    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Directory Specific Adjustment Needed

    def enhance_image_for_ocr(img):
        """Enhance the image for better OCR results."""
        img = img.convert('L')
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(2.0)
        return img

    def pdf_to_searchable_pdf(uploaded_pdf):
        temp_pdf_path = tempfile.mktemp(suffix=".pdf")
        try:
            pdf_document = fitz.open(stream=uploaded_pdf.read(), filetype="pdf")
            new_pdf = fitz.open()

            for page_num in range(len(pdf_document)):
                page = pdf_document.load_page(page_num)
                pix = page.get_pixmap()
                img_bytes = pix.tobytes("png")
                img = Image.open(io.BytesIO(img_bytes))

                img = enhance_image_for_ocr(img)
                text = pytesseract.image_to_string(img)
                st.write(f"OCR Output for Page {page_num + 1}: {text}")

                new_page = new_pdf.new_page(width=page.rect.width, height=page.rect.height)

                margin = 50
                text_rect = fitz.Rect(margin, margin, new_page.rect.width - margin, new_page.rect.height - margin)

                new_page.insert_textbox(text_rect, text, fontsize=10, align=fitz.TEXT_ALIGN_LEFT)

            new_pdf.save(temp_pdf_path)
            new_pdf.close()
            pdf_document.close()

            return temp_pdf_path

        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            if os.path.exists(temp_pdf_path):
                os.remove(temp_pdf_path)
            return None

    st.title("Scanned to Searchable PDF - OCR")

    uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

    placeholder.empty()

    if uploaded_file is not None:
        searchable_pdf_path = pdf_to_searchable_pdf(uploaded_file)

        if searchable_pdf_path:
            st.success("Searchable PDF created successfully!")
            
            with open(searchable_pdf_path, "rb") as f:
                st.download_button("Download Searchable PDF", f, file_name="searchable.pdf")

            os.remove(searchable_pdf_path)


# Handle PDF Page Rotation
if st.session_state.conversion_type == "rtpdf":

    st.title("PDF Page Rotator (Clockwise)")

    uploaded_pdf = st.file_uploader("Upload PDF", type="pdf")

    placeholder.empty()

    if uploaded_pdf:

        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
            temp_pdf.write(uploaded_pdf.read())
            temp_pdf_path = temp_pdf.name

        pdf_images = convert_from_path(temp_pdf_path)

        st.write("**Original PDF Pages:**")

        col_images = st.columns(len(pdf_images))
        for i, img in enumerate(pdf_images):
            with col_images[i]:
                st.image(img, caption=f"Page {i + 1}", use_column_width=True)

        page_input = st.text_input("Enter page number or range (e.g., 1, 2-5)", value="1")
        rotation_angle = st.selectbox("Select Rotation Angle", [0, 90, 180, 270, 360])

        output_filename = st.text_input("Enter output PDF name", value="rotated_output.pdf")

        if st.button("Rotate Pages",key="rt_button"):
            pages_to_rotate = []
            
            if '-' in page_input:
                start, end = map(int, page_input.split('-'))
                pages_to_rotate = list(range(start, end + 1))
            else:
                pages_to_rotate = [int(page_input)]

            rotated_images = []
            
            for i, img in enumerate(pdf_images):
                if i + 1 in pages_to_rotate:
                    rotated_img = img.rotate(-rotation_angle, expand=True)
                    rotated_images.append(rotated_img)
                else:
                    rotated_images.append(img)

            st.write("**Rotated PDF Pages (Clockwise):**")
            col_rotated_images = st.columns(len(rotated_images))
            for i, rotated_img in enumerate(rotated_images):
                with col_rotated_images[i]:
                    st.image(rotated_img, caption=f"Page {i + 1}", use_column_width=True)

            output_pdf = io.BytesIO()

            rotated_images[0].save(output_pdf, format='PDF', save_all=True, append_images=rotated_images[1:])

            output_pdf.seek(0)
            st.download_button(
                label=f"Download {output_filename}",
                data=output_pdf.getvalue(),
                file_name=output_filename,
                mime="application/pdf"
            )

st.sidebar.markdown("""
    <div style='text-align: center; display: flex; flex-direction: column; gap: -100px;'>
        <p style='font-size: 1vw;'>Developed by Rayyan Ashraf</p>
        <p style='font-size: 1vw;'>Copyright @ 2024</p>
        <p style='font-size: 1vw;'>Developed in Python 3.12.5</p>
    </div>
""", unsafe_allow_html=True)