# botjack_discord_bot
Discord bot implementation with an ML-trained image classification function. 
It offers several functionalities:

| Functions | Descriptions |
| ------ | ------ |
| !help | Describes the functions currently available to the bot |
| ?info | A more interactive help |
| !avatar | Cites the reddit account of the bot's avatar |
| !roll ``<val>d<val>`` | Dice rolling function |

As well has an image detection implementation. 

| Functions | Descriptions |
| ------ | ------ |
| *ML detection* | Provides a ML-modeled result for each picture directly uploaded to discord |

### Installation
botjack_discord_bot requires Python 3.x to run. It uses the following modules:

| Module names |
| ------ |
| cv2 |
| discord |
| os |
| keras |
| numpy |
| os |
| random |
| urllib.request |

Install the dependencies.

```sh
$ cd botjack_discord_bot
$ python setup.py sdist
```

##### Current packaging:
- botjack_discord_bot
    - commands
        - ``init.py``
        - ``commands.py``
        - ``model.h5``
    - ``main.py``
    - ``setup.py``
    - ``README.md``
    - LICENSE

### License
MIT
