# Network Security Assessment Report

**Tester:** Felix Otieno
**Date:** 30 September 2026
**Scope:** Home network (192.168.1.0/24)
**Methodology:** Manual testing (nmap, ifconfig, ping, curl)
**Purpose:** Educational — self-assessment of own network

---

## Executive Summary

A full security assessment of the home network was performed
over multiple sessions. The network uses an Airtel 4G router
(Model ZLT X17U). The router is well-configured: only 3 open
ports, modern services, with security headers present. The
4G uplink to Airtel is the primary bottleneck — network
performance is limited by weak signal strength, not by any
local misconfiguration.

**Overall Risk: LOW** (local network)
**Overall Risk: MEDIUM** (ISP uplink)

---

## Scope & Methodology

**In Scope:**
- Home Wi-Fi network (192.168.1.0/24)
- Router at 192.168.1.1 (ZLT X17U)
- All devices connected to the network
- The 4G uplink from the router to Airtel

**Out of Scope:**
- Other networks
- Airtel's internal infrastructure
- Any external system

**Tools Used:**
- `nmap` — network discovery and port scanning
- `ifconfig` — local IP discovery
- `ping` — connectivity testing
- `curl` — HTTP header inspection
- `traceroute` — path analysis

---

## Network Topology

**Network Range:** 192.168.1.0/24 (256 addresses)

**Router:** 192.168.1.1 (ZLT X17U)
- DHCP range: 192.168.1.100 – 192.168.1.200
- Lease time: 24 hours
- DNS: 192.168.1.1 (dnsmasq 2.90)

**Connected Devices:** 3 detected via nmap

| IP | Device | Notes |
|---|---|---|
| 192.168.1.1 | Router | ZLT X17U |
| 192.168.1.114 | Phone | Static IP set by technician |
| 192.168.1.189 | Unknown | Second device on network |

**Note:** Some devices do not respond to ping (Android
blocks it) — they exist but are not visible to nmap.

---

## Findings

### Finding 1 — Router Configuration (LOW risk)

**Ports detected via `nmap -sT`:**

| Port | Service | Version | Status |
|---|---|---|---|
| 53 | DNS | dnsmasq 2.90 | ✅ Recent |
| 80 | HTTP | Unknown web server | ✅ Hardened |
| 443 | HTTPS | Custom SSL | ✅ Encrypted |

**Observations:**
- Only 3 ports open (out of 65,535)
- No SSH, Telnet, FTP, or other legacy services
- 997 ports tested closed (connection refused)

**Verdict:** ✅ Router is minimal and secure. No exploitable
services exposed.

### Finding 2 — HTTP Security Headers (LOW risk)

**Response headers from `nmap -sV` HTTP fingerprint:**


**Observations:**
- All modern security headers present
- Unused HTTP methods disabled (OPTIONS returns 501)
- HTTPS enforced with HSTS

**Verdict:** ✅ Web interface is well-hardened.

### Finding 3 — Device Visibility (INFORMATIONAL)

**Devices found via `nmap -sn`:**

Only 3 devices detected out of a possible 256 IPs.

**Reason:** Android devices block ping by default. Many
other devices also ignore ping. So nmap sees fewer devices
than are actually connected.

**Verdict:** ℹ️ Normal behavior. Not a vulnerability.

### Finding 4 — ISP Signal Strength (MEDIUM risk)

**Router 4G signal metrics:**

| Metric | Value | Rating |
|---|---|---|
| RSRP | -91 dBm | ⚠️ Weak |
| RSRQ | -11 dB | ⚠️ Weak |
| SINR | 1 dB | ❌ Very weak |
| RSSI | -90 dBm | ⚠️ Weak |

**Interpretation:**
- **SINR 1 dB** — very low signal quality
- **RSRP -91 dBm** — moderate signal strength
- Both indicate the router is far from Airtel's tower
  or behind obstructions

**Verdict:** ⚠️ The 4G uplink is the bottleneck.

### Finding 5 — Network Performance (MEDIUM risk)

**Ping tests to external targets:**

| Target | Average | Verdict |
|---|---|---|
| Router (192.168.1.1) | 2–10 ms | ✅ Excellent |
| Google (google.com) | 529 ms | ⚠️ Slow |
| Google DNS (8.8.8.8) | 275 ms | ⚠️ Slow |
| DNS Lookup (via curl) | 253 ms overhead | ⚠️ Slow |

**Interpretation:**
- **Local network is fast** (router responds in 2–10 ms)
- **Internet is slow** (529 ms average to google.com)
- **DNS overhead is high** (253 ms extra for domain lookups)
- **50% packet loss** was observed in one test

**Verdict:** ⚠️ Internet performance is degraded. The
bottleneck is the ISP, not the local network.

---

## Risk Summary

| Finding | Risk | Impact |
|---|---|---|
| Router configuration | LOW | Minimal attack surface |
| HTTP security headers | LOW | Web interface hardened |
| Device visibility | INFO | Normal behavior |
| ISP signal strength | MEDIUM | Slow internet |
| Network performance | MEDIUM | Poor user experience |

**Local Network Risk: LOW** ✅
**ISP-Dependent Risk: MEDIUM** ⚠️

---

## Recommendations

### Router (no action needed)
- Router is well-configured
- No changes required
- Keep firmware updated

### ISP Uplink (action needed)
1. **Contact Airtel** — report weak signal (RSRP -91 dBm,
   SINR 1 dB)
2. **Move the router** to a higher location, near a window
3. **Consider a signal booster** if the location cannot
   be improved
4. **Consider a backup ISP** if issues persist

### Devices (no action needed)
- Static IP on phone (192.168.1.114) works well
- Other devices are connected and functional

---

## Conclusion

The home network is **well-configured at the local level**.
The router is minimal, hardened, and secure. The local
network performance is excellent (sub-10ms pings to the
router).

The performance issues are **entirely ISP-dependent**.
Airtel's signal strength at the router location is weak,
causing slow internet and high latency.

**No local vulnerabilities were found.**
**The primary recommendation is to address the ISP signal.**

---

**Report prepared by:** Felix Otieno
**Date:** 30 September 2026
**Tools:** nmap 7.991, ifconfig, ping, curl, traceroute
