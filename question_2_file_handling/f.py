import os
import logging
import csv
import statistics
from typing import Optional, List, Tuple
import pydicom
import numpy as np
import matplotlib.pyplot as plt

class FileProcessor:
    def __init__(self, base_path: str, log_file: str = "file_processor.log"):
        self.base_path = base_path
        os.makedirs(base_path, exist_ok=True)
        
        logging.basicConfig(
            filename=log_file, 
            level=logging.ERROR, 
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger()
    
    def list_folder_contents(self, folder_name: str, details: bool = False) -> None:
        folder_path = os.path.join(self.base_path, folder_name)
        if not os.path.exists(folder_path):
            self.logger.error(f"Folder not found: {folder_path}")
            print("Error: Folder not found.")
            return
        
        items = os.listdir(folder_path)
        print(f"Folder: {folder_path}")
        print(f"Number of elements: {len(items)}")
        
        for item in items:
            item_path = os.path.join(folder_path, item)
            if os.path.isfile(item_path):
                size = os.path.getsize(item_path) / (1024 * 1024)  # Convert to MB
                modified_time = os.path.getmtime(item_path)
                print(f"File: {item} ({size:.2f} MB, Last Modified: {modified_time})")
            elif os.path.isdir(item_path):
                modified_time = os.path.getmtime(item_path)
                print(f"Folder: {item} (Last Modified: {modified_time})")
    
    def read_csv(self, filename: str, report_path: Optional[str] = None, summary: bool = False) -> None:
        file_path = os.path.join(self.base_path, filename)
        if not os.path.isfile(file_path) or not filename.endswith(".csv"):
            self.logger.error(f"CSV file not found or invalid: {file_path}")
            print("Error: CSV file not found or invalid format.")
            return
        
        try:
            with open(file_path, newline='', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)
                headers = next(reader)
                rows = list(reader)
                print(f"Columns: {headers}")
                print(f"Rows: {len(rows)}")
                
                numeric_data = {}
                for col in range(len(headers)):
                    values = []
                    for row in rows:
                        try:
                            values.append(float(row[col]))
                        except ValueError:
                            pass  # Ignore non-numeric values
                    if values:
                        numeric_data[headers[col]] = values
                
                for col, values in numeric_data.items():
                    avg = statistics.mean(values)
                    std_dev = statistics.stdev(values)
                    print(f"{col}: Average = {avg:.2f}, Std Dev = {std_dev:.2f}")
                
                if report_path:
                    os.makedirs(report_path, exist_ok=True)
                    report_file = os.path.join(report_path, f"{filename}_summary.txt")
                    with open(report_file, "w") as f:
                        for col, values in numeric_data.items():
                            f.write(f"{col}: Average = {avg:.2f}, Std Dev = {std_dev:.2f}\n")
                    print(f"Saved summary report to {report_file}")
        except Exception as e:
            self.logger.error(f"Error reading CSV file {filename}: {str(e)}")
            print("Error processing CSV file.")
    
    def read_dicom(self, filename: str, tags: Optional[List[Tuple[int, int]]] = None, extract_image: bool = False) -> None:
        file_path = os.path.join(self.base_path, filename)
        if not os.path.isfile(file_path):
            self.logger.error(f"DICOM file not found: {file_path}")
            print("Error: DICOM file not found.")
            return
        
        try:
            dicom_data = pydicom.dcmread(file_path)
            print(f"Patient Name: {dicom_data.PatientName}")
            print(f"Study Date: {dicom_data.StudyDate}")
            print(f"Modality: {dicom_data.Modality}")
            
            if tags:
                for tag in tags:
                    try:
                        print(f"Tag {tag}: {dicom_data[tag]}")
                    except KeyError:
                        print(f"Tag {tag} not found in DICOM file.")
            
            if extract_image and hasattr(dicom_data, 'PixelData'):
                image_data = dicom_data.pixel_array
                plt.imshow(image_data, cmap='gray')
                image_filename = os.path.join(self.base_path, filename.replace(".dcm", ".png"))
                plt.imsave(image_filename, image_data, cmap='gray')
                print(f"Extracted image saved to {image_filename}")
        except Exception as e:
            self.logger.error(f"Error reading DICOM file {filename}: {str(e)}")
            print("Error processing DICOM file.")

# Example Usage:
if __name__ == "__main__":
    processor = FileProcessor(base_path="./data")
    processor.list_folder_contents(folder_name="test_folder", details=True)
    processor.read_csv(filename="sample-01-csv.csv", report_path="./reports", summary=True)
    processor.read_dicom(
        filename="sample-01-dicom.dcm", 
        tags=[(0x0010, 0x0010), (0x0008, 0x0060)], 
        extract_image=True
    )
