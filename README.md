# easydrop

Easily share files through AirDrop *without a Mac*

[![PyPI](https://img.shields.io/pypi/v/easydrop)](https://pypi.org/project/easydrop/)
[![Donate](https://img.shields.io/badge/Donate-PayPal-blue.svg?logo=paypal)](https://www.paypal.me/TheLastGimbus)

`easydrop` is a simple cli utility for quick and easy ~~sending~~/receiving files with AirDrop on ~~Windoza~~/Linux

// Strikethrough words are stuff that doesn't work yet tho I would really want it to

## Using
0. Make sure you have [everything required](#supported-hardware-and-platforms)
1. `pip install -U easydrop`
2. Receive files:
    ```bash
    $ easydrop receive
    sudo password:  # Password to manage network interfaces
    22:01:51 Hang tight! Disabling normal WiFi...  # easydrop will disable your normal network when running
    22:01:52 Starting OWL...
    22:01:54 OWL running!
    22:01:55 Starting HTTP server - press CTRL+C to stop...
    ^C22:01:59 Stopping OWL...
    22:01:59 Restarting network...  # ...but will bring it back up after it's done!
    Aborted!
    ```
3. Send files: not yet implemented :disappointed:

## Credits

This is a very simple wrapper around much much bigger work of guys @seemoo-lab - it uses [owl](https://github.com/seemoo-lab/owl) for low-level AirDrop network layer as well as [opendrop](https://github.com/seemoo-lab/opendrop) for some app level - HUGE shout-out for them for reverse enineering all of this!!!

## Supported hardware and platforms

As noted on [owl repo](https://github.com/seemoo-lab/owl/#requirements), you need WiFi card that supports *active* monitor mode - you can quickly check it by running:
```bash
$ iw list | grep "active monitor"
# You should see:
> 	Device supports active monitor (which will ACK incoming frames)
```
If you don't have it, then I'm sorry, but it probably won't work :disappointed:

For now, `easydrop` only works on Linux (amd64 arch) (`owl` itself works on MacOS too, but you already have AirDrop there :laugh:)

You will also need to install `libpcap`, `libev` and `libnl`:
- on Debian: `sudo apt install libpcap-dev libev-dev libnl-3-dev libnl-genl-3-dev libnl-route-3-dev`
- on Fedora: `sudo dnf install libpcap-devel libev-devel libnl3-devel`
- on other distros: idk, you can do it :muscle:

`owl` is already included in the package :wink:

// TODO: Include those dependencies in package


## TODO:
- [ ] Sending files - may require more work to also [advertise BLE beacons to wake up receivers](https://github.com/seemoo-lab/opendrop/issues/30)
- [ ] Windoza
- [ ] Include all lib* dependencies within package
