# Portable Document Format Manipulator : PDF-M

# Description
**PDF-Manipulator**, this `Streamlit-based` web application allows users to seamlessly manipulate PDF in various forms, including `Merging`, `Splitting`, `Watermarking`, `Encrypting & Decrypting`, `OCR - Text Extracting` and `Adding, Deleting & Rotating PDF Pages`. The application is designed to be **user-friendly**, **fast**, and **reliable**.

# Installation (Method 1)
1. Download `.zip` file for this project under `Code` option button on Repository Page
2. Extract the `.zip` file to your preferred location
3. Open any Integrated Development Environment IDE of your choice on extracted folder's location, i used `VS Code` as IDE
4. Install the neceesary libraries if not installed earlier, Use Command :
   ```bash
   pip install -r requirements.txt
   ```

   Or Update if already installed but not updated, Use Command :
   ```bash
   pip install --upgrade -r requirements.txt
   ```
# Installation (Method 2)
1. Open any Integrated Development Environment IDE of your choice on a location where you wish to store the project, i used `VS Code` as IDE
2. Clone this `.git` repository
   Use Command :
   ```bash
   git clone https://github.com/etsryn/PDF-Manipulator.git
   ```
3. Install the neceesary libraries if not installed earlier, Use Command :
   ```bash
   pip install -r requirements.txt
   ```

   Or Update if already installed but not updated, Use Command :
   ```bash
   pip install --upgrade -r requirements.txt
   ```

# Additional Requirement
### 1. Tesserect : Link Below (Open in any web-browser, then perform the following steps)
  ```bash
  https://github.com/UB-Mannheim/tesseract/wiki
  ```
**Step 1** : Under `The latest installers can be downloaded here:` click `tesseract-ocr-w64-setup-5.4.0.20240606.exe (64 bit)` (Version May Get Updated At Your Time)<br />

**Step 2** : Download will start, file is `47.9 MB` (Size May Get Increased/Decreased At Your Time)<br />

**Step 3** : Go to the location where `tesseract-ocr-w64-setup-5.4.0.20240606.exe (64 bit)` is downloaded, double click it<br />

**Step 4** : Get done with the Installation process through `Installation Wizard` (You may change the location of installation, preferred is keeping the same i,e; `C:\Program Files\Tesseract-OCR`)<br />

**Step 5** : Go to `C:\Program Files\Tesseract-OCR` or your installed location, and copy the path, that is `C:\Program Files\Tesseract-OCR\`<br />

**Step 6** : Press windows key, then search `Edit the system environment variables`, click enter<br />

**Step 7** : Click on `Environment Variables` on bottom right corner, click<br />

**Step 8** : In `System Variable` section click `path` then `Edit` then `New`<br />

**Step 9** : Paste the copied path, click `Ok`, `Ok` then `Ok`<br />

**Step 10** : Restart the IDE and run the python file `ftp.py`

### 2. PyTorch library and its associated packages (torch, torchvision, and torchaudio)
  #### Below Command is Recommended if you have an NVIDIA GPU and want to take advantage of GPU acceleration<br />
  Run Either This Command
  ```bash
  pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
  ```
  #### Below Command is Recommended if you don't have an NVIDIA GPU, or for tasks where GPU acceleration is not required
  Or Run This Command
  ```bash
  pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
  ```

# File Structure
📦 pdf-manipulator<br />
│<br />
├── 📜 pdfm.py&nbsp;&nbsp;&nbsp;&nbsp;=>&nbsp;&nbsp;&nbsp;&nbsp;Main Streamlit App file<br />
├── 📜 requirements.txt&nbsp;&nbsp;&nbsp;&nbsp;=>&nbsp;&nbsp;&nbsp;&nbsp;Python dependencies for the project<br />
├── 📜 README.md&nbsp;&nbsp;&nbsp;&nbsp;=>&nbsp;&nbsp;&nbsp;&nbsp;Project documentation (this file)<br />

# Usage
#### Since this project is a `streamlit`-based web application, so simply `py pdfm.py` won't help to execute this program, instead use
   ```bash
   streamlit run pdfm.py
```
## Features

- Feature 1 `Merging PDFs`
- Feature 2 `Splitting PDF`
- Feature 3 `Rearrange PDF Pages`
- Feature 4 `PDF Watermarking`
- Feature 5 `Adding & Deleting PDF Pages`
- Feature 6 `PDF Metadata Extractor`
- Feature 7 `PDF Metadata Editor`
- Feature 8 `Encrypting & Decrypting PDF`
- Feature 9 `OCR Text Extraction`
- Feature 10 `Rotate PDF Pages`
- More to come...

# Contributing
1. You can improve the design of UI which may look more professional and easy to use
2. You may add more functionality like PDF Visual Render Editing

# Changelog
1. Currently working on 2nd point of Contributing section.

# Conclusion
This program is currently executing with zero error, so you are good to go with it, **Thank You**

# License
Apache-2.0 license

# Contact me at
LinkedIn Account : www.linkedin.com/in/rayyan-ashraf-71117b249<br />
Instagram Account : @etsrayy<br />
Email At : ryshashraf@gmail.com
