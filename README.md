# subgram-telegram-bot
A test telegram bot which shows how easy it is to integrate the subscriptions and start to monetise your audience.

This bot is based on `python-telegram-bot` Telegram API wrapper and [`subgram-python-sdk`](https://github.com/subgram/subgram-python-sdk) package.

Start with reading `bot.py` file. Then check [`subgram-python-sdk`](https://github.com/subgram/subgram-python-sdk) README file.


## How to run

``` bash
cp .env.example .env
```

Fill `.env` file with your tokens. To get `SUBGRAM_TOKEN` and `SUBGRAM_PRODUCT_ID` please go to [@subgram](https://t.me/subgram) for information.


``` bash
pip install -r requirements.txt

python bot.py
```


Or you can use our Dockerfile if you want.

---
*Happy coding!*