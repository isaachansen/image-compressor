# Image Compressor

A lightweight desktop application for compressing images locally. This tool allows you to reduce image file sizes while maintaining acceptable quality, all without requiring an internet connection.

## Features

- Support for multiple image formats (JPEG, PNG, BMP, etc.)
- Local processing - no server connection required
- Simple and intuitive user interface
- Adjustable compression settings
- Batch processing capability
- Cross-platform compatibility

## Requirements

- Python 3.8 or higher
- Dependencies listed in `requirements.txt`

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/image-compressor.git
cd image-compressor
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the application:
```bash
python src/main.py
```

## Development

This project uses:
- PyQt6 for the GUI
- Pillow (PIL) for image processing
- PyInstaller for creating standalone executables

## License

MIT License 