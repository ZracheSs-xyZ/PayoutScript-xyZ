# PayoutScript-xyZ
- This script will make all the payouts for your Axie Infinity academy!


# Setup

## Previous version
- Windows : https://medium.com/@ZracheSs-xyZ/payoutscript-xyz-step-by-step-installation-instructions-239a9fd9c424
- MacOS : coming soon...

## Using encryption for sensitive data
The above link is still valid, however
If anyone can set their hands on your private keys, they can do whatever they want with your funds / axies.
Please prefer the encryption method describe below
For that you will need the cryptography package:

 ```bash
pip install -r requirements.txt
 ```

You can list the config possibility with the command:

 ```bash
python config.py --help
 ```

### New configuration

If you want to create a new configuration, juste launch the command:

 ```bash
python config.py --create
 ```

### To encrypt an existing configuration file

If you have already json file with the config information, you can convert it to an encrypted config.
You can delete your json file after that.

 ```bash
python config.py --convert_clear file_path <file_path>
 ```

### To add or delete scholars from your config

 ```bash
python config.py --add
 ```

 ```bash
python config.py --delete
 ```

### To display the current state of the config

 ```bash
python config.py --display
 ```

### Launching payouts

To launch the payouts using the encrypted config, no args should be provided:

 ```bash
python PayoutScript-xyZ.py
 ```

---

# Step-by-step help
1. Please join my Discord channel : https://discord.com/invite/837cCXPd48
2. DM our Head of IT for support

# Upcoming new features
- [x] Create a QR Code Bot : https://github.com/ZracheSs-xyZ/QrCodeBot-xyZ
- [x] Create a payout script : https://github.com/ZracheSs-xyZ/PayoutScript-xyZ
- [ ] So much more... If you have some nice idea, please DM me!

# Bug to fix
- Please tell me if you experience any bugs...

# Donations
With your donation, I will be able to keep working on this project and add new features. 
Thank you!

* There’s a built-in donation of 1% that you can easily modify by changing the value of FEE_PAYOUT_ADDRESS from 0.01 to 0.

* Ronin Wallet Address: ronin:a04d88fbd1cf579a83741ad6cd51748a4e2e2b6a
* Ethereum Wallet Address: 0x3C133521589daFa7213E5c98C74464a9577bEE01

# Help
If you need help with setup or you have any question, please reach out to me!

* Twitter: https://twitter.com/ZracheSs
* Discord: https://discord.com/invite/837cCXPd48

# License

The MIT License (MIT)

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
