import pandas as pd

# Create sample barcode data
sample_barcodes = [
    "1234567890123",
    "9876543210987", 
    "4567890123456",
    "7890123456789",
    "2345678901234",
    "5678901234567",
    "8901234567890",
    "3456789012345",
    "6789012345678",
    "0123456789012",
    "ABC123XYZ789",
    "DEF456UVW012",
    "GHI789RST345",
    "JKL012PQR678",
    "MNO345LMN901"
]

# Create DataFrame
df = pd.DataFrame({'Barcode': sample_barcodes})

# Save to Excel
df.to_excel('./barcode_scanner_app/sample_barcodes.xlsx', index=False)
print("Sample Excel file created: sample_barcodes.xlsx")
