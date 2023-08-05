# QR DOOR LOCK

Meant to use with:
- **Raspberry Pi** 4 (with relay shield and qr reader connected throught UART), (RTC (clock) for offline usage)

Using:
- Python 3 **client** (the Raspberry)
    - dependencies: `uuniot` (our library), `pyserial`, `validators`
- node.js **server**
    - dependencies: `ed25519`, `qrcode`

Overview
=======
- a server signs a generated qr code containing unique code and from + to timestamp using private key (ed25519)
- raspberry checks it using public key when reading and checks a time validity
- opens door based on check
- can be extended to multiple clients/doors/rooms
- contains components for communication with server
  - client sends **used codes**
  - monitor door state (opened/closed)
  - library functionality (configuration update & server heartbeat signalling online state to server)
## Limitations
- once a code is generated, it cannot be revoked (can't do 'rereservation'), unless a online delivered 'blacklist' is communicated (is not implemented, wouldn't work when offline)


#### Note

- all paths in this document are relative to PROJECT root, not system root


Client
=========

## General info

- **config file** is located in `/config.json`
- backup files (in offline mode) are located in `/backup/<module>.json`, but should not be necessary to access them directly

# Setting client up (Raspberry Pi)

- when setting a new client, these steps should be taken to reproduce the current setup

## Service persistence

- a systemd service was set up in order to achieve reliability, persistence and good system-wide emergency logging
- see library `ucliot` README for installation scripts for systemd persistence

## RTC clock

- Raspberry Pi does not have a backup baterry which could keep track of time during times when rpi is off (power surge, ...)

- an RTC module [DS1307](https://www.gme.cz/modul-rtc-ds1307-s-32k-flash?fbclid=IwAR11CYoBqdgsRHZJXuy6G6EZiVVMUnKZYVFmo5TeUu4nUxasl3dH7t-du_8#product-detail) was used with a battery

- voltage pins are connected as VCC -> +5V and GND -> GND on raspberry

- SDA and SCL are connected correspondingly on raspberry

- installation:

    ```shell
    # *unplug RTC module*
    
    cd ~
    git clone https://github.com/Seeed-Studio/pi-hats.git
    cd pi-hats/tools
    sudo ./install.sh rtc_ds1307
    sudo shutdown -h now
    
    # *connect RTC module and THEN start RPI* 
    cd ~/pi-hats/tools
    # check output to see if install was successful
    ./install.sh -l
    ```

- the module should be installed and from now on automatically sync time from RTC
- verify install without wifi/ethernet to see if time was set correctly (for example test time validity of qr codes)
- more info: [seedstudio](http://wiki.seeedstudio.com/Pi_RTC-DS1307/?fbclid=IwAR07fLFdaQ3mOgabdYLMQBzrJA35yiCBlmNHqxEwHSXNIVqSPz9P-PmzfVw)

## Debugging scripts

- read serial data from qr reader, send command to qr reader, try switching relay


## Hardware functionality 

- all functionality related to hardware (qr reader and relay control) is located in `hw.py` and is documented right in code with docstrings

