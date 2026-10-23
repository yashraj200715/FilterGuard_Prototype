# FilterGuard Prototype

A small Streamlit dashboard for the FilterGuard hackathon concept.

## What it demonstrates
- Editable example sensor readings
- Transparent, rule-based warnings based on flow, pressure-drop and usage inputs
- A chart using simulated trend data
- Explanations for warnings and explicit limitations

## Important
This is a concept demo, not a certified water-quality test or a validated filter-life predictor. Thresholds are illustrative. TDS alone cannot establish that water is safe. Do not present simulated values as real measurements.

## Run it on Windows (HP laptop)

1. Install Python 3.10 or newer from https://www.python.org/downloads/ if you do not already have it. During setup, enable **Add Python to PATH**.
2. Extract this folder.
3. Open the folder in VS Code.
4. Open Terminal → New Terminal.
5. Create a virtual environment (recommended):

   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

   If PowerShell blocks activation, run this instead:

   ```powershell
   .\.venv\Scripts\python.exe -m pip install -r requirements.txt
   .\.venv\Scripts\python.exe -m streamlit run app.py
   ```

6. Install packages:

   ```powershell
   python -m pip install -r requirements.txt
   ```

7. Launch:

   ```powershell
   python -m streamlit run app.py
   ```

8. Streamlit will print a local URL, usually http://localhost:8501. Open it in your browser.

## Demo flow
1. Select **Manual inputs**.
2. Lower the flow rate and increase pressure drop.
3. Show how the status and explanation change.
4. Select **Simulated trend** to display an illustrative trend.
5. Explain that real sensor readings and calibration are the next step.

## Suggested next improvement
Connect an ESP32 and suitable flow/pressure sensors to a safe test rig, log timestamped readings, and compare the rules with observed filter condition. Only consider machine learning after collecting suitable labelled data.
