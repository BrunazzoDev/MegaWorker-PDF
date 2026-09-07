# Changelog

## v1.2.5 - 2026-09-07

- Renamed the application to **MegaWorker PDF**.
- Updated the displayed application version to **v1.2.5**.
- Translated the complete user interface to English by default.
- Added Italian as an optional interface language.
- Added a persistent language selector in Settings.
- Changed the default appearance theme to `System`.
- Persisted language and theme preferences in `settings.json` between sessions.
- Fixed the Python environment and dependency setup for `PyPDF2`, `customtkinter`, and `Pillow`.
- Reworked background conversion and compression tasks so GUI updates run safely on the main thread.
- Added a queue-based progress and completion system for worker tasks.
- Made `Database` and `History` paths relative to the application file instead of the current working directory.
- Ensured temporary compression files are removed even when an error occurs.
- Added validation for empty PDFs, PDFs without pages, and attempts to overwrite the source PDF.
- Improved image resource handling by closing opened image files correctly.
- Fixed the initial window size so the complete interface is visible.
- Fixed the image preview workflow so the confirmation list refreshes after files are excluded.
- Made malformed or non-list history JSON safer to load.

## v1.1

1. **Settings tab**

   Added options to clear the application history, view the current version, and choose between the default dark theme and the new beta light theme.

2. **New notification bar**

   Added an interactive notification bar at the bottom of the Conversion and Settings tabs, removing the central dialog section from the UI.
   Added automatic scrolling animation for the conversion history.

3. **Advanced file selection**

   Added an image preview and exclusion window while reviewing files selected from each folder. Individual files can be removed before generating the final PDF.

## Hotfix #1 - v1.0.1

- Removed bugs that slowed down the generation of new PDFs in the Database.

## Major Release I - v1.0

1. **Automatic saving to the Database directory**

   Added automatic saving to the Database directory and the `ensure_database_directory()` function, which creates the directory when needed.
   The Database directory is suggested by default when saving a PDF, while users can still choose another location and filename.

2. **History functionality**

   Added a complete operation history system.
   Each conversion or compression is recorded with a timestamp, action type, and details.
   Both tabs show the history for their operation type, with the most recent entries displayed first.

3. **UI improvements**

   Increased the window height to accommodate the history section.
   Added emoji icons (📄 for conversion and 🔄 for compression) to improve readability.
   Reduced the height of the compression information section to balance it with the history area.

4. **Other optimizations**

   The application suggests a filename based on the first selected folder.
   Compressed PDFs are given a suggested output name containing `_compresso`.
   History is sorted chronologically and filtered by operation type in each tab.

## Major Update 1 - v0.2 [Test Features]

- Added a page for compressing existing PDFs.
- Added low PDF compression.
- Added medium PDF compression.
- Added high PDF compression.

## Minor Update 02 - v0.1.1

- Added a new CustomTkinter UI.
- Changed file collection to use folders instead of numeric ordering. *(This resolves many issues.)*
- Added a dark theme.
- Added a progress bar for PDF generation.

## Minor Update 01 - v0.1

- Added support for importing files from multiple folders.
- Added a new Tkinter UI.
- Added error windows.
- Removed the terminal script.
- Removed terminal input.