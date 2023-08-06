# Webex-Integration

**webex-integration** a simple project which can be used to send webex 
messages and emits log records from the native logging module

## Installing Webex-Integration

Webex-Integration is available on PyPi

```console
$ python -m pip install webex-integration
```

## Usage

### Simple Message

In order to send a simple webex message, you just have to initialize a new 
`WebexTeams` instance with you personal token and the appropriate room id:

```python
from webexintegration import WebexTeams

webex_teams = WebexTeams(
    token = my_token,
    room_id = my_room_id
)

response = webex_teams.send_message("This is a bot")
response.raise_for_status()
```

### logging handler

In order to send logging message into an selected chat room, you just have to 
initialize a new `WebexTeamsHandler` with an appropriate `WebexTeams` instance 
and pass the handler to your logging instance:

```python
import logging
from webexintegration import WebexTeams

webex_teams = WebexTeams(
    token = my_token,
    room_id = my_room_id
)
webex_handler = WebexHandler(webex_teams)
webex_handler.setLevel(logging.INFO)

logging.basicConfig(level=logging.INFO, handlers=[webex_handler])

try:
    raise RuntimeError()
except Exception as ex:
    logging.error("An Error occured")
```

The default logging formatter is set to `WebexFormatter`, feel free to 
override or use a different formatter.
