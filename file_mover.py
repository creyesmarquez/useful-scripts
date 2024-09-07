import shutil
import time
from pathlib import Path
from tqdm import tqdm
import argparse
from tools.logger import setup_logger

# Set up logger
logger = setup_logger()

def move_folder_contents(src_folder, dest_folder, dry_run=False):
    """
    Move contents from the source folder to the destination folder.

    Parameters:
    src_folder (str): Source folder path
    dest_folder (str): Destination folder path
    dry_run (bool): If True, only simulate the move without performing actual file operations
    """
    # Convert to Path objects for cleaner cross-platform compatibility
    src_folder = Path(src_folder)
    dest_folder = Path(dest_folder)

    # Ensure the source folder exists
    if not src_folder.exists() or not src_folder.is_dir():
        logger.error(f"Source folder {src_folder} does not exist or is not a directory.")
        return

    # Ensure the destination folder exists
    try:
        dest_folder.mkdir(parents=True, exist_ok=True)
    except OSError as e:
        logger.error(f"Error creating destination folder {dest_folder}: {e}")
        return

    # Check if source folder is empty
    if not any(src_folder.iterdir()):
        logger.warning(f"🚨 Source folder {src_folder} is empty. No items to move.")
        return

    # Get total items for progress tracking
    total_items = sum(1 for _ in src_folder.iterdir())
    
    # Iterate over all files and folders in the source folder with progress bar
    with tqdm(total=total_items, desc="Moving files", unit="file") as pbar:
        for item in src_folder.iterdir():
            src_path = item
            dest_path = dest_folder / item.name

            try:
                if dry_run:
                    logger.info(f"Simulating move of {src_path} to {dest_path}")
                else:
                    logger.info(f"Moving {src_path} to {dest_path}... 🚚 ")
                    shutil.move(str(src_path), str(dest_path))

                pbar.update(1)  # Update progress bar
                time.sleep(0.05)  # Optional delay for smoother progress bar update

            except OSError as e:
                logger.error(f"Error moving {item.name}: {e}")

    if dry_run:
        logger.info(f"ℹ️ Dry run completed. No files were moved.")
    else:
        logger.info(f"✅ Completed moving items from {src_folder} to {dest_folder}!")

if __name__ == "__main__":
    # Set up command-line argument parser
    parser = argparse.ArgumentParser(description="Move contents from a source folder to a destination folder.")
    parser.add_argument("src_folder", type=str, help="Source folder path")
    parser.add_argument("dest_folder", type=str, help="Destination folder path")
    parser.add_argument("--dry-run", action="store_true", help="Simulate the move without actually moving files")

    # Parse the command-line arguments
    args = parser.parse_args()

    # Call the move_folder_contents function with the provided arguments
    move_folder_contents(args.src_folder, args.dest_folder, args.dry_run)
