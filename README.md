<div align="center">
  <img src="https://gist.githubusercontent.com/boywithkeyboard/e8dc5b1810bd29e1d70346ca11d7f09d/raw/7f7eeea482f5047e62944e54182aa26c89cc299a/whatsapp_python.svg" alt="logo" width="128px">
  <h1>whatsapp-python</h1>
  <p>Free, open-source Python wrapper for the <a href="https://developers.facebook.com/docs/whatsapp/cloud-api">WhatsApp Cloud API</a>.<br>Forked from <a href="https://github.com/Neurotech-HQ/heyoo">Neurotech-HQ/heyoo</a>.</p>
  <img src="https://img.shields.io/badge/made%20in-italy-008751.svg?style=flat-square" alt="Made in Italy">
  <a href="https://pepy.tech/project/whatsapp-python"><img src="https://static.pepy.tech/personalized-badge/whatsapp-python?period=total&units=none&left_color=grey&right_color=blue&left_text=Downloads" alt="Downloads"></a>
  <a href="https://pepy.tech/project/whatsapp-python"><img src="https://pepy.tech/badge/whatsapp-python/month" alt="Monthly Downloads"></a>
  <a href="https://pepy.tech/project/whatsapp-python"><img src="https://pepy.tech/badge/whatsapp-python/week" alt="Weekly Downloads"></a>
</div>

## Installation

To install the library you can either use pip (latest release version):

``pip install whatsapp-python``

You can also install the development GitHub version (always up to date):

```bash
git clone https://github.com/filipporomani/whatsapp.git
cd whatsapp
pip install .
```

If you want to use a local enviroment you can also use hatch:
  
```bash
git clone https://github.com/filipporomani/whatsapp.git
cd whatsapp
pip install hatch
hatch shell
```

Documentation is available in the [wiki section](https://github.com/filipporomani/whatsapp/wiki) on GitHub.

## Why choose this library?

The main reason why I decided to fork the original library is that it uses an old version of the API, it's missing many useful features and it's almost not mantained anymore.

In this fork I added app events (to listen to incoming messages) and implemented an easier way to send/receive messages and media by using the `Message` object.

I fixed some bugs and added many features, however the library still needs a lot of work to be done even if it's working and usable.

### Supported features:

- Listening to events (messages, media, etc.)
- Sending messages
- Marking messages as read
- Sending Media (images, audio, video and documents)
- Sending location
- Sending interactive buttons
- Sending template messages
- Parsing messages and media received

## Obtaining the WhatsApp API credentials

To use the WhatsApp API you need to create a Facebook Business account and a WhatsApp Business account.

> [!TIP]  
> To create an account, I recommend to follow [this video](https://youtu.be/d6lNxP2gadA).

## Pricing of the API

Whereas using third-party providers of the WhatsApp API can result in monthly fees, using the WhatsApp API[^1] offered directly by Facebook is much cheaper, even if the billing documentation is quite difficult to understand.

> [!CAUTION]  
> It is now mandatory to add a credit card to the WhatsApp account (at least for me) in order to use the service. I was even charged a fee for using a non-test phone number (~€1.20), so be careful when using the API! I'm not responsible for any costs you may face by using the API.

All the prices are available in the [**WhatsApp API docs**](https://developers.facebook.com/docs/whatsapp/pricing).

> [!TIP]  
> One recommendation I can give you is to use a test number (you can get a free phone number and use it for testing purposes only).

## Migrating from `Neurotech-HQ/heyoo`

*You can ignore this if it's your first time using the library.*

- Any version >1.1.2 is incompatible with the original `heyoo` library! Be careful updating! Read the docs first!
- Any version <=1.1.2 is fully compatible with the original `heyoo` library and doesn't include breaking changes.

Switching from heyoo to whatsapp-python doesn't require any change for versions up to 1.1.2: just uninstall `heyoo`, install `whatsapp-python==1.1.2` and change the import name from `heyoo` to `whatsapp`.

For versions GREATER THAN 1.1.2, messages have became objects, so you need to change your code to use the new methods.

> [!NOTE]  
> Documentation for version 1.1.2 can be found [here](https://github.com/filipporomani/whatsapp/wiki/v1.1.2).

## Contributing

If you are facing any issues or have any questions, please [open a new issue](https://github.com/filipporomani/whatsapp/issues/new/choose)!

*This is an open source project published under the [MIT License](LICENSE).*

[^1]: https://developers.facebook.com/docs/whatsapp/cloud-api
