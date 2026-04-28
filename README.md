
# VerifyPad
<img width="420" height="595" alt="Really good zine" src="https://github.com/user-attachments/assets/c25e6422-f377-4141-9c7b-d6e0fb70b0fa" />

# About
Simple macropad for [Hack club fallout](https://fallout.hackclub.com/)

It uses a simple desktop app to check your email every 3 seconds and check for OTP codes/links. You press the left button to paste an OTP and the right button to paste a verification link. It uses a program you install on your computer to check your email and paste codes.

We decided to make it to save effort when pasting email codes because it can be very annoying and it's much easier to just press a button and have it done for you. 

we made it by just doing an hour of work each day until everything worked. joe did pcb and brad did code and case. joe still cant code :( he gonna learn tho :)

# Motivation
We were motivated to make this project because all the time it takes to open your email for a OTP adds up, and it would be really nice to click a button to get an OTP code. Also we got it done really quickly because we both set a 14 day streak goal and didn't want to lose it. We're really exited to put it together!

# Bill of Materials (BOM)

| Id | Name                   | Quantity | Price  |
|----|------------------------|----------|--------|
| 1  | [Cherry MX Clear - MX1A-C1NW](https://www.digikey.com/en/products/detail/cherry-americas-llc/MX1A-C1NW/280855)               | 2        | $2.85 each|
| 2  | [SparkFun Accessories Cherry MX Keycap - R2](https://www.digikey.com/en/products/detail/sparkfun-electronics/15305/10130914)                | 2        |$1.05 each |
| 3  |[ XIAO-RP2040-DIP](https://www.seeedstudio.com/XIAO-RP2040-v1-0-p-5026.html)        | 1        | $4.99  |
| 4  | [Waveshare 0.49 Display](https://www.waveshare.com/0.49inch-oled-module.htm) | 1        | $5.99  |
| 5  | [PCB](pcb/)                    | 1        | $3.12  |
| 6  | [3D printed parts](case/)       | ?        | $0.00  |
Total Cost: $21.90

# Design
### PCB
<img width="1723" height="902" alt="image" src="https://github.com/user-attachments/assets/13fb58f2-9a23-4402-b727-b04b0ce55b7a" />

### Assembly Video

below is an assembly video for the 3d printed files. you should solder the xiao and switches into their outlined spots, solder the screen on with wires and slot it into the lid, then flash the firmware.

[https://raw.githubusercontent.com/Broseph9972/Verifypad/main/media/assembly.mp4
](https://github.com/user-attachments/assets/6515c9df-35d1-4015-a47c-1bd419035557)

# Downloading Software
If you're on windows, use the installer in releases and it will automatically install the program, as well as adding it to path and creating a system task to run it on login.
If you're on another OS or the installer doesn't work (very likely) you can also clone the repo, go to the application folder, and run verifypad.py.
