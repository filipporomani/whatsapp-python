# [whatsapp-python](https://pypi.org/project/whatsapp-python/)

![Made in Italy](https://img.shields.io/badge/made%20in-italy-008751.svg?style=flat-square)
[![Downloads](https://pepy.tech/badge/whatsapp-python)](https://pepy.tech/project/whatsapp-python)
[![Downloads](https://pepy.tech/badge/whatsapp-python/month)](https://pepy.tech/project/whatsapp-python)
[![Downloads](https://pepy.tech/badge/whatsapp-python/week)](https://pepy.tech/project/whatsapp-python)

Free, open-source Python wrapper for the [WhatsApp Cloud API](https://developers.facebook.com/docs/whatsapp/cloud-api)
Forked from [Neurotech-HQ/heyoo](https://github.com/Neurotech-HQ/heyoo)

## Supported features

1. Sending messages
2. Marking messages as read
3. Sending Media (images, audio, video and documents)
4. Sending location
5. Sending interactive buttons
6. Sending template messages
7. Parsing messages and media received

## Documentation

The documentation for the is available in the [**wiki**](https://github.com/filipporomani/whatsapp/wiki)

## Costs of the API

While using third-party API providers of the WhatsApp API may have some monthly fees, using the WhatsApp API provided directly by Facebook is way cheaper. 
The first 1000 chats created are free, then there is a pay-as-you-go fee that is paid for each conversation started.

All the prices are available in the [**WhatsApp API docs**](https://developers.facebook.com/docs/whatsapp/pricing)

## Switching from `Neurotech-HQ/heyoo`
Any version >1.1.2 is incompatible with the original `heyoo` library! Be careful updating! Read the docs first!
Any version <=1.1.2 is fully compatible with the original `heyoo` library and doesn't include any breaking change.
You can ignore this warning if it's your first time using the library.


Switching from heyoo to whatsapp-python doesn't require any change for versions up to 1.1.2: just uninstall the old, install the new and change the import name from `heyoo` to `whatsapp`.
For version which are GREATER THEN 1.1.2, messages have became objects, so you need to change your code to use the new methods.

Note: docs for version 1.1.2 are available in the [**dedicated wiki page**](https://github.com/filipporomani/whatsapp/wiki/v1.1.2)




## Issues

If you are facing any issues or have any questions, please open an issue on the [**GitHub repository**](https://github.com/filipporomani/whatsapp/issues)

## Contributing

This is an opensource project published under the ```MIT License```: [**LICENSE**](LICENSE).

## References

1. [WhatsApp Cloud API official documentation](https://developers.facebook.com/docs/whatsapp/cloud-api/)
