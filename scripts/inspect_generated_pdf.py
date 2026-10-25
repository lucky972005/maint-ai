import fitz

doc = fitz.open(r"C:\dev\pro\MaintAI_Reporting_4_Het_Joshi.pdf")
print("Total pages in generated PDF:", len(doc))

for i, page in enumerate(doc):
    text_sample = page.get_text("text").strip().replace("\n", " ")[:100]
    images = page.get_images()
    print(f"Page {i+1}: {len(images)} images, text: {text_sample}...")
