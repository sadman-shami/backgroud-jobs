#!/usr/bin/env bash

set -e

uv run fastapi dev &
BACKEND_PID=$!

pnpm --prefix frontend run dev &
FRONTEND_PID=$!

trap 'kill "$BACKEND_PID" "$FRONTEND_PID" 2>/dev/null' EXIT

wait -n "$BACKEND_PID" "$FRONTEND_PID"