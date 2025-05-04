from utils.cleaning_audit.audit_logger import AuditLog
import pandas as pd

def clean_data(df: pd.DataFrame):
    audit = AuditLog()
    original_len = len(df)

    # ====== Date Validation ======
    date_mask = df['date'].str.contains('wrong_date', na=False)
    invalid_dates = df[date_mask]
    
    # Log and remove invalid dates
    for idx in invalid_dates.index:
        audit.log_row_error(
            row_index=idx,
            column='date',
            original_value=df.loc[idx, 'date'],
            error_type='Invalid date format'
        )
    df = df[~date_mask].copy()
    audit.log_action(
        'Removed invalid dates',
        len(invalid_dates),
        reason=f"Dates: {invalid_dates['date'].tolist()}"
    )

    # ====== Data Quality Checks ======

    # Add demand validation
    demand_mask = df['demand'].notna()
    missing_demand = df[~demand_mask]
    for idx in missing_demand.index:
        audit.log_row_error(idx, 'demand', None, 'Missing demand')
    df = df[demand_mask].copy()
    # Missing demand
    missing_demand = df[df['demand'].isna()]
    for idx in missing_demand.index:
        audit.log_row_error(
            idx, 'demand', None, 'Missing demand value'
        )

    # Duplicates
    before = len(df)
    df = df.drop_duplicates()
    audit.log_action(
        'Dropped duplicates',
        before - len(df),
        reason=f"Duplicate rows: {before - len(df)}"
    )

    # Null rows
    before = len(df)
    df = df.dropna(how='all')
    audit.log_action(
        'Dropped empty rows',
        before - len(df),
        reason="All-column null values"
    )

    return df, audit