"""
🔹 BARCODE SCANNER STREAMLIT APP
=====================================

INSTALLATION INSTRUCTIONS:
1. Install required packages:
   pip install streamlit streamlit-webrtc opencv-python pyzbar pandas openpyxl av

2. Run the app:
   streamlit run app.py

3. Open in browser (usually http://localhost:8501)

FEATURES:
- Upload Excel/CSV file with valid barcodes
- Real-time webcam barcode scanning
- Visual/audio feedback for matches
- Scan history with timestamps
- Export functionality

REQUIREMENTS:
- Webcam access (browser will prompt for permission)
- Modern browser (Chrome/Firefox recommended)
"""

import streamlit as st
import pandas as pd
import cv2
import numpy as np
from pyzbar import pyzbar
import base64
import io
from datetime import datetime
import time
from streamlit_webrtc import webrtc_streamer, WebRtcMode, RTCConfiguration
import av
from typing import Set, List, Dict, Optional
# Page configuration
st.set_page_config(
    page_title="Barcode Scanner App",
    page_icon="📱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
def initialize_session_state():
    """Initialize all session state variables"""
    if 'valid_barcodes' not in st.session_state:
        st.session_state.valid_barcodes = set()
    if 'scanned_barcodes' not in st.session_state:
        st.session_state.scanned_barcodes = []
    if 'last_scanned' not in st.session_state:
        st.session_state.last_scanned = None
    if 'scan_status' not in st.session_state:
        st.session_state.scan_status = None
    if 'file_uploaded' not in st.session_state:
        st.session_state.file_uploaded = False

# Audio functions
def get_success_sound():
    """Generate base64 encoded success sound (simple beep)"""
    # Simple success sound as base64
    return "data:audio/wav;base64,UklGRnoGAABXQVZFZm10IBAAAAABAAEAQB8AAEAfAAABAAgAZGF0YQoGAACBhYqFbF1fdJivrJBhNjVgodDbq2EcBj+a2/LDciUFLIHO8tiJNwgZaLvt559NEAxQp+PwtmMcBjiR1/LMeSwFJHfH8N2QQAoUXrTp66hVFApGn+DyvmsdCTGH0fPTgjMGHm7A7+OZSA0PVqzn77BdGAg+ltryxnkpBSl+zPLaizsIGGS57OihUgwLTKXh8bllHgg2jdXzzn0vBSF1xe/glEILElyx5+2qWBUIQ5zd8sFuIAUuhM/z2YU2Bhxqvu7mnEoODlOq5O+zYBoGPJPY88p9KwUme8rx3I4+CRZiturqpVITC0ml4PK8aB4GM4nU8tGAMQYfcsLu45ZFDBFYr+ftrVoXCECY3PLEcSEELIHO8tiJOQcZZ7zs4Z9NEAxPqOPwtmQcBjiS2fHNeSsFJHfH8N2QQAoUXrTp66hVFApGnt/yvmwdCTCG0fPTgzQGHW/A7eSaRw0PVqzl8LJeGQc9ltvyxnkpBSh+zPDaizsIGGS56+mjUgwLTKXh8bllHgg2jdT0z3wvBSJ0xe/glEILElyx5+2qWRUIQ5zd8sFuIAUug8/y2oU2Bhxqvu3mnEoPDlOq5O+zYRsGPJLZ8sp9KgUme8rx3I4+CRVht+vtpVMSC0mk4PK8aB4GMojU8tGAMQYfccPu45ZFDBFYruftrVwWCECY3PLEcSEGK4DN8tiIOQcZZ7vs4Z9OEAxOpePxtmQdBTiS2fHNeSsFJHbH8N2QQAoUXrPq66hWFAlFnt/yv2wdCTCG0fPTgzQHHG/A7eSaSQ0PVqrl8LJfGQc9ltvyxnkpBSh+zPDaizsIGGS56+mjUgwLTKXh8bllHgg2jdTy0H4wBiFzxu7glEQKElux5+2qWRUJQprd8sFuIAUug8/y2oU2Bhxqvu3mnEwODVKp5e+zYRsGOpPX8sp9KgUmecnw3Y9ACRVdt+vupl4SC0mk4PK8aB4GMojS89GAMgUfccLt45dGCxFYruftrV0XB0CY3PLEcSEGK4DN8tiIOQcZZ7vs4Z9OEAxOpePxtmQdBTiS2fHNeSsFJHbH8N2QQAoUXrPq66hWFAlFnt/yv2wdCTCG0fPTgzQHHG/A7eSaSQ0PVqrl8LJfGQc9ltvyxnkpBSh+zPDaizsIGGS56+mjUgwLTKXh8bllHgg2jdTy0H4wBiFzxu7glEQKElux5+2qWRUJQprd8sFuIAUug8/y2oU2Bhxqvu3mnEwODVKp5e+zYRsGOpPX8sp9KgUmecnw3Y9ACRVdt+vupl4SC0mk4PK8aB4GMojS89GAMgUfccLt45dGCxFYruftrV0XB0CY3PLEcSEGK4DN8tiIOQcZZ7vs4Z9OEAxOpePxtmQdBTiS2fHNeSsFJHbH8N2QQAoUXrPq66hWFAlFnt/yv2wdCTCG0fPTgzQHHW/A7eSaSQ0PVqrl8LJfGQc9ltvyxnkpBSh+zPDaizsIGGS56+mjUgwLTKXh8bllHgg2jdTy0H4wBiFzxu7glEQKElux5+2qWRUJQprd8sFuIAUug8/y2oU2Bhxqvu3mnEwODVKp5e+zYRsGOpPX8sp9KgUmecnw3Y9ACRVdt+vupl4TC0mk4PK8aB4GMojS89GAMgUfccLt45dGCxFYruftrV0XB0CY3PLEcSEGK4DN8tiIOQcZZ7vs4Z9OEAxOpePxtmQdBTiS2fHNeSsFJHbH8N2QQAoUXrPq66hWFAlFnt/yv2wdCTCG0fPTgzQHHW/A7eSaSQ0PVqnl8LJfGQc6lPvyxnkpBSh+zPDaizsIGGS56+mjUgwLTKXh8bllHgg2jdTy0H4wBiFzxu7glEQKElux5+2qWRUJQprd8sFuIAUug8/y2oU2Bhxqvu3mnEwODVKp5e+zYRsGOpPX8sp9KgUmecnw3Y9ACRVdt+vupl4TC0mk4PK8aB4GMojS89GAMgUfccLt45dGCxFYruftrV0XB0CY3PLEcSEGK4DN8tiIOQcZZ7vs4Z9OEAxOpePxtmQdBTiS2fHNeSsFJHbH8N2QQAoUXrPq66hWFAlFnt/yv2wdCTCG0fPTgzQHHW/A7eSaSQ0PVqrl8LJfGQc6ltvyxnkpBSh+zPDaizsIGGS56+mjUgwLTKXh8bllHgg2jdTy0H4wBiFzxu7glEQKElux5+2qWRUJQprd8sFuIAUug8/y2oU2Bhxqvu3mnEwODVKp5e+zYRsGOpPX8sp9KgUmecnw3Y9ACRVdt+vupl4TC0mk4PK8aB4GMojS89GAMgUfccLt45dGCxFYruftrV0X"

def get_failure_sound():
    """Generate base64 encoded failure sound"""
    return "data:audio/wav;base64,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"

def play_sound(sound_data: str):
    """Play sound using HTML audio element"""
    audio_html = f"""
    <audio autoplay>
        <source src="{sound_data}" type="audio/wav">
    </audio>
    """
    st.markdown(audio_html, unsafe_allow_html=True)

# File handling functions
def load_barcodes_from_file(uploaded_file) -> Set[str]:
    """Load barcodes from uploaded Excel or CSV file"""
    try:
        # Determine file type and read accordingly
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        elif uploaded_file.name.endswith(('.xlsx', '.xls')):
            df = pd.read_excel(uploaded_file)
        else:
            raise ValueError("Unsupported file format. Please upload CSV or Excel file.")
        
        # Get first column and convert to string set
        if df.empty:
            raise ValueError("The uploaded file is empty.")
        
        # Get first column values, remove NaN, and convert to strings
        first_column = df.iloc[:, 0].dropna().astype(str).str.strip()
        barcode_set = set(first_column.tolist())
        
        # Remove empty strings
        barcode_set.discard('')
        
        return barcode_set
        
    except Exception as e:
        st.error(f"Error reading file: {str(e)}")
        return set()

# Barcode scanning functions
def detect_barcodes(frame):
    """Detect and decode barcodes in the given frame"""
    barcodes = pyzbar.decode(frame)
    detected_codes = []
    
    for barcode in barcodes:
        # Extract barcode data and type
        barcode_data = barcode.data.decode('utf-8')
        barcode_type = barcode.type
        
        # Get barcode location
        (x, y, w, h) = barcode.rect
        
        detected_codes.append({
            'data': barcode_data,
            'type': barcode_type,
            'location': (x, y, w, h)
        })
    
    return detected_codes

def draw_barcode_box(frame, barcode_info, is_valid=False):
    """Draw bounding box around detected barcode"""
    x, y, w, h = barcode_info['location']
    
    # Choose color based on validity
    color = (0, 255, 0) if is_valid else (0, 0, 255)  # Green if valid, Red if invalid
    
    # Draw rectangle
    cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
    
    # Add text
    text = f"{barcode_info['data']} ({'✓' if is_valid else '✗'})"
    cv2.putText(frame, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
    
    return frame

# WebRTC callback class
class BarcodeProcessor:
    def __init__(self):
        self.last_scan_time = 0
        self.scan_cooldown = 2.0  # 2 seconds between scans
    
    def recv(self, frame):
        img = frame.to_ndarray(format="bgr24")
        
        # Only process every few frames to improve performance
        current_time = time.time()
        if current_time - self.last_scan_time > self.scan_cooldown:
            # Detect barcodes
            detected_barcodes = detect_barcodes(img)
            
            for barcode_info in detected_barcodes:
                barcode_data = barcode_info['data']
                
                # Check if barcode is valid
                if (barcode_data in st.session_state.valid_barcodes and 
                    barcode_data not in [scan['barcode'] for scan in st.session_state.scanned_barcodes]):
                    
                    # Valid and new barcode
                    st.session_state.scanned_barcodes.append({
                        'barcode': barcode_data,
                        'timestamp': datetime.now(),
                        'status': 'Valid'
                    })
                    st.session_state.scan_status = 'success'
                    st.session_state.last_scanned = barcode_data
                    self.last_scan_time = current_time
                    
                elif barcode_data in st.session_state.valid_barcodes:
                    # Already scanned
                    st.session_state.scan_status = 'duplicate'
                    st.session_state.last_scanned = barcode_data
                    self.last_scan_time = current_time
                    
                else:
                    # Invalid barcode
                    st.session_state.scan_status = 'invalid'
                    st.session_state.last_scanned = barcode_data
                    self.last_scan_time = current_time
                
                # Draw bounding box
                is_valid = barcode_data in st.session_state.valid_barcodes
                img = draw_barcode_box(img, barcode_info, is_valid)
        
        return av.VideoFrame.from_ndarray(img, format="bgr24")

# Main application
def main():
    # Initialize session state
    initialize_session_state()
    
    # Header
    st.title("📱 Barcode Scanner App")
    st.markdown("---")
    
    # Sidebar for file upload and controls
    with st.sidebar:
        st.header("📁 Upload Barcode List")
        
        uploaded_file = st.file_uploader(
            "Choose Excel or CSV file",
            type=['xlsx', 'xls', 'csv'],
            help="Upload a file with barcodes in the first column"
        )
        
        if uploaded_file is not None:
            with st.spinner("Loading barcodes..."):
                valid_barcodes = load_barcodes_from_file(uploaded_file)
                
            if valid_barcodes:
                st.session_state.valid_barcodes = valid_barcodes
                st.session_state.file_uploaded = True
                st.success(f"✅ Loaded {len(valid_barcodes)} valid barcodes!")
                
                # Show first few barcodes as preview
                with st.expander("Preview loaded barcodes"):
                    preview_list = list(valid_barcodes)[:10]
                    for i, barcode in enumerate(preview_list, 1):
                        st.text(f"{i}. {barcode}")
                    if len(valid_barcodes) > 10:
                        st.text(f"... and {len(valid_barcodes) - 10} more")
        
        st.markdown("---")
        
        # Controls
        st.header("🎛️ Controls")
        
        if st.button("🗑️ Clear Scan History", type="secondary"):
            st.session_state.scanned_barcodes = []
            st.session_state.scan_status = None
            st.session_state.last_scanned = None
            st.success("History cleared!")
        
        # Export functionality
        if st.session_state.scanned_barcodes:
            if st.button("📥 Export Scanned Barcodes", type="secondary"):
                df_export = pd.DataFrame(st.session_state.scanned_barcodes)
                csv = df_export.to_csv(index=False)
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name=f"scanned_barcodes_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("📷 Camera Scanner")
        
        if not st.session_state.file_uploaded:
            st.warning("⚠️ Please upload a barcode list first!")
            st.info("👈 Use the sidebar to upload your Excel or CSV file with valid barcodes.")
        else:
            # WebRTC streamer for camera
            webrtc_ctx = webrtc_streamer(
                key="barcode-scanner",
                mode=WebRtcMode.SENDRECV,
                rtc_configuration=RTCConfiguration(
                    {"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}
                ),
                video_processor_factory=BarcodeProcessor,
                media_stream_constraints={"video": True, "audio": False},
                async_processing=True,
            )
            
            st.info("💡 **Tips:**")
            st.markdown("""
            - Hold barcode steady in camera view
            - Ensure good lighting
            - Keep barcode at moderate distance
            - Wait for green/red indicator after scan
            """)
    
    with col2:
        st.header("📊 Scan Status")
        
        # Status display
        status_placeholder = st.empty()
        
        # Handle scan status
        if st.session_state.scan_status == 'success':
            with status_placeholder.container():
                st.success(f"✅ Valid Barcode Scanned!")
                st.code(st.session_state.last_scanned)
                st.balloons()
                # Play success sound
                play_sound(get_success_sound())
            # Reset status after showing
            st.session_state.scan_status = None
            
        elif st.session_state.scan_status == 'invalid':
            with status_placeholder.container():
                st.error(f"❌ Invalid Barcode!")
                st.code(st.session_state.last_scanned)
                # Play failure sound
                play_sound(get_failure_sound())
            # Reset status after showing
            st.session_state.scan_status = None
            
        elif st.session_state.scan_status == 'duplicate':
            with status_placeholder.container():
                st.warning(f"⚠️ Already Scanned!")
                st.code(st.session_state.last_scanned)
            # Reset status after showing
            st.session_state.scan_status = None
        
        # Statistics
        if st.session_state.file_uploaded:
            st.markdown("### 📈 Statistics")
            total_valid = len(st.session_state.valid_barcodes)
            total_scanned = len(st.session_state.scanned_barcodes)
            progress = (total_scanned / total_valid) * 100 if total_valid > 0 else 0
            
            st.metric("Total Valid Barcodes", total_valid)
            st.metric("Scanned", total_scanned)
            st.metric("Progress", f"{progress:.1f}%")
            
            # Progress bar
            st.progress(progress / 100)
    
    # Scan History Section
    st.markdown("---")
    st.header("📋 Scan History")
    
    if st.session_state.scanned_barcodes:
        # Create DataFrame for display
        df_history = pd.DataFrame(st.session_state.scanned_barcodes)
        df_history['timestamp'] = df_history['timestamp'].dt.strftime('%Y-%m-%d %H:%M:%S')
        
        # Display as table
        st.dataframe(
            df_history[['timestamp', 'barcode', 'status']],
            column_config={
                'timestamp': 'Scan Time',
                'barcode': 'Barcode',
                'status': 'Status'
            },
            use_container_width=True,
            hide_index=True
        )
        
        # Summary by status
        col1, col2, col3 = st.columns(3)
        with col1:
            valid_count = len([s for s in st.session_state.scanned_barcodes if s['status'] == 'Valid'])
            st.metric("✅ Valid Scans", valid_count)
        
        with col2:
            # Show remaining barcodes
            remaining = len(st.session_state.valid_barcodes) - len(st.session_state.scanned_barcodes)
            st.metric("📋 Remaining", remaining)
        
        with col3:
            # Show completion percentage
            completion = (len(st.session_state.scanned_barcodes) / len(st.session_state.valid_barcodes)) * 100 if st.session_state.valid_barcodes else 0
            st.metric("📊 Completion", f"{completion:.1f}%")
    
    else:
        st.info("📝 No barcodes scanned yet. Start scanning to see history here!")
        
        # Show some helpful information
        if st.session_state.file_uploaded:
            st.markdown("### 💡 Quick Start Guide")
            st.markdown("""
            1. **Position your barcode** in front of the camera
            2. **Wait for detection** - you'll see a colored box around valid barcodes
            3. **Listen for audio feedback** - success/failure sounds will play
            4. **Check the status panel** - see real-time scan results
            5. **Monitor progress** - track your scanning completion
            """)

if __name__ == "__main__":
    main()
