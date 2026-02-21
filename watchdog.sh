#!/bin/bash
# Watchdog - keeps one Codex loop alive and restarts it if frozen.
# Usage:
#   ./watchdog.sh         # single health-check pass
#   ./watchdog.sh --loop  # run checks continuously (recommended for service mode)

set -u

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKING_DIR="$SCRIPT_DIR"
CODEX_BIN="${CODEX_BIN:-$(command -v codex)}"

HEARTBEAT="$WORKING_DIR/.heartbeat"
LOGFILE="$WORKING_DIR/watchdog.log"
LOCKFILE="$WORKING_DIR/.watchdog.lock"
PIDFILE="$WORKING_DIR/.codex.pid"
WAKEUP_PROMPT="$WORKING_DIR/wakeup-prompt.md"
MAX_AGE="${MAX_AGE:-600}"                # heartbeat staleness threshold in seconds
WATCHDOG_INTERVAL="${WATCHDOG_INTERVAL:-300}"  # loop mode check interval (5 min cadence)
MODEL="${MODEL:-gpt-5.2-codex}"

log() {
    mkdir -p "$WORKING_DIR"
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOGFILE"
}

is_pid_running() {
    local pid="$1"
    [ -n "$pid" ] && kill -0 "$pid" 2>/dev/null
}

current_pid() {
    if [ -f "$PIDFILE" ]; then
        cat "$PIDFILE" 2>/dev/null
    fi
}

start_codex() {
    if [ -z "$CODEX_BIN" ]; then
        log "ERROR: codex binary not found in PATH."
        return 1
    fi
    if [ ! -f "$WAKEUP_PROMPT" ]; then
        log "ERROR: Missing wakeup prompt at $WAKEUP_PROMPT."
        return 1
    fi

    cd "$WORKING_DIR" || return 1
    nohup "$CODEX_BIN" exec --dangerously-bypass-approvals-and-sandbox --model "$MODEL" "$(cat "$WAKEUP_PROMPT")" >> "$LOGFILE" 2>&1 &
    echo "$!" > "$PIDFILE"
    log "Started new Codex instance (PID: $!)."
}

stop_codex() {
    local pid="$1"
    if ! is_pid_running "$pid"; then
        rm -f "$PIDFILE"
        return 0
    fi

    kill "$pid" 2>/dev/null || true
    sleep 5
    if is_pid_running "$pid"; then
        kill -9 "$pid" 2>/dev/null || true
    fi
    rm -f "$PIDFILE"
    log "Stopped stale Codex PID $pid."
}

run_once() {
    exec 9>"$LOCKFILE"
    if ! flock -n 9; then
        exit 0
    fi

    local pid
    pid="$(current_pid)"

    if ! is_pid_running "$pid"; then
        if [ -n "$pid" ]; then
            log "ALERT: PID file pointed to dead PID $pid."
        else
            log "ALERT: No Codex PID file found."
        fi
        start_codex
        return $?
    fi

    if [ ! -f "$HEARTBEAT" ]; then
        log "WARNING: No heartbeat file found. Creating one."
        touch "$HEARTBEAT"
        return 0
    fi

    local heartbeat_age
    heartbeat_age=$(( $(date +%s) - $(stat -c %Y "$HEARTBEAT") ))

    if [ "$heartbeat_age" -le "$MAX_AGE" ]; then
        log "OK: Heartbeat is ${heartbeat_age}s old. Codex is alive (PID $pid)."
        return 0
    fi

    log "WARNING: Heartbeat is ${heartbeat_age}s old (max ${MAX_AGE}s). Checking .codex logs..."
    local newest_codex_log=""
    newest_codex_log=$(find "$HOME/.codex" \( -name "*.jsonl" -o -name "*.log" \) -type f -print0 2>/dev/null | xargs -0 ls -t 2>/dev/null | head -1)

    if [ -n "$newest_codex_log" ]; then
        local codex_log_age
        codex_log_age=$(( $(date +%s) - $(stat -c %Y "$newest_codex_log") ))
        log "Newest .codex log: $newest_codex_log (${codex_log_age}s old)."
        if [ "$codex_log_age" -lt "$MAX_AGE" ]; then
            log "Codex appears busy but alive (.codex logs still active)."
            return 0
        fi
    else
        log "No .codex logs found."
    fi

    log "ALERT: Heartbeat and .codex logs are stale. Restarting PID $pid."
    stop_codex "$pid"
    start_codex
}

if [ "${1:-}" = "--loop" ]; then
    log "Starting watchdog loop (interval ${WATCHDOG_INTERVAL}s, max heartbeat age ${MAX_AGE}s)."
    while true; do
        run_once
        sleep "$WATCHDOG_INTERVAL"
    done
else
    run_once
fi
