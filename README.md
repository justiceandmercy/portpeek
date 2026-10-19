# portpeek

A tiny, zero-dependency CLI that peeks at the processes listening on TCP ports.
Useful when something is already bound to a port and you need to know who owns it.

## Features

- Lists every listening TCP port with its PID, user, command, and address.
- Filter by a single port: `portpeek 3000`.
- Machine-readable JSON output via `--json`.
- Optionally terminate matching processes with `--kill`.
- No third-party dependencies; uses the system `lsof`.

## Install

```sh
pip install .
```

Or run directly:

```sh
python3 portpeek.py
```

## Usage

```sh
# list all listening ports
portpeek

# inspect a specific port
portpeek 8000

# JSON output
portpeek --json

# terminate the process on port 3000
portpeek 3000 --kill
```

## Requirements

- Python 3.9+
- `lsof` available on PATH (standard on macOS and most Linux distributions)

## License

MIT
