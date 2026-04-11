def safe_float(val):
    if not val or str(val).strip().lower() in ["no", "yes", "none", ""]:
        return 0.0
    try:
        return float(val)
    except:
        return 0.0
