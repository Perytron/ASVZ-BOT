### Status
This project is currently under development while you are reading this. The ASVZ bot does not yet work in any shape or form.

### Install Requirements
The ASVZ bot needs certain python packages to function successfully. These are listed in the **requirements.txt**. Be aware, you will need [pip](https://pip.pypa.io/en/stable/installation/) to install the dependencies.\
First off, open your command-line interface of choice, on Windows this would be **cmd**, and type the following into the console:

`cd C:\location\to\your\repository\ASVZ-BOT`

You should now find yourself in the root directory of [ASVZ-BOT](https://github.com/Perytron/ASVZ-BOT). Next off, call [pip](https://pip.pypa.io/en/stable/installation/) to install the required packages by entering:

`pip install -r requirements.txt`

### 2 Run ASVZ Bot
#### 2.1 Navigate to Directory
In order to run your lovely ASVZ bot, you will first need to visit him at home. Open up your command-line interface of choice and use the navigation software called `cd` to pay him a visit.

`cd C:\location\to\your\repository\ASVZ-BOT\src\asvzbot`

#### 2.2 Call ASVZ Bot
Now, it depends on how you have set up Python. The matter of installing Python would be a scientific paper alone, so please make sure you know how to run a python script from the command-line. If you don't know where to start, compose an [issue](https://github.com/Perytron/ASVZ-BOT/issues) and I will help you as soon as possible™. Mostly, however, it boils down to either one of the following options:

`python main.py` or `python3 main.py` or `"C:/location/to/python.exe" main.py`

#### 2.3 Command-Line Arguments
In order for your lovely ASVZ bot to work his (...) off, he firstly needs to be well-fed using command-line arguments or a configuration file. Silly jokes aside, be aware that, when running it the first time, you need to provide every parameter using command line arguments. If every required parameter has been provided, the bot will then run and automatically generate a configuration file which is being used the next time. This enables you to completely omit command-line arguments from now on, or use them as a way of updating the configuration file.\
Please consider running the following command, using the method that works for you, to get an overview over the possible options:

`python main.py -h`

This will generate the following message, telling you what each parameter does in detail:

```
usage: Parser [-h] [-u USERNAME] [-p PASSWORD] [-b {brave,chromium,chrome,firefox,edge}] [-l {asvz,switch}] [-i ID] [-s]

options:
  -h, --help            		show this help message and exit
  -u USERNAME, --username USERNAME	provide username you use to login to ASVZ
  -p PASSWORD, --password PASSWORD	provide password to the corresponding username
  -b {...}, --browser {...}		provide if you want to use a specific browser
  -l {...}, --login {...}		provide login method
  -i ID, --id ID        		provide sports lesson id
  -s, --stealth         		do not store the password in 'config.json'
```
#### 2.4 Examples
A complete first call for a newly cloned bot would look like this:

`python main.py -u UZHBeschte -p ETHIschScheiseLoL -b firefox -l switch -i 69420`

The following example would be a call if some info has changed: For example, you have changed your password and additionally, you now would like to participate in another sports lesson. Your lovely bot will read the configuration and override it with the command-line options you have provided. In this particular example, the username (-u), the browser (-b) and the login method (-l) would stay the same, but the password (-p) and the sports lesson ID (-i) will be updated.

`python main.py -i 123456 -p HelloWorld`

If you, for whatever reason, don't want your password stored in the configuration file, you can supply `-s` as a parameter. However, be aware that you therefore need to supply the password each time as command-line arguments too.

`python main.py -s -p HelloWorld`