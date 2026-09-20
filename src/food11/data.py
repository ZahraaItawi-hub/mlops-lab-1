from pathlib import Path
from PIL import Image
import shutil

BASE_DIR = Path(__file__).resolve().parents[2]

RAW_DIR = BASE_DIR / "data" / "food11_raw"
PROCESSED_DIR = BASE_DIR / "data" / "food11_processed"
MINI_DIR = BASE_DIR / "data" / "food11_processed_mini"

CATEGORIES = {
    "0": "Bread",
    "1": "Dairy product",
    "2": "Dessert",
    "3": "Egg",
    "4": "Fried food",
    "5": "Meat",
    "6": "Noodles-Pasta",
    "7": "Rice",
    "8": "Seafood",
    "9": "Soup",
    "10": "Vegetable-Fruit",
}

SPLITS = ["training", "evaluation", "validation"]


def prepare_dataset(source_dir, target_dir, limit_per_category=None):
    if target_dir.exists():
        shutil.rmtree(target_dir)

    for split in SPLITS:
        split_dir = source_dir / split
        counts = {category: 0 for category in CATEGORIES.values()}

        for image_path in split_dir.iterdir():
            if not image_path.is_file():
                continue

            class_id = image_path.name.split("_")[0]

            if class_id not in CATEGORIES:
                continue

            category = CATEGORIES[class_id]

            if limit_per_category is not None:
                if counts[category] >= limit_per_category:
                    continue

            output_dir = target_dir / split / category
            output_dir.mkdir(parents=True, exist_ok=True)

            output_path = output_dir / image_path.name

            try:
                with Image.open(image_path) as img:
                    img = img.convert("RGB")
                    img = img.resize((128, 128))
                    img.save(output_path)

                counts[category] += 1

            except Exception as e:
                print(f"Could not process {image_path}: {e}")


print("Creating full processed dataset...")
prepare_dataset(RAW_DIR, PROCESSED_DIR)

print("Creating mini processed dataset...")
prepare_dataset(RAW_DIR, MINI_DIR, limit_per_category=100)

print("Done.")