# DDoS Mitigation Simulator

A Python-based firewall simulation that mitigates high-rate traffic floods using Token Bucket rate limiting, per-IP state tracking, temporary blocklisting, and escalation-based defense responses.

## Overview

This project simulates how a defensive security system responds to both normal and malicious network traffic. It tracks requests per IP address, applies rate limiting, and escalates responses from allowing traffic → rate limiting → blocking → temporary ban.

The system also triggers a critical alert when attack intensity exceeds a defined threshold.

## Features

- Token Bucket rate-limiting algorithm
- Per-IP state tracking using dictionaries
- Automated temporary blocklisting system
- Multi-level response system:
  - PASS (allowed traffic)
  - MITIGATED (rate-limited traffic)
  - BANNED (blocked IP traffic)
- Critical threshold-based alerting system
- Simulated normal and DDoS-style traffic patterns
- No external dependencies

## How It Works

1. Each IP address is assigned a token bucket.
2. Requests consume available tokens.
3. Tokens regenerate over time.
4. If tokens are unavailable, requests are rate-limited.
5. Repeated violations increase strike count.
6. After reaching a threshold, the IP is temporarily banned.
7. If total dropped requests exceed a limit, a critical alert is triggered.

## Technologies Used

- Python 3
- time module
- random module
- logging module
- dictionaries for state management

## Example Output

### Normal Traffic Phase
```
USER [192.168.x.x]: PASS
PASS: Request processed successfully.
BLOCK: Request rate limited
```

### Attack Simulation Phase
```
PASS: Flood request bypassed defense.
MITIGATED: Flood request dropped by rate limiter
BANNED: Flood request dropped automatically via Firewall Blocklist.
```

### Critical Alert
```
>>> [CRITICAL ALARM] Drop threshold breached! Total drops: 8 <<<
>>> IPS Engine executing automated infrastructure defense protocols <<<
```

## Getting Started

### Requirements
- Python 3

No external libraries required.

### Clone the Repository
```bash
git clone https://github.com/abraralhadi-alt/ddos-mitigation-tool.git
cd ddos-mitigation-tool
```

### Run the Tool
```bash
python ddos_mitigator.py
```

## Purpose

This project is intended for educational and defensive cybersecurity purposes. It demonstrates how modern systems use rate limiting, state tracking, and automated response mechanisms to mitigate denial-of-service attacks.

## Limitations

- Simulates network behavior only (does not interact with real networks)
- Uses predefined traffic patterns
- Intended for learning and demonstration purposes

## License

This project is licensed under the MIT License.
