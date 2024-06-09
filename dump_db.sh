#!/bin/sh
pg_dump -U postgres -h db -d postgres -f /app/dumpfile
