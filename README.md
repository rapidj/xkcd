# xkcd
Publishing xkcd comics in Telegram

# How to start

Python3 should be already installed. Then use pip to install dependencies:

```bash
pip install -r requirements.txt
```

### Environment variables

- TLG_BOT_TOKEN <- token for your Telegram bot
- TLG_CHANNEL_ID <- id of your Telegram channel


### Prerequisites

1. Crete a Telegram bot (please see the [documentation](https://core.telegram.org/bots/features#botfather))

2. Create a Telegram channel

3. Add your bot as administrator to your channel 

### Run

If you want to publish a random comic, just run main.py script.

```bash
$ python main.py
```