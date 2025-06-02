from PIL import Image
import os
from typing import Tuple, Optional

class ImageProcessor:
    def __init__(self):
        self.supported_formats = {'.jpg', '.jpeg', '.png', '.bmp', '.webp'}
    
    def is_supported_format(self, file_path: str) -> bool:
        """Check if the file format is supported"""
        ext = os.path.splitext(file_path.lower())[1]
        return ext in self.supported_formats
    
    def get_image_info(self, image_path: str) -> Tuple[int, int, str, int]:
        """Get image information (width, height, format, size)"""
        try:
            with Image.open(image_path) as img:
                width, height = img.size
                format = img.format
                size = os.path.getsize(image_path)
                return width, height, format, size
        except Exception as e:
            raise Exception(f"Error reading image: {str(e)}")
    
    def compress_image(self, 
                      input_path: str, 
                      output_path: str, 
                      quality: int = 85,
                      max_size: Optional[int] = None) -> Tuple[int, int]:
        """
        Compress an image and save it to the output path
        
        Args:
            input_path: Path to input image
            output_path: Path to save compressed image
            quality: Compression quality (1-100)
            max_size: Maximum file size in bytes (optional)
            
        Returns:
            Tuple of (original_size, compressed_size) in bytes
        """
        try:
            # Open and compress image
            with Image.open(input_path) as img:
                # Convert to RGB if necessary (for PNG with transparency)
                if img.mode in ('RGBA', 'LA') or (img.mode == 'P' and 'transparency' in img.info):
                    background = Image.new('RGB', img.size, (255, 255, 255))
                    background.paste(img, mask=img.split()[-1])
                    img = background
                
                # Save with compression
                img.save(output_path, 
                        quality=quality, 
                        optimize=True)
                
                # Get file sizes
                original_size = os.path.getsize(input_path)
                compressed_size = os.path.getsize(output_path)
                
                return original_size, compressed_size
                
        except Exception as e:
            raise Exception(f"Error compressing image: {str(e)}")
    
    def batch_compress(self, 
                      input_paths: list[str], 
                      output_dir: str,
                      quality: int = 85) -> list[Tuple[str, int, int]]:
        """
        Compress multiple images
        
        Args:
            input_paths: List of input image paths
            output_dir: Directory to save compressed images
            quality: Compression quality (1-100)
            
        Returns:
            List of tuples containing (filename, original_size, compressed_size)
        """
        results = []
        
        for input_path in input_paths:
            if not self.is_supported_format(input_path):
                continue
                
            filename = os.path.basename(input_path)
            output_path = os.path.join(output_dir, f"compressed_{filename}")
            
            try:
                orig_size, comp_size = self.compress_image(
                    input_path, output_path, quality
                )
                results.append((filename, orig_size, comp_size))
            except Exception as e:
                print(f"Error processing {filename}: {str(e)}")
                continue
        
        return results 