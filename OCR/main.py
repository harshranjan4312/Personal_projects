import shutil
import argparse
import sys
import os
import os.path
import filetype
import pytesseract
from PIL import Image
import cv2
import pytesseract as pt
from docx2pdf import convert as docx_to_pdf
from pdf2image import convert_from_path

from revised_preprocessing.inversion_01 import invert_image
from revised_preprocessing.resizing_02 import resize
from revised_preprocessing.binarization_03 import thresholding_image
from revised_preprocessing.morphological_operations_04 import closing
from revised_preprocessing.morphological_operations_04 import opening
from revised_preprocessing.connected_component_filtering_06 import connected_component_filtering


def move_input_file_to_images(src_path):
    if not os.path.isfile(src_path):
        raise FileNotFoundError("File not found or does not exist")
    ext = os.path.splitext(src_path)[1].lower()
    output_paths = []
    if ext in [".png", ".jpg", ".jpeg"]:
        dst = os.path.join("images", "page_1.png")
        shutil.copy(src_path, dst)
        output_paths.append(dst)
    elif ext == ".pdf":
        images = convert_from_path(src_path)
        for i, img in enumerate(images):
            path = os.path.join("images", f"page_{i+1}.png")
            img.save(path, "PNG")
            output_paths.append(path)
    elif ext == ".docx":
        temp_pdf = "temp_doc.pdf"
        docx_to_pdf(src_path, temp_pdf)
        images = convert_from_path(temp_pdf)
        os.remove(temp_pdf)
        for i, img in enumerate(images):
            path = os.path.join("images", f"page_{i+1}.png")
            img.save(path, "PNG")
            output_paths.append(path)
    else:
        raise ValueError("Unsupported file type")
    return output_paths


def complete_preprocessing_pipeline(image_path,binarization_threshold = 127, opening_kernel = 3, closing_kernel = 5, minimum_size = 10):
    resized_image = resize(image_path)
    thresholded_image = thresholding_image(resized_image, binarization_threshold)
    morph_open = opening(thresholded_image,opening_kernel)
    morph_close = closing(morph_open, closing_kernel)
    filtered_image = connected_component_filtering(morph_close, minimum_size)
    return filtered_image

def clear_output_folders():
    folders = ["images", "preprocessed_image", "output_text"]
    for folder in folders:
        if os.path.exists(folder):
            for f in os.listdir(folder):
                file_path = os.path.join(folder, f)
                if os.path.isfile(file_path):
                    os.remove(file_path)
def main():
    parser = argparse.ArgumentParser(description="OCR pipeline for images, PDFs, and Word documents.")
    parser.add_argument("input_file", help="Path to input file")
    parser.add_argument("--threshold", type=int, default=127, help="Binarization threshold (default: 127)")
    parser.add_argument("--open", type=int, default=3, help="Opening kernel size (default: 3)")
    parser.add_argument("--close", type=int, default=5, help="Closing kernel size (default: 5)")
    parser.add_argument("--minsize", type=int, default=10, help="Minimum connected component size (default: 10)")
    args = parser.parse_args()
    clear_output_folders()
    image_paths = move_input_file_to_images(args.input_file)
    with open("output_text/text_from_image.txt", "w") as out_file:
        for i, path in enumerate(image_paths):
            processed = complete_preprocessing_pipeline(path, binarization_threshold=args.threshold, opening_kernel=args.open, closing_kernel=args.close, minimum_size=args.minsize)
            out_img_path = f"preprocessed_image/page_{i+1}_processed.png"
            cv2.imwrite(out_img_path, processed)
            text = pt.image_to_string(Image.fromarray(processed))
            out_file.write(f"Page {i+1}: {text}\n")
    

if __name__ == "__main__":
    main()