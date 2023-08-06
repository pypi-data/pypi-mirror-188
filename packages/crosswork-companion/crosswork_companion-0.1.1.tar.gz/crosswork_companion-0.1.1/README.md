# Crosswork Companion

Business Ready Documents for Cisco Crosswork

## Current API Coverage

Health Insights KPI Management Query

    pulse_cpu_utilization

    pulse_cpu_threshold

    pulse_cef_drops

    pulse_device_uptime

    pulse_ethernet_port_error_counters

    pulse_ethernet_port_packet_size_distribution

    pulse_interface_packet_counters

    pulse_interface_qos_egress

    pulse_interface_qos_ingress

    pulse_interface_rate_counters

    pulse_memory_utilization

NCA YANG Modules


## Installation

```console
$ python3 -m venv crosswork
$ source crosswork/bin/activate
(crosswork) $ pip install crosswork_companion
```

## Usage - Help

```console
(crosswork) $ crosswork_companion --help
```

![Help](/images/help.png)

## Usage - In-line

```console
(crossswork) $ crosswork_companion --url <url to Crosswork> --username <crosswork username> --password <crosswork password>
```

## Usage - Interactive

```console
(crosswork) $ crosswork_companion
Crosswork URL: <URL to Crosswork>
Crosswork Username: <Crosswork Username>
Crosswork Password: <Crosswork Password>
```

## Usage - Environment Variables

```console
(crosswork) $ export URL=<URL to Crosswork>
(crosswork) $ export USERNAME=<Crosswork Username>
(crosswork) $ export PASSWORD=<Crosswork Password>
```

## Recommended VS Code Extensions

Excel Viewer - CSV Files

Markdown Preview - Markdown Files

Markmap - Mindmap Files

Open in Default Browser - HTML Files

## Contact

Please contact John Capobianco if you need any assistance
