import pandas as pd
import io

def load_ohlc_csv_robust(file_path: str) -> pd.DataFrame:
    """
    Robustly load OHLC data. Handles different separators (commas, spaces, tabs)
    and prevents date-parsing errors.
    """
    # 1. Load the data with separator auto-detection
    # 'sep=None' tells pandas to guess the separator (comma, tab, or space)
    try:
        data = pd.read_csv(file_path, sep=None, engine='python')
    except Exception as e:
        raise ValueError(f"Could not read the file: {e}")

    # 2. Cleanup column names
    data.columns = [str(c).strip() for c in data.columns]

    # 3. Identify the Date column
    date_col = None
    for col in data.columns:
        if "date" in col.lower() or "time" in col.lower():
            date_col = col
            break
    
    if not date_col:
        # Fallback: if columns are smashed, the first column usually contains the date
        date_col = data.columns[0]

    # 4. Parse Dates (Removed 'dayfirst=True' to support YYYY-MM-DD correctly)
    data[date_col] = pd.to_datetime(data[date_col], errors="coerce")
    
    # Check if parsing failed (smashed data detection)
    if data[date_col].isnull().all():
        raise ValueError("Error: Could not parse dates. Please ensure your CSV "
                         "columns are separated by commas or spaces.")

    # Drop rows with invalid dates and set index
    data = data.dropna(subset=[date_col])
    data.set_index(date_col, inplace=True)

    # 5. Standardize OHLC Columns
    required = ["Open", "High", "Low", "Close"]
    col_map = {}
    for req in required:
        for actual in data.columns:
            if req.lower() == actual.lower():
                col_map[actual] = req
    
    data.rename(columns=col_map, inplace=True)

    # 6. Final cleanup: Convert prices to numeric and sort
    for col in required:
        if col in data.columns:
            data[col] = pd.to_numeric(data[col], errors="coerce")
    
    data.dropna(subset=[c for c in required if c in data.columns], inplace=True)
    data.sort_index(inplace=True)

    return data
