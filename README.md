# [whatsapp-python](https://pypi.org/project/whatsapp-python/)

![Made in Italy](https://img.shields.io/badge/made%20in-italy-008751.svg?style=flat-square)
[![Downloads](https://pepy.tech/badge/whatsapp-python)](https://pepy.tech/project/whatsapp-python)
[![Downloads](https://pepy.tech/badge/whatsapp-python/month)](https://pepy.tech/project/whatsapp-python)
[![Downloads](https://pepy.tech/badge/whatsapp-python/week)](https://pepy.tech/project/whatsapp-python)

Unofficial Python wrapper for the [WhatsApp Cloud API](https://developers.facebook.com/docs/whatsapp/cloud-api)
Forked from [Neurotech-HQ/heyoo](https://github.com/Neurotech-HQ/heyoo)

## ⚠️ WARNING ⚠️
Any version newer than 1.1.2 is incompatible with the original `heyoo` library! Be careful updating! Read the docs first!

You can ignore this warning if it's your first time using the library.

## Supported features

1. Sending messages
2. Marking messages as read
3. Sending Media (images, audio, video and documents)
4. Sending location
5. Sending interactive buttons
6. Sending template messages
7. Parsing messages and media received

## Switching from `Neurotech-HQ/heyoo`
Switching from heyoo to whatsapp-python doesn't require any change for versions up to 1.1.2: just uninstall the old, install the new and change the import name from `heyoo` to `whatsapp`.
For version which are GREATER THEN 1.1.2, messages have became objects, so you need to change your code to use the new methods.



## Documentation

The documentation is available under the [wiki section](https://github.com/filipporomani/whatsapp/wiki)


## Issues

If you are facing any issues or have any questions, please open an issue on the [GitHub repository](https://github.com/filipporomani/whatsapp/issues)

## Contributing

This is an opensource project published under the ```MIT License```. Please refer to the [LICENSE](LICENSE) file.

## References

1. [WhatsApp Cloud API official documentation](https://developers.facebook.com/docs/whatsapp/cloud-api/)
