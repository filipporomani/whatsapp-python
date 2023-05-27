## whatsapp.App()


#### All the methods are the same as the ones in the official docs.

To create an event listener app, you need to create an App() instance and pass it a callback function. The callback function will be called every time an event occurs.

```python
from whatsapp import App

app = App()

@app.on_message
def on_message(message):
    print(message)

app.run(host, port, debug, **kwargs)
```

The on_message event is triggered on a new message in any chat. The Message object is passed as an argument to the callback function.

The on_verification event is triggered when the webhook gets verified by WhatsApp. The Verification object is passed as an argument to the callback function. If the verification is not successful, the callback function will return False.

The on_event event is triggered on any event. A single argument is passed, whose type depends on the event type (Message, str, bool, etc).

