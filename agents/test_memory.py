from memory_agent import log_session, fetch_recent_sessions

if __name__ == "__main__":
    dummy_summary = "Clustered SKUs into 3 groups, used ARIMA, MAPE improved by 5%."
    log_session(dummy_summary)

    print("🧠 Recent Memory Sessions:")
    recent = fetch_recent_sessions()
    for ts, summary in recent:
        print(f"{ts}: {summary}")
