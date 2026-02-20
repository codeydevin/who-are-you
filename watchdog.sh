#!/bin/bash
# Watchdog - checks if Codex is alive and responsive
# Run via cron every 10 minutes
# If Codex is frozen (heartbeat stale >10 min) or dead, restart it

# === CONFIGURE THESE ===
WORKING_DIR="$HOME/autonomous-ai"
CODEX_BIN="$HOME/.local/bin/codex"
# === END CONFIG ===

HEARTBEAT="$WORKING_DIR/.heartbeat"
LOGFILE="$WORKING_DIR/watchdog.log"
WAKEUP_PROMPT="$WORKING_DIR/wakeup-prompt.md"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOGFILE"
}

# Check if any codex process is running
CODEX_PIDS=$(pgrep -f "$CODEX_BIN" | head -5)

if [ -z "$CODEX_PIDS" ]; then
    log "ALERT: No Codex process found. Starting fresh instance."

    export DISPLAY=:0
    cd "$WORKING_DIR"
    xterm -e "$CODEX_BIN exec --full-auto --model gpt-5.2-codex \"$(cat $WAKEUP_PROMPT)\"" &

    log "Started new Codex instance in xterm (PID: $!)"
    exit 0
fi

# Codex is running - check if heartbeat is fresh
if [ ! -f "$HEARTBEAT" ]; then
    log "WARNING: No heartbeat file found. Creating one. Will check again next run."
    touch "$HEARTBEAT"
    exit 0
fi

# Check heartbeat age (in seconds)
HEARTBEAT_AGE=$(( $(date +%s) - $(stat -c %Y "$HEARTBEAT") ))
MAX_AGE=600  # 10 minutes

if [ "$HEARTBEAT_AGE" -gt "$MAX_AGE" ]; then
    log "WARNING: Heartbeat is ${HEARTBEAT_AGE}s old (max ${MAX_AGE}s). Checking .codex logs..."

    # Secondary check: are .codex log files still being written to?
    CODEX_LOG_DIR="$HOME/.codex"
    NEWEST_CODEX_LOG=$(find "$CODEX_LOG_DIR" -name "*.jsonl" -o -name "*.log" 2>/dev/null | head -20 | xargs ls -t 2>/dev/null | head -1)

    if [ -n "$NEWEST_CODEX_LOG" ]; then
        CODEX_LOG_AGE=$(( $(date +%s) - $(stat -c %Y "$NEWEST_CODEX_LOG") ))
        log "  Newest .codex log: $NEWEST_CODEX_LOG (${CODEX_LOG_AGE}s old)"

        if [ "$CODEX_LOG_AGE" -lt "$MAX_AGE" ]; then
            log "  Codex is BUSY but alive (.codex logs still active). NOT killing."
            exit 0
        fi
        log "  .codex logs ALSO stale (${CODEX_LOG_AGE}s). Codex is truly frozen."
    else
        log "  No .codex logs found. Proceeding with kill."
    fi

    log "ALERT: Both heartbeat AND .codex logs are stale. Codex is frozen."
    log "Killing stale Codex processes: $CODEX_PIDS"

    for pid in $CODEX_PIDS; do
        kill "$pid" 2>/dev/null
        log "Killed PID $pid"
    done

    sleep 5

    for pid in $CODEX_PIDS; do
        kill -9 "$pid" 2>/dev/null
    done

    sleep 2

    export DISPLAY=:0
    cd "$WORKING_DIR"
    xterm -e "$CODEX_BIN exec --full-auto --model gpt-5.2-codex \"$(cat $WAKEUP_PROMPT)\"" &

    log "Started new Codex instance in xterm (PID: $!)"
else
    log "OK: Heartbeat is ${HEARTBEAT_AGE}s old. Codex is alive."
fi
