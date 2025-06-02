import sys
import os
import shutil
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QSlider, QFileDialog, QProgressBar,
    QScrollArea, QFrame, QSizePolicy, QMessageBox, QGroupBox, QGridLayout
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QPixmap, QImage, QClipboard, QPalette, QColor, QFont, QLinearGradient, QGradient, QIcon
from image_processor import ImageProcessor
from PyQt6.QtCore import pyqtSignal

# Modern dark mode color scheme with purple accents
COLORS = {
    'background': '#0a0a0a',
    'surface': '#151515',
    'surface_hover': '#1a1a1a',
    'primary': '#ffffff',
    'secondary': '#a0a0a0',
    'accent': '#8b5cf6',  # Purple
    'accent_hover': '#7c3aed',
    'accent_glow': 'rgba(139, 92, 246, 0.15)',
    'border': '#2a2a2a',
    'border_hover': '#3a3a3a',
    'hover': '#1f1f1f',
    'success': '#8b5cf6',
    'error': '#ef4444',
    'text': '#ffffff',
    'text_secondary': '#a0a0a0',
    'shadow': 'rgba(0, 0, 0, 0.3)',
}

class ModernButton(QPushButton):
    def __init__(self, text, primary=False):
        super().__init__(text)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setMinimumHeight(40)
        self.setFont(QFont('Inter', 10, QFont.Weight.Medium))
        
        if primary:
            self.setStyleSheet(f"""
                QPushButton {{
                    background-color: {COLORS['accent']};
                    color: white;
                    border: none;
                    border-radius: 8px;
                    padding: 10px 20px;
                    font-weight: 500;
                }}
                QPushButton:hover {{
                    background-color: {COLORS['accent_hover']};
                }}
                QPushButton:pressed {{
                    background-color: {COLORS['accent_hover']};
                    padding-top: 12px;
                    padding-bottom: 8px;
                }}
                QPushButton:disabled {{
                    background-color: {COLORS['surface']};
                    color: {COLORS['text_secondary']};
                    border: 1px solid {COLORS['border']};
                }}
            """)
        else:
            self.setStyleSheet(f"""
                QPushButton {{
                    background-color: {COLORS['surface']};
                    color: {COLORS['text']};
                    border: 1px solid {COLORS['border']};
                    border-radius: 8px;
                    padding: 10px 20px;
                    font-weight: 500;
                }}
                QPushButton:hover {{
                    background-color: {COLORS['surface_hover']};
                    border-color: {COLORS['accent']};
                }}
                QPushButton:pressed {{
                    background-color: {COLORS['surface_hover']};
                    padding-top: 12px;
                    padding-bottom: 8px;
                }}
                QPushButton:disabled {{
                    background-color: {COLORS['surface']};
                    color: {COLORS['text_secondary']};
                    border-color: {COLORS['border']};
                }}
            """)

class ModernSlider(QSlider):
    def __init__(self):
        super().__init__(Qt.Orientation.Horizontal)
        self.setStyleSheet(f"""
            QSlider {{
                height: 24px;
            }}
            QSlider::groove:horizontal {{
                height: 2px;
                background: {COLORS['border']};
                margin: 11px 0;
            }}
            QSlider::handle:horizontal {{
                background: white;
                width: 16px;
                height: 16px;
                margin: -7px 0;
                border-radius: 8px;
            }}
            QSlider::sub-page:horizontal {{
                background: white;
            }}
        """)

class ModernLabel(QLabel):
    def __init__(self, text="", secondary=False):
        super().__init__(text)
        self.setFont(QFont('Inter', 10))
        if secondary:
            self.setStyleSheet(f"color: {COLORS['text_secondary']};")
        else:
            self.setStyleSheet(f"color: {COLORS['text']};")

class ModernGroupBox(QGroupBox):
    def __init__(self, title):
        super().__init__(title)
        self.setFont(QFont('Inter', 12, QFont.Weight.Medium))
        self.setStyleSheet(f"""
            QGroupBox {{
                background-color: {COLORS['surface']};
                border: 1px solid {COLORS['border']};
                border-radius: 12px;
                margin-top: 20px;
                padding: 20px;
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 20px;
                padding: 0 10px;
                color: {COLORS['text']};
                background-color: {COLORS['surface']};
            }}
        """)

class StatsFrame(QFrame):
    def __init__(self):
        super().__init__()
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['surface']};
                border: 1px solid {COLORS['border']};
                border-radius: 10px;
            }}
        """)
        
        # Main layout with proper margins
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(24, 24, 24, 24)
        self.layout.setSpacing(16)
        
        # Title
        self.title = ModernLabel("Compression Results")
        self.title.setFont(QFont('Inter', 13, QFont.Weight.Medium))
        self.layout.addWidget(self.title)
        
        # Stats container with proper expansion
        stats_widget = QWidget()
        stats_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        stats_layout = QVBoxLayout(stats_widget)
        stats_layout.setContentsMargins(0, 0, 0, 0)
        stats_layout.setSpacing(12)
        
        # Stats
        self.original_label = ModernLabel("Original Size: --")
        self.original_label.setFont(QFont('Inter', 12))
        self.original_label.setWordWrap(True)
        stats_layout.addWidget(self.original_label)
        
        self.compressed_label = ModernLabel("Compressed Size: --")
        self.compressed_label.setFont(QFont('Inter', 12))
        self.compressed_label.setWordWrap(True)
        stats_layout.addWidget(self.compressed_label)
        
        self.savings_label = ModernLabel("Space Saved: --")
        self.savings_label.setFont(QFont('Inter', 12))
        self.savings_label.setWordWrap(True)
        stats_layout.addWidget(self.savings_label)
        
        # Percentage with some spacing
        stats_layout.addSpacing(4)
        self.percentage_label = ModernLabel("Reduction: --")
        self.percentage_label.setFont(QFont('Inter', 14, QFont.Weight.Medium))
        self.percentage_label.setWordWrap(True)
        stats_layout.addWidget(self.percentage_label)
        
        self.layout.addWidget(stats_widget)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setStyleSheet(f"""
            QProgressBar {{
                border: 1px solid {COLORS['border']};
                border-radius: 6px;
                background-color: {COLORS['background']};
                height: 8px;
                margin-top: 12px;
            }}
            QProgressBar::chunk {{
                background-color: {COLORS['accent']};
                border-radius: 6px;
            }}
        """)
        self.layout.addWidget(self.progress_bar)
        
        # Set minimum width to prevent text cutoff
        self.setMinimumWidth(280)
        
    def update_stats(self, original_size: int, compressed_size: int):
        """Update the stats display with new values"""
        savings = original_size - compressed_size
        savings_percent = (savings / original_size) * 100
        
        # Update values with formatted sizes
        self.original_label.setText(f"Original Size: {self.format_size(original_size)}")
        self.compressed_label.setText(f"Compressed Size: {self.format_size(compressed_size)}")
        self.savings_label.setText(f"Space Saved: {self.format_size(savings)}")
        self.percentage_label.setText(f"Reduction: {savings_percent:.1f}%")
        
        # Color the percentage based on compression ratio
        if savings_percent >= 50:
            color = "#10b981"  # Green for good compression
        elif savings_percent >= 25:
            color = "#f59e0b"  # Orange for moderate compression
        else:
            color = "#ef4444"  # Red for poor compression
            
        self.percentage_label.setStyleSheet(f"color: {color};")
        
    @staticmethod
    def format_size(size_bytes: int) -> str:
        """Format size in bytes to human readable format"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024
        return f"{size_bytes:.1f} TB"

class ImagePreview(QLabel):
    def __init__(self, title="Image Preview"):
        super().__init__()
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setMinimumSize(350, 300)
        self.setStyleSheet(f"""
            QLabel {{
                background-color: {COLORS['background']};
                border: 2px dashed {COLORS['border']};
                border-radius: 12px;
                padding: 20px;
                color: {COLORS['text_secondary']};
            }}
        """)
        self.setText("No image selected")
        self.setFont(QFont('Inter', 10))
        self.set_title(title)
        
    def set_title(self, title):
        self.setToolTip(title)
        
    def set_image(self, image_path: str):
        pixmap = QPixmap(image_path)
        scaled_pixmap = pixmap.scaled(
            self.size(),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        self.setPixmap(scaled_pixmap)

class QualityPresets(QWidget):
    # Define signal as a class attribute
    valueChanged = pyqtSignal(int)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QHBoxLayout(self)
        self.layout.setSpacing(12)
        self.layout.setContentsMargins(0, 0, 0, 0)
        
        self.value = 85  # Default value
        
        # Define presets with their descriptions, ordered from worst to best quality
        self.presets = [
            (40, "Minimum", "Maximum compression, ~85-95% size reduction"),
            (60, "Low", "Significant compression, ~75-85% size reduction"),
            (75, "Medium", "Noticeable but acceptable quality loss, ~60-75% size reduction"),
            (85, "High", "Good balance, ~40-60% size reduction"),
            (100, "Maximum", "Best quality, minimal compression")
        ]
        
        # Create preset buttons
        for value, label, tooltip in self.presets:
            btn = QPushButton(label)
            btn.setToolTip(tooltip)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setProperty("value", value)
            btn.setCheckable(True)
            btn.clicked.connect(lambda checked, v=value: self.set_value(v))
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {COLORS['surface']};
                    color: {COLORS['text']};
                    border: 1px solid {COLORS['border']};
                    border-radius: 6px;
                    padding: 8px 16px;
                    font-size: 11px;
                    font-weight: 500;
                    min-width: 80px;
                }}
                QPushButton:hover {{
                    background-color: {COLORS['surface_hover']};
                    border-color: {COLORS['accent']};
                }}
                QPushButton:checked {{
                    background-color: {COLORS['accent']};
                    color: white;
                    border-color: {COLORS['accent']};
                }}
            """)
            self.layout.addWidget(btn)
            
        # Set initial state
        self.update_preset_state()
        
    def set_value(self, value):
        """Set the quality value and update the UI"""
        self.value = value
        self.valueChanged.emit(value)
        self.update_preset_state()
        
    def update_preset_state(self):
        """Update the checked state of preset buttons based on current value"""
        for i, (value, _, _) in enumerate(self.presets):
            btn = self.layout.itemAt(i).widget()
            btn.setChecked(value == self.value)

class ImageCompressorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.image_processor = ImageProcessor()
        self.current_image_path = None
        self.last_compressed_path = None
        
        self.setWindowTitle("Image Compressor")
        self.setMinimumSize(1200, 700)
        self.setup_style()
        
        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.main_layout = QHBoxLayout(central_widget)
        self.main_layout.setSpacing(30)
        self.main_layout.setContentsMargins(30, 30, 30, 30)
        
        self.setup_ui()
        self.setup_connections()
        
    def setup_style(self):
        """Set up the application style"""
        self.setStyleSheet(f"""
            QMainWindow {{
                background-color: {COLORS['background']};
            }}
            QWidget {{
                font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
            }}
            QProgressBar {{
                border: 1px solid {COLORS['border']};
                border-radius: 6px;
                text-align: center;
                background-color: {COLORS['surface']};
                height: 10px;
            }}
            QProgressBar::chunk {{
                background-color: {COLORS['accent']};
                border-radius: 6px;
            }}
            QScrollBar:vertical {{
                border: none;
                background: {COLORS['surface']};
                width: 10px;
                margin: 0px;
            }}
            QScrollBar::handle:vertical {{
                background: {COLORS['accent']};
                min-height: 20px;
                border-radius: 5px;
            }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                height: 0px;
            }}
            QScrollBar:horizontal {{
                border: none;
                background: {COLORS['surface']};
                height: 10px;
                margin: 0px;
            }}
            QScrollBar::handle:horizontal {{
                background: {COLORS['accent']};
                min-width: 20px;
                border-radius: 5px;
            }}
            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
                width: 0px;
            }}
        """)
        
    def setup_ui(self):
        """Set up the user interface components"""
        # Create left panel for original image
        left_panel = ModernGroupBox("Original Image")
        left_layout = QVBoxLayout(left_panel)
        left_layout.setSpacing(20)
        
        # Original image preview
        self.original_preview = ImagePreview("Original Image")
        left_layout.addWidget(self.original_preview)
        
        # Original image controls
        original_controls = QVBoxLayout()
        original_controls.setSpacing(15)
        
        # File selection button
        self.select_button = ModernButton("Select Image", primary=True)
        original_controls.addWidget(self.select_button)
        
        # Quality controls container
        quality_container = QFrame()
        quality_container.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['background']};
                border-radius: 8px;
                padding: 20px;
            }}
        """)
        quality_layout = QVBoxLayout(quality_container)
        quality_layout.setSpacing(16)
        
        # Quality header
        quality_header = QHBoxLayout()
        quality_label = ModernLabel("Quality:")
        quality_label.setFont(QFont('Inter', 11, QFont.Weight.Medium))
        quality_header.addWidget(quality_label)
        
        self.quality_label = ModernLabel("85%", secondary=True)
        self.quality_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        quality_header.addWidget(self.quality_label)
        quality_layout.addLayout(quality_header)
        
        # Add some vertical space
        quality_layout.addSpacing(8)
        
        # Quality presets
        self.quality_presets = QualityPresets()
        quality_layout.addWidget(self.quality_presets)
        
        original_controls.addWidget(quality_container)
        
        # Compress button
        self.compress_button = ModernButton("Compress", primary=True)
        self.compress_button.setEnabled(False)
        original_controls.addWidget(self.compress_button)
        
        left_layout.addLayout(original_controls)
        self.main_layout.addWidget(left_panel)
        
        # Create right panel for compressed image
        right_panel = ModernGroupBox("Compressed Image")
        right_layout = QVBoxLayout(right_panel)
        right_layout.setSpacing(20)
        
        # Compressed image preview
        self.compressed_preview = ImagePreview("Compressed Image")
        right_layout.addWidget(self.compressed_preview)
        
        # Compressed image controls
        compressed_controls = QVBoxLayout()
        compressed_controls.setSpacing(15)
        
        # Save and Copy buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(15)
        
        self.save_as_button = ModernButton("Save As...")
        self.save_as_button.setEnabled(False)
        button_layout.addWidget(self.save_as_button)
        
        self.copy_button = ModernButton("Copy to Clipboard")
        self.copy_button.setEnabled(False)
        button_layout.addWidget(self.copy_button)
        
        compressed_controls.addLayout(button_layout)
        
        # Stats frame
        self.stats_frame = StatsFrame()
        compressed_controls.addWidget(self.stats_frame)
        
        right_layout.addLayout(compressed_controls)
        self.main_layout.addWidget(right_panel)
        
    def setup_connections(self):
        """Set up signal/slot connections"""
        self.select_button.clicked.connect(self.select_image)
        self.quality_presets.valueChanged.connect(self.update_quality_label)
        self.compress_button.clicked.connect(self.compress_image)
        self.save_as_button.clicked.connect(self.save_compressed_image)
        self.copy_button.clicked.connect(self.copy_to_clipboard)
        
    def select_image(self):
        """Handle image selection"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Image",
            "",
            "Images (*.png *.jpg *.jpeg *.bmp *.webp)"
        )
        
        if file_path:
            if self.image_processor.is_supported_format(file_path):
                self.current_image_path = file_path
                self.original_preview.set_image(file_path)
                self.compressed_preview.setText("No compressed image yet")
                self.compress_button.setEnabled(True)
                # Reset action buttons
                self.save_as_button.setEnabled(False)
                self.copy_button.setEnabled(False)
                self.last_compressed_path = None
                self.update_status(f"Selected: {os.path.basename(file_path)}")
            else:
                self.update_status("Unsupported file format")
                
    def update_quality_label(self, value):
        """Update the quality label when selector changes"""
        self.quality_label.setText(f"{value}%")
        
    def update_status(self, message: str):
        """Update the status label"""
        self.stats_frame.title.setText(message)
        
    def compress_image(self):
        """Handle image compression"""
        if not self.current_image_path:
            return
            
        try:
            # Create output directory if it doesn't exist
            output_dir = os.path.join(os.path.dirname(self.current_image_path), "compressed")
            os.makedirs(output_dir, exist_ok=True)
            
            # Get output path
            filename = os.path.basename(self.current_image_path)
            output_path = os.path.join(output_dir, f"compressed_{filename}")
            
            # Show progress
            self.stats_frame.progress_bar.setVisible(True)
            self.stats_frame.progress_bar.setValue(0)
            
            # Compress image
            quality = self.quality_presets.value
            original_size, compressed_size = self.image_processor.compress_image(
                self.current_image_path,
                output_path,
                quality
            )
            
            # Store the compressed image path
            self.last_compressed_path = output_path
            
            # Update compressed preview
            self.compressed_preview.set_image(output_path)
            
            # Enable action buttons
            self.save_as_button.setEnabled(True)
            self.copy_button.setEnabled(True)
            
            # Update stats
            self.stats_frame.update_stats(original_size, compressed_size)
            
            # Update progress
            self.stats_frame.progress_bar.setValue(100)
            
        except Exception as e:
            self.stats_frame.title.setText("Error")
            self.stats_frame.percentage_label.setText(str(e))
            self.stats_frame.percentage_label.setStyleSheet(f"color: {COLORS['error']};")
            self.save_as_button.setEnabled(False)
            self.copy_button.setEnabled(False)
        finally:
            self.stats_frame.progress_bar.setVisible(False)
            
    def save_compressed_image(self):
        """Save the compressed image to a user-selected location"""
        if not self.last_compressed_path or not os.path.exists(self.last_compressed_path):
            QMessageBox.warning(self, "Error", "No compressed image available to save.")
            return

        # Get the default filename from the compressed image
        default_name = os.path.basename(self.last_compressed_path)
        
        # Open save dialog
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Compressed Image",
            default_name,
            "Images (*.jpg *.jpeg *.png *.webp)"
        )
        
        if file_path:
            try:
                # Copy the compressed image to the new location
                shutil.copy2(self.last_compressed_path, file_path)
                self.update_status(f"Image saved to: {file_path}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to save image: {str(e)}")

    def copy_to_clipboard(self):
        """Copy the compressed image to clipboard"""
        if not self.last_compressed_path or not os.path.exists(self.last_compressed_path):
            QMessageBox.warning(self, "Error", "No compressed image available to copy.")
            return

        try:
            # Load the image and copy to clipboard
            pixmap = QPixmap(self.last_compressed_path)
            if not pixmap.isNull():
                QApplication.clipboard().setPixmap(pixmap)
                self.update_status("Image copied to clipboard")
            else:
                raise Exception("Failed to load image")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to copy image: {str(e)}")

def main():
    app = QApplication(sys.argv)
    
    # Set application style
    app.setStyle('Fusion')
    
    # Set the application and window icon
    app.setWindowIcon(QIcon("src/icon.png"))
    window = ImageCompressorApp()
    window.setWindowIcon(QIcon("src/icon.png"))
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main() 