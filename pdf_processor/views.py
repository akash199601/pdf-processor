from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.conf import settings
import os
import PyPDF2
from PIL import Image
import io
from pdf2image import convert_from_path
from datetime import datetime

def home(request):
    return render(request, 'pdf_processor/home.html')


def merge_pdfs(request):
    if request.method == 'POST':
        try:
            pdf_files = request.FILES.getlist('pdfs')
            merger = PyPDF2.PdfMerger()
            
            for pdf in pdf_files:
                merger.append(io.BytesIO(pdf.read()))
            
            output = io.BytesIO()
            merger.write(output)
            merger.close()
            
            response = HttpResponse(output.getvalue(), content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename=merged_pdf.pdf'
            return response
            
        except Exception as e:
            messages.error(request, f'Error merging PDFs: {str(e)}')
            
    return render(request, 'pdf_processor/merge.html')

def split_pdf(request):
    if request.method == 'POST':
        try:
            pdf_file = request.FILES['pdf']
            pages = request.POST.get('pages', '').split(',')
            
            reader = PyPDF2.PdfReader(io.BytesIO(pdf_file.read()))
            writer = PyPDF2.PdfWriter()
            
            for page_num in pages:
                page_num = int(page_num.strip()) - 1
                if 0 <= page_num < len(reader.pages):
                    writer.add_page(reader.pages[page_num])
            
            output = io.BytesIO()
            writer.write(output)
            
            response = HttpResponse(output.getvalue(), content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename=split_pdf.pdf'
            return response
            
        except Exception as e:
            messages.error(request, f'Error splitting PDF: {str(e)}')
            
    return render(request, 'pdf_processor/split.html')

def compress_pdf(request):
    if request.method == 'POST':
        try:
            pdf_file = request.FILES['pdf']
            quality = int(request.POST.get('quality', 75))
            
            reader = PyPDF2.PdfReader(io.BytesIO(pdf_file.read()))
            writer = PyPDF2.PdfWriter()
            
            for page in reader.pages:
                writer.add_page(page)
                
            writer.add_metadata(reader.metadata)
            
            output = io.BytesIO()
            writer.write(output)
            
            response = HttpResponse(output.getvalue(), content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename=compressed_pdf.pdf'
            return response
            
        except Exception as e:
            messages.error(request, f'Error compressing PDF: {str(e)}')
            
    return render(request, 'pdf_processor/compress.html')

def extract_text(request):
    if request.method == 'POST':
        try:
            pdf_file = request.FILES['pdf']
            reader = PyPDF2.PdfReader(io.BytesIO(pdf_file.read()))
            text = ""
            
            for page in reader.pages:
                text += page.extract_text() + "\n\n"
                
            response = HttpResponse(text, content_type='text/plain')
            response['Content-Disposition'] = 'attachment; filename=extracted_text.txt'
            return response
            
        except Exception as e:
            messages.error(request, f'Error extracting text: {str(e)}')
            
    return render(request, 'pdf_processor/extract_text.html')

def extract_images(request):
    if request.method == 'POST':
        try:
            pdf_file = request.FILES['pdf']
            temp_path = os.path.join(settings.MEDIA_ROOT, 'temp.pdf')
            
            with open(temp_path, 'wb') as f:
                f.write(pdf_file.read())
            
            images = convert_from_path(temp_path)
            
            # Create a zip file containing all images
            zip_buffer = io.BytesIO()
            from zipfile import ZipFile
            
            with ZipFile(zip_buffer, 'w') as zip_file:
                for i, image in enumerate(images):
                    img_buffer = io.BytesIO()
                    image.save(img_buffer, format='PNG')
                    zip_file.writestr(f'page_{i+1}.png', img_buffer.getvalue())
            
            os.remove(temp_path)
            
            response = HttpResponse(zip_buffer.getvalue(), content_type='application/zip')
            response['Content-Disposition'] = 'attachment; filename=extracted_images.zip'
            return response
            
        except Exception as e:
            messages.error(request, f'Error extracting images: {str(e)}')
            
    return render(request, 'pdf_processor/extract_images.html')

def protect_pdf(request):
    if request.method == 'POST':
        try:
            pdf_file = request.FILES['pdf']
            password = request.POST.get('password')
            
            reader = PyPDF2.PdfReader(io.BytesIO(pdf_file.read()))
            writer = PyPDF2.PdfWriter()
            
            for page in reader.pages:
                writer.add_page(page)
                
            writer.encrypt(password)
            
            output = io.BytesIO()
            writer.write(output)
            
            response = HttpResponse(output.getvalue(), content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename=protected_pdf.pdf'
            return response
            
        except Exception as e:
            messages.error(request, f'Error protecting PDF: {str(e)}')
            
    return render(request, 'pdf_processor/protect.html')
