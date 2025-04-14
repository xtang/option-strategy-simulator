# Options Strategy Simulator (Streamlit Version)

This project provides a web interface using Streamlit to simulate and plot the Profit/Loss (P/L) for various stock options hedging strategies against holding the underlying stock.

## Strategies Simulated

- Stock Only
- Protective Put
- Covered Call
- Collar

## Setup and Usage (using uv)

1.  **Install uv** (if you haven't already):
    See the official [uv installation guide](https://github.com/astral-sh/uv#installation).

2.  **Clone the Repository** (if you haven't already):
    ```bash
    # git clone <repository_url>
    # cd options_stock
    ```

3.  **Create and Activate Virtual Environment:**
    ```bash
    uv venv
    source .venv/bin/activate  # macOS/Linux
    # .venv\Scripts\activate.bat # Windows Cmd
    # .venv\Scripts\Activate.ps1 # Windows PowerShell
    ```

4.  **Install Dependencies:**
    ```bash
    uv pip install -r requirements.txt
    ```

5.  **Run the Streamlit Application:**
    ```bash
    streamlit run app_streamlit.py
    ```

6.  **Access the Application:**
    Streamlit will automatically open the application in your default web browser. If not, it will display the local URL (usually `http://localhost:8501`).

7.  **Use the Simulator:**
    *   Use the sidebar controls to adjust the stock details, options parameters, and simulation settings.
    *   The P/L plot in the main area will update automatically as you change the inputs.

## Files

- `app_streamlit.py`: The main Streamlit application script.
- `simulator.py`: Contains the core P/L calculation and plotting logic.
- `test.py`: The original script for command-line simulation (kept for reference).
- `pyproject.toml`: Project metadata and dependencies.
- `requirements.txt`: List of dependencies for `pip`.
- `.gitignore`: Standard Git ignore file for Python.
- `README.md`: This file.

(Optional: The files `main.py` and the `templates/` directory are from the previous FastAPI version and can be deleted if no longer needed.) 