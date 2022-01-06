# Урок 2. Посчитайте клики по ссылкам

This project is a simple command line tool for shortening URLs via Bitly service.

## Features
- Shorten URL via [Bitly](https://bitly.com/)
- Get click counts of shortened URL

## Installation notes
1. Clone project
```bash
git clone https://github.com/gennadis/api-bitly.git
cd api-bitly
```

2. Create virtual environment
```bash
python3 -m venv env
source env/bin/activate
```

3. Install requirements
```bash
pip install -r requirements.txt
```

4. Rename .env.example file to .env and place Bitly Token in it

5. Run
```bash
python main.py URL
```
## Examples

Lets say you want to shorten this link: ```https://www.reddit.com/r/python```

So you have to run main.py with this URL as an argument.
```bash
python main.py https://www.reddit.com/r/python
```

You'll get a Bitlink:
```bash
Bitlink: bit.ly/3qWSato
```

