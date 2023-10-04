import PyPDF2
import os
import asyncio
from PIL import Image
from reportlab.pdfgen import canvas
from redownloader import check_and_download
import json


def images_to_pdf(images, output_filename, title):
    failed = []
    c = canvas.Canvas(output_filename)
    
    for image_path in images:
        try:
            img = Image.open(image_path)
            img.verify()  # To check if the image is valid
            img = Image.open(image_path)  # Reopen since verify() closes the image
            width, height = img.size
            c.setPageSize((width, height))
            c.drawImage(image_path, 0, 0, width, height)
            c.showPage()
        except Exception as e:
            print(f"Error processing {image_path}: {e}")
            failed.append(image_path)
    c.save()
    print(f"Saved {output_filename} successfully.")
    with open('data/failed_images.json', 'r') as file:
        data = json.load(file)
    with open("data/failed_images.json", "w", encoding="utf-8") as f:
        json.dump(data + failed, f, indent=4)

def process_folder(folder_path, title):
    for volume in sorted(os.listdir(folder_path)):
        volume_path = os.path.join(folder_path, volume)
        if not os.path.isdir(volume_path):
            continue
        images = []
        for chapter in sorted(os.listdir(volume_path)):
            chapter_path = os.path.join(volume_path, chapter)
            if os.path.isdir(chapter_path):
                chapter_images = [os.path.join(chapter_path, img) for img in sorted(os.listdir(chapter_path)) if img.lower().endswith(('.png', '.jpg', '.jpeg'))]
                images.extend(chapter_images)
        if images:
            pdf_output = os.path.join(folder_path, f"{title} {volume}.pdf")
            images_to_pdf(images, pdf_output, title)

def get_image_paths(folder_path):
    image_extensions = ['.png', '.jpg', '.jpeg']
    image_paths = []

    for root, _, files in os.walk(folder_path):
        for file in files:
            if any(file.lower().endswith(ext) for ext in image_extensions):
                image_paths.append(os.path.join(root, file))

    return image_paths

if __name__ == "__main__":
    r1 = r"manga\a_yuri_story_about_a_girl_who_insists_its_impossible_for_two_girls_to_get_together_completely_falling_within_100_days\a_yuri_story_about_a_girl_who_insists_its_impossible_for_two_girls_to_get_together_completely_falling_within_100_days_ch69"
    r2 = r"manga\a_yuri_story_about_a_girl_who_insists_its_impossible_for_two_girls_to_get_together_completely_falling_within_100_days\a_yuri_story_about_a_girl_who_insists_its_impossible_for_two_girls_to_get_together_completely_falling_within_100_days_extra_watanare_crossover"
    images = get_image_paths(r1)    
    folder_path = r"manga\a_yuri_story_about_a_girl_who_insists_its_impossible_for_two_girls_to_get_together_completely_falling_within_100_days"
    images_to_pdf(images, os.path.join(folder_path, "ch69.pdf"))
    images = get_image_paths(r2)
    images_to_pdf(images, os.path.join(folder_path, "watanare crossover.pdf"))
