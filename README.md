# [whatsapp-python](https://pypi.org/project/whatsapp-python/)

![Made in Italy](https://img.shields.io/badge/made%20in-italy-008751.svg?style=flat-square)
[![Downloads](https://pepy.tech/badge/whatsapp-python)](https://pepy.tech/project/whatsapp-python)
[![Downloads](https://pepy.tech/badge/whatsapp-python/month)](https://pepy.tech/project/whatsapp-python)
[![Downloads](https://pepy.tech/badge/whatsapp-python/week)](https://pepy.tech/project/whatsapp-python)

Unofficial Python wrapper for the [WhatsApp Cloud API](https://developers.facebook.com/docs/whatsapp/cloud-api)
Forked from [Neurotech-HQ/whatsapp](https://github.com/Neurotech-HQ/heyoo)


## Supported features

1. Sending messages
2. Marking messages as read
3. Sending Media (images, audio, video and documents)
4. Sending location
5. Sending interactive buttons
6. Sending template messages
7. Parsing messages and media received

## Switching from `heyoo`
As of now (v1.1.2), switching from heyoo to whatsapp-python doesn't require any change: just uninstall the old, install the new and change the import name from `heyoo` to `whatsapp`.

## Getting started

To get started with **whatsapp-python**, you have to firstly install the libary either directly or using *pip*.

### Installing from source - always up to date

```bash
$ git clone https://github.com/filipporomani/whatsapp
$ cd whatsapp
$ python setup.py install
```

### Installing from pip - stable version

```bash
# For Windows 

pip install --upgrade whatsapp-python

#For Linux | MAC 

pip3 install --upgrade whatsapp-python
```

## Setting up

To get started using this package, you will need **TOKEN** and **TEST WHATSAPP NUMBER** (the library works either with a production phone number, if you have one) which you can get from the [Facebook Developer Portal](https://developers.facebook.com/)

Here are steps to follow for you to get started:

1. [Go to your apps](https://developers.facebook.com/apps)
2. [create an app](https://developers.facebook.com/apps/create/)
3. Select Business >> Business
4. It will prompt you to enter basic app informations
5. It will ask you to add products to your app
    a. Add WhatsApp Messenger
6. Right there you will see a your **TOKEN** and **TEST WHATSAPP NUMBER** and its phone_number_id
7. Lastly verify the number you will be using for testing on the **To** field.

Once you've followed the above procedures you're ready to start hacking with the Wrapper.

## Authentication

To authenticate your application, you need to specify  the ```TOKEN``` and the ```phone_number_id``` of your application. The `logger` parameter is optional and it's used to disable logging (default: `True`)

```python
>>> from whatsapp import WhatsApp
>>> messenger = WhatsApp('TOKEN',  phone_number_id='xxxxxxxxx', logger=True)
```

Once you have authenticated your app you can start using the above mentioned feature as shown above;

> It is only possible to send messages other than templates only after the target phone responds to an initial template message or sends a message first. This resets every 24 hours; after that, you need to send a template again or the message won't be delivered. Reference: <https://developers.facebook.com/community/threads/425605939396247/>

## Logging

You can configure your own log level. This is an example to set the log level to info. By default only Error messages are logged.

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
```

To disable logging, set the `logger` parameter to `False` when initializing the `WhatsApp` object.


## Sending Messanges

Use this method to send text message to a WhatsApp number.

```python
>>> messenger.send_message('Your message ', 'Mobile eg: 255757xxxxx')
```

## Marking messages as read

Use this method to mark a previously sent text message as read.

```python
>>> messenger.mark_as_read('Message ID')
```
    
## Sending Images

When sending media(image, video, audio, gif and document ), you can either specify a link containing  the media or specify object id, you can do this using the same method.

By default all media methods assume you're sending link containing media but you can change this by specifying the ```link=False```.

Here an example;

```python
>>> messenger.send_image(
        image="https://i.imgur.com/Fh7XVYY.jpeg",
        recipient_id="255757xxxxxx",
    )
```

> Note: You can also send media from your local machine but you have to upload it first to Whatsapp Cloud API, you can do this using the ```upload_media``` method. and then use the returned object id to send the media.

Here an example;

```python
>>> media_id = messenger.upload_media(
        media='path/to/media',
    )['id']
>>> messenger.send_image(
        image=media_id,
        recipient_id="255757xxxxxx",
        link=False
    )
```

> Note: Don't forget to set the link to False, and also you can use the same technique for sending video, audio, gif and document from your local machine.

## Sending Video

Here an example;

```python

>>> messenger.send_video(
        video="https://www.youtube.com/watch?v=K4TOrB7at0Y",
        recipient_id="255757xxxxxx",
    )
```

## Sending Audio

Here an example;

```python
>>> messenger.send_audio(
        audio="https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3",
        recipient_id="255757xxxxxx",
    )
```

## Sending Document

Here an example;

```python
>>> messenger.send_document(
        document="http://www.africau.edu/images/default/sample.pdf",
        recipient_id="255757xxxxxx",
    )
```

## Sending Location

Here an example;

```python
>>> messenger.send_location(
        lat=1.29,
        long=103.85,
        name="Singapore",
        address="Singapore",
        recipient_id="255757xxxxxx",
    )
```

## Sending Interactive buttons

Here an example;

> Note: row button title may not exceed 20 characters otherwise your message will not be sent to the target phone.

```python
>>> messenger.send_button(
        recipient_id="255757xxxxxx",
        button={
            "header": "Header Testing",
            "body": "Body Testing",
            "footer": "Footer Testing",
            "action": {
                "button": "Button Testing",
                "sections": [
                    {
                        "title": "iBank",
                        "rows": [
                            {"id": "row 1", "title": "Send Money", "description": ""},
                            {
                                "id": "row 2",
                                "title": "Withdraw money",
                                "description": "",
                            },
                        ],
                    }
                ],
            },
        },
    )
```

## Sending Interactive reply buttons

Here an example;

> Send reply button only displays three reply buttons, if it exceeds three reply buttons, it will raise an error and your message will not be sent.

```python
>>> messenger.send_reply_button(
        recipient_id="255757xxxxxx",
        button={
            "type": "button",
            "body": {
                "text": "This is a test button"
            },
            "action": {
                "buttons": [
                    {
                        "type": "reply",
                        "reply": {
                            "id": "b1",
                            "title": "This is button 1"
                        }
                    },
                    {
                        "type": "reply",
                        "reply": {
                            "id": "b2",
                            "title": "this is button 2"
                        }
                    }
                ]
            }
      },
    )
```

## Sending a Template Messages
    
Here how to send a pre-approved template message, Template messages can either be;

1. Text template
2. Media based template
3. Interactive template

You can customize the template message by passing a dictionary of components.

    
IMPORTANT: components are also known as variable parameters (like `{{0}}` or `{{1}}`) which are used to include variables into a message.
You can find the available components in the documentation.
<https://developers.facebook.com/docs/whatsapp/cloud-api/guides/send-message-templates>

```python
>>> messenger.send_template("hello_world", "255757xxxxxx", components=[], lang="en_US")
```
`lang` is optional but required when sending templates in other languages.

## Webhook

Webhook are useful incase you're wondering how to respond to incoming message sent by users.
An example of webhook is shown in the [hook.py](hook.py) file.

## Steps to deploy the webhook to Heroku

1. Click the deploy button and the Heroku webpage will open for authentication, after authentication sit back and relax for deployment to finish. [![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/JAXPARROW/whatsapi-flask-webhook) -- the template repo uses an outdated version of the library
2. From Heroku settings configure your Environment varibles of your WhatsAapp application.
3. Setup and verify your webhook url and token then subscribe to messages.

To learn more about webhook and how to configure in your Facebook developer dashboard please [have a look here](https://developers.facebook.com/docs/whatsapp/cloud-api/guides/set-up-webhooks).


## Issues

If you are facing any issues or have any questions, please open an issue on the [GitHub repository](https://github.com/filipporomani/whatsapp/issues)

## Contributing

This is an opensource project published under the ```MIT License``` so anyone is welcome to contribute.

## References

1. [WhatsApp Cloud API official documentation](https://developers.facebook.com/docs/whatsapp/cloud-api/)