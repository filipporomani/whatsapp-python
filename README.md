# [whatsapp-python](https://pypi.org/project/whatsapp-python/)

![Made in Italy](https://img.shields.io/badge/made%20in-italy-008751.svg?style=flat-square)
[![Downloads](https://static.pepy.tech/personalized-badge/whatsapp-python?period=total&units=none&left_color=grey&right_color=blue&left_text=Downloads)](https://pepy.tech/project/whatsapp-python)
[![Downloads](https://pepy.tech/badge/whatsapp-python/month)](https://pepy.tech/project/whatsapp-python)
[![Downloads](https://pepy.tech/badge/whatsapp-python/week)](https://pepy.tech/project/whatsapp-python)

Free, open-source Python wrapper for the [WhatsApp Cloud API](https://developers.facebook.com/docs/whatsapp/cloud-api).

Forked from [Neurotech-HQ/heyoo](https://github.com/Neurotech-HQ/heyoo)

## Supported features

1. Listening to events (messages, media, etc.)
2. Sending messages
3. Marking messages as read
4. Sending Media (images, audio, video and documents)
5. Sending location
6. Sending interactive buttons
7. Sending template messages
8. Parsing messages and media received

## App events

Asynchronous app events are now available!

The docs are available in the [wiki](https://github.com/filipporomani/whatsapp/wiki/App-events)

Leave feedbacks/report issues freely on GitHub! I'll be glad to help you!


## Installation

To install the library you can either use pip (latest release version):

``pip install whatsapp-python``

or git (latest development version):

```bash
git clone https://github.com/filipporomani/whatsapp.git
cd whatsapp
python3 setup.py install
```

## Documentation

The documentation for the library is available under the [**wiki**](https://github.com/filipporomani/whatsapp/wiki) section on GitHub.

## Costs of the API

While using third-party API providers of the WhatsApp API may have some monthly fees, using the WhatsApp API provided directly by Facebook is way cheaper, even if the billing docs are pretty hard to understand.
The first 1000 chats created are free, then there is a pay-as-you-go fee that is paid for each conversation started.

**IMPORTANT**: it is now mandatory (at least it was for me) to add a credit card to the whatsapp account to use the service. I eventually got billed for using a non-test number (~1,20€), so be carefull using the API!

All the prices are available in the [**WhatsApp API docs**](https://developers.facebook.com/docs/whatsapp/pricing)

## Switching from `Neurotech-HQ/heyoo`
Any version >1.1.2 is incompatible with the original `heyoo` library! Be careful updating! Read the docs first!
Any version <=1.1.2 is fully compatible with the original `heyoo` library and doesn't include any breaking change..
You can ignore this warning if it's your first time using the library.


Switching from heyoo to whatsapp-python doesn't require any change for versions up to 1.1.2: just uninstall `heyoo`, install `whatsapp-python==1.1.2` and change the import name from `heyoo` to `whatsapp`.
For version which are GREATER THEN 1.1.2, messages have became objects, so you need to change your code to use the new methods.

**Note**: docs for version 1.1.2 are available in the [**dedicated wiki page**](https://github.com/filipporomani/whatsapp/wiki/v1.1.2).




## Issues

If you are facing any issues or have any questions, please open an issue on the [**GitHub repository**](https://github.com/filipporomani/whatsapp/issues)

## Contributing

This is an opensource project published under the ```MIT License```: [**LICENSE**](LICENSE).

## References

1. [WhatsApp Cloud API official documentation](https://developers.facebook.com/docs/whatsapp/cloud-api/)
