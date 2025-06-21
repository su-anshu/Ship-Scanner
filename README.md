# 📱 Barcode Scanner Streamlit App

A complete desktop web application for barcode scanning with webcam integration, Excel file upload, and real-time validation.

## ✨ Features

- 📁 **Excel/CSV Upload**: Upload files with valid barcodes (first column)
- 📷 **Real-time Scanning**: Webcam-based barcode detection using pyzbar
- ✅ **Visual Feedback**: Green checkmarks for valid, red X for invalid barcodes
- 🔊 **Audio Feedback**: Success and failure sounds
- 📊 **Progress Tracking**: Real-time statistics and completion progress
- 📋 **Scan History**: Complete log with timestamps
- 📥 **Export Function**: Download scan results as CSV
- 🎯 **Duplicate Prevention**: Prevents scanning the same barcode twice

## 🚀 Installation & Setup

### 1. Install Python Dependencies

```bash
pip install streamlit streamlit-webrtc opencv-python pyzbar pandas openpyxl av numpy
```

Or use the requirements file:

```bash
pip install -r requirements.txt
```

### 2. Run the Application

```bash
streamlit run app.py
```

### 3. Open in Browser

The app will automatically open at `http://localhost:8501`

## 📋 Usage Instructions

### Step 1: Upload Barcode List
1. Click "Choose Excel or CSV file" in the sidebar
2. Upload your file with barcodes in the first column
3. Wait for confirmation message showing number of loaded barcodes

### Step 2: Start Scanning
1. Allow camera permissions when prompted by browser
2. Position barcodes in front of the camera
3. Wait for colored bounding boxes to appear around detected barcodes
4. Listen for audio feedback (success/failure sounds)

### Step 3: Monitor Progress
- Check the **Scan Status** panel for real-time feedback
- View **Statistics** showing progress percentage
- Review **Scan History** for complete log

### Step 4: Export Results
- Click "Export Scanned Barcodes" to download CSV
- Use "Clear Scan History" to reset and start over

## 🔧 Technical Requirements

- **Camera**: Webcam access required
- **Browser**: Chrome or Firefox recommended
- **Python**: 3.8+ with required packages
- **Network**: Internet connection for WebRTC functionality

## 📂 File Structure

```
barcode_scanner_app/
├── app.py                    # Main Streamlit application
├── requirements.txt          # Python dependencies
├── sample_barcodes.csv      # Example barcode file
└── README.md               # This file
```

## 🎛️ Configuration Options

### Scan Cooldown
- Default: 2 seconds between scans
- Modify `scan_cooldown` in `BarcodeProcessor` class

### Audio Settings
- Success/failure sounds are base64 encoded
- Replace sound data in `get_success_sound()` and `get_failure_sound()`

### Camera Settings
- Resolution and constraints can be modified in `webrtc_streamer`
- STUN server configuration available for different network setups

## 🐛 Troubleshooting

### Camera Not Working
- Ensure browser has camera permissions
- Try refreshing the page
- Check if camera is used by another application

### Barcode Not Detected
- Ensure good lighting conditions
- Hold barcode steady and at moderate distance
- Try different angles
- Check if barcode format is supported by pyzbar

### File Upload Issues
- Ensure file has barcodes in the first column
- Check file format (Excel .xlsx or CSV)
- Verify file is not corrupted

### Performance Issues
- Close other camera applications
- Use Chrome browser for best performance
- Reduce scan frequency if needed

## 📊 Supported Barcode Formats

The app supports all formats that pyzbar can decode:
- Code 128
- Code 39
- EAN-13/UPC-A
- EAN-8/UPC-E
- QR Code
- Data Matrix
- PDF417
- And more...

## 🔒 Privacy & Security

- All processing happens locally on your machine
- No data is sent to external servers
- Camera feed is processed in real-time only
- Uploaded files are processed in memory only

## 🆘 Support

For issues or questions:
1. Check the troubleshooting section above
2. Ensure all dependencies are correctly installed
3. Verify camera and browser compatibility
4. Check console logs for detailed error messages

---

**Made with ❤️ using Streamlit and OpenCV**