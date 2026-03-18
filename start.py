#!/usr/bin/env python3
import os
import sys
import tempfile
from pathlib import Path

# Read the original config
config_path = Path(__file__).parent / "config"
config_content = config_path.read_text()

# Get port from Railway environment, default to 5232
port = os.getenv("PORT", "5232")
users_path = str((Path(__file__).parent / "users").resolve())

# Update the hosts line to use the correct port
updated_config = ""
for line in config_content.split('\n'):
    if line.strip().startswith('hosts = '):
        updated_config += f"hosts = 0.0.0.0:{port}\n"
    elif line.strip().startswith('htpasswd_filename = '):
        updated_config += f"htpasswd_filename = {users_path}\n"
    else:
        updated_config += line + '\n'

# Write updated config temporarily
temp_config = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='_config')
temp_config.write(updated_config)
temp_config.close()

# Set environment variable to use this config
os.environ['RADICALE_CONFIG'] = temp_config.name

# Import and run Radicale
from radicale.__main__ import run

run()
