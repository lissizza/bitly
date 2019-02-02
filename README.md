# Bitly url shorterer

This small script can help you to make your long links short and pretty, and it can check the click statistics for your short links as well. This could be useful for SMM managers, for example.


### How to install
1. To use this script you have been registered on [bit.ly](http://bit.ly/) service. 
2. After registration you should go to **Your Account - Edit Profile - Generic Access Token** and generate your private OAuth token. 
3. Create a file with name `.env` in the same folder as this script is, and put there the next text (place your bit.ly token instead *your_token*, with no quotes):
```
TOKEN=your_token
```
4. Python should be already installed. The minimum requirement is **Python 3.6**.
5. Use `pip` (or `pip3`, if there is a conflict with Python2) to install dependencies:
```console
pip install -r requirements.txt
```

### How to use
Just start the python script with your link as argument:
```console
$ python main.py http://dvmn.org
This is your very short link: http://bit.ly/2Myn2fj
```

```console
$ python3.6 main.py http://bit.ly/2Myn2fj
This link has been clicked 3 times.
```

### Project Goals
The code is written for educational purposes on online-course for web-developers [dvmn.org](https://dvmn.org/).
