# Just another URL shortener CLI tool

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

4. Create .env file and place your Bitly Token in it
```python
BITLY_TOKEN=place_your_token_here
```

5. Run
```bash
python main.py http://example.com
```
## Examples

Lets say you want to shorten this link: ```https://www.reddit.com/r/python```

So you have to run main.py with this URL as an argument.
```bash
python main.py https://www.reddit.com/r/python
```

Voila! You now have a Bitlink to share!
```bash
Bitlink: bit.ly/3qWSato
```

Or maybe you want to get some stats of Biltlink you've got there.
Just run main.py with your Bitlink as an argument.
```bash
python main.py bit.ly/3qWSato
```

And the answer is:
```bash
Click counts: 7
```