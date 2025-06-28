import os
import shutil
import random

# Base directories
base_img_dir = "data/images"
base_lbl_dir = "data/labels"

# Target directories
splits = ['train', 'val', 'test']
for split in splits:
    os.makedirs(f"data/images/{split}", exist_ok=True)
    os.makedirs(f"data/labels/{split}", exist_ok=True)

# Get image filenames
image_files = [f for f in os.listdir(base_img_dir) if f.endswith((".png", ".jpg"))]
random.shuffle(image_files)

total = len(image_files)
train_split = int(0.8 * total)
val_split = int(0.9 * total)

# Copy files
for i, img_file in enumerate(image_files):
    base = os.path.splitext(img_file)[0]
    label_file = base + ".txt"
    
    if i < train_split:
        split = "train"
    elif i < val_split:
        split = "val"
    else:
        split = "test"

    shutil.copy(os.path.join(base_img_dir, img_file), f"data/images/{split}/{img_file}")
    shutil.copy(os.path.join(base_lbl_dir, label_file), f"data/labels/{split}/{label_file}")
