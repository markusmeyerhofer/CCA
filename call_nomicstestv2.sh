#!/bin/bash
while true; do
  sleep $((60 - $(date +%s) % 60))
  python3.9 nomicstesv2.py
done