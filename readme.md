# WDF Converter Desktop Application

## Features
- Cross-platform GUI (Windows, macOS, Linux)
- Dual directory selection with browse buttons
- Real-time progress bar and log display
- Drag and drop support for .wdf files/folders
- Automatic .tek file association
- Conversion failure list export
- User preference persistence

## Requirements
- Python 3.8+
- PyQt6
- renishawWiRE

## Installation
```bash
pip install -r requirements.txt
```

## Usage
1. Select input directory containing .wdf files
2. Select output directory for converted .txt files
3. Click "Start Conversion"
4. View progress and logs in real-time

## Error Handling
- Invalid WDF file detection
- Disk space warnings
- File permission errors
- Conversion interruption recovery

## Packaging
For macOS:
```bash
pyinstaller --windowed --onefile --icon=app.icns main.py
codesign --deep --force --verify --verbose --sign "Developer ID" ./dist/WDFConverter.app
```

For Windows:
```bash
pyinstaller --windowed --onefile --icon=app.ico main.py
```

## License
MIT License
