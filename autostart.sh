#!/bin/bash
# Boc entrypoint goc cua CTFd: chay CTFd nen, doi no len roi tu seed challenge.
set -uo pipefail

# Khoi dong CTFd (entrypoint goc: flask db upgrade + gunicorn 0.0.0.0:8000)
/opt/CTFd/docker-entrypoint.sh &
CTFD_PID=$!

# Chuyen tiep tin hieu dung de CTFd tat muot
trap 'kill -TERM "$CTFD_PID" 2>/dev/null' TERM INT

# Tu seed (tat bang bien AUTOSEED=false neu khong muon)
if [ "${AUTOSEED:-true}" != "false" ]; then
    python /opt/seed/autoseed.py || echo "[autoseed] loi/bo qua, tiep tuc chay CTFd"
fi

# Giu CTFd lam tien trinh chinh
wait "$CTFD_PID"
