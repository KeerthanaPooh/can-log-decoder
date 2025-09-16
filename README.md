# 🚛 CAN Log Decoder (PGN → SPN)

A Streamlit web application to decode CAN log files into human-readable **PGN → SPN** parameters.  
The app supports `.log` and `.txt` CAN log files and outputs results in a table with an option to **download as Excel**.

---

## ✨ Features
- Upload CAN log files (`.log`, `.txt`)
- Extracts PGNs and decodes SPNs into physical values
- Displays results in an interactive table
- Download results as **Excel file**
- Works fully online (no CMD or setup required)

---

## 🚀 Live Demo
👉 [Click here to open the app](https://can-log-decoder-m4r4aqngstrdappr8suwxsb.streamlit.app)

---

## 🛠️ How to Run Locally (Optional for Developers)
If you want to run this app on your own machine:

```bash
# Clone the repo
git clone https://github.com/KeerthanaPooh/can-log-decoder.git
cd can-log-decoder

# Install dependencies
pip install -r requirements.txt

# Run Streamlit app
streamlit run app.py
