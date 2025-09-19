import streamlit as st
import pandas as pd
from io import BytesIO

# --- PGN → SPN mapping ---
PGN_MAP = {
    61444: [{"name": "Engine Speed", "spn": 190, "start": 4, "length": 2, "res": 0.125, "offset": 0, "unit": "rpm"}],
    65262: [
        {"name": "Engine Water Temp", "spn": 110, "start": 1, "length": 1, "res": 1, "offset": -40, "unit": "°C"},
        {"name": "Engine Oil Temp", "spn": 175, "start": 0, "length": 2, "res": 0.03125, "offset": -273, "unit": "°C"},
    ],
    65263: [{"name": "Engine Oil Pressure", "spn": 100, "start": 4, "length": 1, "res": 4, "offset": 0, "unit": "kPa"}],
    65271: [{"name": "Battery Voltage", "spn": 168, "start": 5, "length": 2, "res": 0.05, "offset": 0, "unit": "V"}],
    65276: [{"name": "Fuel Level", "spn": 96, "start": 2, "length": 1, "res": 0.4, "offset": 0, "unit": "%"}],
    65272: [{"name": "Transmission Oil Pressure", "spn": 127, "start": 2, "length": 2, "res": 16, "offset": 0, "unit": "kPa"}],
    64917: [{"name": "Converter Oil Temp", "spn": 3823, "start": 3, "length": 2, "res": 0.03125, "offset": -273, "unit": "°C"}],
    65253: [{"name": "Hour Meter", "spn": 247, "start": 2, "length": 3, "res": 0.05, "offset": 0, "unit": "hrs"}],
}

def extract_pgn(can_id_hex):
    can_id = int(can_id_hex, 16)
    return (can_id >> 8) & 0xFFFF

def decode_value(data_bytes, rule):
    start = rule["start"] - 1
    length = rule["length"]
    raw_slice = data_bytes[start:start+length]
    raw_hex = raw_slice.hex().upper()
    raw_dec = int.from_bytes(raw_slice, byteorder="little")
    phys_val = raw_dec * rule["res"] + rule["offset"]
    return raw_hex, str(raw_dec), f"{phys_val:.2f} {rule['unit']}"

def process_log_from_lines(lines):
    rows = []
    for line in lines:
        parts = line.strip().split()
        if len(parts) >= 11:
            can_id_hex = parts[0]
            try:
                pgn = extract_pgn(can_id_hex)
            except:
                continue
            if pgn in PGN_MAP:
                try:
                    data_bytes = bytes.fromhex("".join(parts[2:10]))
                except:
                    continue
                timestamp = parts[-1]
                for rule in PGN_MAP[pgn]:
                    raw_hex, raw_dec, final_val = decode_value(data_bytes, rule)
                    rows.append({
                        "CAN ID": can_id_hex,
                        "PGN (Hex)": f"{pgn:04X}",
                        "PGN (Dec)": str(pgn),
                        "Parameter": rule["name"],
                        "SPN": rule["spn"],
                        "Raw Data (Hex)": raw_hex,
                        "Raw Data (Dec)": raw_dec,
                        "Final Value": final_val,
                        "Timestamp": timestamp
                    })
    return pd.DataFrame(rows)

# --- Streamlit UI ---
st.title("🚛 CAN Log Decoder (PGN → SPN)")

uploaded_file = st.file_uploader("Upload CAN Log File", type=["log", "txt"])
pasted_text = st.text_area("Or paste CAN log content here")

df = None
if uploaded_file:
    lines = uploaded_file.getvalue().decode("utf-8-sig").splitlines()
    df = process_log_from_lines(lines)
elif pasted_text.strip():
    lines = pasted_text.splitlines()
    df = process_log_from_lines(lines)

if df is not None:
    if df.empty:
        st.warning("⚠️ No matching PGN/SPN data found.")
    else:
        st.success("✅ Processed successfully!")
        st.dataframe(df, use_container_width=True)

        # Excel download
        out_file = "decoded_output.xlsx"
        df.to_excel(out_file, index=False)
        with open(out_file, "rb") as f:
            st.download_button("📥 Download Excel", f, file_name="decoded_output.xlsx")
