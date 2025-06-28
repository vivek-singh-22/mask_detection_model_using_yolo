import os
import xml.etree.ElementTree as ET
from PIL import Image

# Define paths
IMG_DIR = "data/images"
XML_DIR = "data/annotations"
LABEL_DIR = "data/labels"

os.makedirs(LABEL_DIR, exist_ok=True)

# Class mapping (Kaggle dataset includes this typo)
CLASS_MAP = {
    "with_mask": 0,
    "without_mask": 1,
    "mask_weared_incorrect": 2,
    "mask_weared_incorrec": 2  # handle the typo too
}

def convert(xml_path, img_path, label_path):
    tree = ET.parse(xml_path)
    root = tree.getroot()

    try:
        img = Image.open(img_path)
        img_w, img_h = img.size
    except Exception as e:
        print(f"Error opening image {img_path}: {e}")
        return

    with open(label_path, "w") as f:
        for obj in root.findall("object"):
            cls_name = obj.find("name").text
            if cls_name not in CLASS_MAP:
                continue
            cls_id = CLASS_MAP[cls_name]

            bbox = obj.find("bndbox")
            xmin = float(bbox.find("xmin").text)
            ymin = float(bbox.find("ymin").text)
            xmax = float(bbox.find("xmax").text)
            ymax = float(bbox.find("ymax").text)

            x_center = ((xmin + xmax) / 2) / img_w
            y_center = ((ymin + ymax) / 2) / img_h
            width = (xmax - xmin) / img_w
            height = (ymax - ymin) / img_h

            f.write(f"{cls_id} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}\n")

count = 0
for filename in os.listdir(XML_DIR):
    if not filename.endswith(".xml"):
        continue

    base = os.path.splitext(filename)[0]
    xml_path = os.path.join(XML_DIR, filename)
    img_path = os.path.join(IMG_DIR, base + ".png")  # Change if your images are .jpg
    label_path = os.path.join(LABEL_DIR, base + ".txt")

    if os.path.exists(img_path):
        convert(xml_path, img_path, label_path)
        count += 1
    else:
        print(f"Image not found for {filename}")

print(f" Converted {count} annotations to YOLO format.")
