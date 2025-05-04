import pandas as pd 
class AuditLog:
    def __init__(self):
        self.logs = []
        self.row_errors = []  # For Phase 1 row-level error flags

    # Bulk action logging (e.g., "Dropped 5 duplicates")
    def log_action(self, action, rows_affected, reason="N/A"):
        self.logs.append({
            "action": action,
            "rows_affected": rows_affected,
            "reason": reason
        })
    
    # Row-level logging (for Phase 1 error highlights)
    def log_row_error(self, row_index, column, original_value, error_type):
        self.row_errors.append({
            "row": row_index,
            "column": column,
            "original_value": original_value,
            "error_type": error_type
        })

    def get_log_df(self):
        return pd.DataFrame(self.logs)
    
    def get_error_df(self):
        return pd.DataFrame(self.row_errors)