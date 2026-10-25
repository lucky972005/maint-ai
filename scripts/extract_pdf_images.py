import fitz
import os

doc = fitz.open(r"C:\Users\hetjo\Downloads\report3.pdf")
print("Page count:", len(doc))
os.makedirs("pdf_images", exist_ok=True)

img_count = 0
for page_index in range(len(doc)):
    page = doc[page_index]
    image_list = page.get_images(full=True)
    if image_list:
        print(f"Page {page_index+1} has {len(image_list)} images")
    for img_index, img in enumerate(image_list):
        xref = img[0]
        base_image = doc.extract_image(xref)
        image_bytes = base_image["image"]
        image_ext = base_image["ext"]
        img_name = f"pdf_images/p{page_index+1}_img{img_index}_{xref}.{image_ext}"
        with open(img_name, "wb") as f:
            f.write(image_bytes)
        img_count += 1
        print(f"  Saved {img_name}: {len(image_bytes)} bytes, dims: {base_image.get('width')}x{base_image.get('height')}")

print(f"Total images extracted: {img_count}")
