# MegaWorker PDF

MegaWorker PDF is a desktop utility for converting image collections into PDF documents and compressing existing PDFs. It provides a focused CustomTkinter interface, progress feedback, operation history, and persistent user preferences.

## Features

- Convert PNG, JPG, and JPEG images from multiple folders into one PDF.
- Preserve folder selection order and naturally sort filenames.
- Choose between A4 output and original image dimensions.
- Review images before conversion and exclude individual files.
- Compress existing PDFs using low, medium, or high compression levels.
- Display separate conversion and compression histories.
- Select the interface language: English or Italian.
- Persist language and appearance preferences between sessions.
- Follow the system appearance by default, with Light and Dark alternatives.
- Run long PDF operations in the background while keeping the interface responsive.

## Requirements

- Windows, macOS, or Linux
- Python 3.11 or newer
- `Pillow`
- `PyPDF2`
- `customtkinter`

## Installation

Clone the repository and create a virtual environment:

```bash
git clone https://github.com/BrunazzoDev/MegaWorker-PDF.git
cd MegaWorker-PDF
python -m venv .venv
```

Activate the environment:

### Windows PowerShell

```powershell
.\.venv\Scripts\Activate.ps1
```

### macOS/Linux

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
python -m pip install --upgrade pip
python -m pip install customtkinter Pillow PyPDF2
```

## Run

```bash
python main.py
```

The application creates `Database/` and `History/` automatically when needed. User preferences are stored in `settings.json` beside `main.py`.

## Usage

### Convert images to PDF

1. Open **Convert Images to PDF**.
2. Select one or more folders.
3. Choose A4 or original quality.
4. Review the collected images and exclude any unwanted files.
5. Choose an output path and start the conversion.

### Compress a PDF

1. Open **Compress PDF**.
2. Select the source PDF.
3. Choose an output path different from the source.
4. Select a compression level and wait for completion.

### Preferences

The **Settings** tab contains the appearance theme, interface language, history management, and application version. Changes to the language and theme are saved automatically and restored at the next launch.

## Project Structure

```text
main.py                 Application entry point
Changelog.md            Release history
README.md               Project documentation
Database/               Default PDF output directory
History/                Conversion and compression history
settings.json           Persisted user preferences, created at runtime
```

## Version

Current version: **v1.2.5**

## License

MIT Licence.
