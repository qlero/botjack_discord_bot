# botjack_discord_bot
Discord bot implementation with an ML-trained image classification function. 
It offers several functionalities:

| Functions | Descriptions |
| ------ | ------ |
| !help | Describes the functions currently available |
| ?help ``<function_name>`` | Provides some details on the function |
| !avatar | Cites the reddit account of the bot's avatar |
| !roll ``<val>d<val>`` | Dice rolling function |
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