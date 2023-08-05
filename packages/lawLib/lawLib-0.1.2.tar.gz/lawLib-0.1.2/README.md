# lawLib

Library to extract legal information from official resources.

### Installation
```
<h3>:construction: Working enviroment:</h3>
<li>Python version <b>3.9</b></li> 
<li>Virtual enviroment: <b>py -m venv env</b></li> 
<li>Activate on WINDOWS: <b>env\Scripts\activate</b></li>
<li>Activate on MAC: <b>source env/bin/activate</b></li>
<h3>:books: Dependencies</h3>
<li>Install with: <b>pip3 install -r requirements.txt</b></li>
<h3>:mag_right: Testing</h3>
<li>Launch tests with: <b>pytest -W ignore::DeprecationWarning</b></li>
```

### Get started
Get data from Spanish Supreme Court:

```Python
from scrapper import DataScrapper
import configparser

config = configparser.ConfigParser()
config.read("config.ini")
url:str = config['URLS']['SpanishSupremeCourt']+'29174'

returned_data = DataScrapper(url).get_data()
print(returned_data)
```