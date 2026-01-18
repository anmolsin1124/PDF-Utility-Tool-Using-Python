from pdf2image import convert_from_path
from PIL import Image
from PyPDF2 import PdfMerger
import os

def pdf_to_image():
    pdf_path = input("Enter pdf file pathe: ")

    file_exist = os.path.exists(pdf_path)
    if file_exist == False:
        print("File not fount")
        return

    images = convert_from_path(pdf_path)

    count = 1
    for img in images:
        name = "page_" + str(count) + ".jpg"
        img.save(name, "JPEG")
        count = count + 1

    print("Pdf converted into images succesfully")

def image_to_pdf():
    n = int(input("How many image you want convert into pdf: "))
    images = []

    i = 0
    while i < n:
        img_path = input("Enter image " + str(i+1) + " pathe: ")

        check = os.path.exists(img_path)
        if check == False:
            print("Image not fount")
            return

        img = Image.open(img_path)
        img = img.convert("RGB")
        images.append(img)

        i = i + 1

    output = input("Enter output pdf name (ex: output.pdf): ")

    first_img = images[0]
    other_img = []

    for j in range(1, len(images)):
        other_img.append(images[j])

    first_img.save(output, save_all=True, append_images=other_img)

    print("Images converted into pdf succesfully")

def merge_pdfs():
    merger = PdfMerger()
    n = int(input("How many pdf file you want to marge: "))

    pdf_list = []

    for i in range(n):
        pdf = input("Enter pdf " + str(i+1) + " pathe: ")
        if os.path.exists(pdf) == False:
            print("Pdf file not fount")
            return
        pdf_list.append(pdf)

    for p in pdf_list:
        merger.append(p)

    output = input("Enter merged pdf name (ex: merged.pdf): ")
    merger.write(output)
    merger.close()

    print("Pdf files marged succesfully")

while True:
    print("\n====== PDF UTILITY TOOl ======")
    print("1. Pdf to Image")
    print("2. Image to Pdf")
    print("3. Merge Pdf")
    print("4. Exit programe")

    choice = input("Enter your choise: ")

    if choice == "1":
        pdf_to_image()
    elif choice == "2":
        image_to_pdf()
    elif choice == "3":
        merge_pdfs()
    elif choice == "4":
        print("Programe exited")
        break
    else:
        print("Wrong choise try agian")

