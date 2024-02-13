# rclone-generator-bot
Generate your Rclone config easily via Telegram bot
## Demo
1. https://t.me/CanonRcloneBot
2. https://t.me/CanonRcloneV2Bot
## How to deploy
### Docker
Coming soon
### Legacy
1. Clone this repository
```
git clone https://github.com/devolart/rclone-generator-bot
```
2. Open the cloned directory
```
cd rclone-generator-bot
```
3. Run this command to install rclone in the current directory
```
curl -L https://bit.ly/rclone_noroot | bash
```
4. Install python packages from requirements file
```
pip install -r requirements.txt
```
NOTE: This bot uses old version of `python-telegram-bot` package (version 13.7). If your machine uses the same package with different versions for other bots, I recommend you to use venv or add this argument `--target=.` to the end of the command above to install the packages in the current directory instead.

5. Edit `main.py` to put your bot token inside (you can use Nano, Vi, or any other text editors. In this example, we use Nano)
```
nano main.py
```
6. Run `main.py` with Python
```
python main.py
```
### Heroku
Coming soon
### Render
Coming soon

## Support
Telegram channel: https://t.me/tearflakes
