### INF601 - Advanced Programming in Python
### Rachel White
### Mini Project 3
 
 
# Project Title
 
This project uses Pandas DataFrames to answer a question with data.
 
## Description
 
I am using the us_average_prices_item_summary.csv file from https://www.kaggle.com/datasets/harshitsama/us-grocery-and-gas-prices-2015-2026?resource=download to see how the cost of ground beef, regular unleaded gasoline, and coffee has changed from 2015 to 2026.
 
## Getting Started
 
### Dependencies
 
* You will need the us_average_prices_item_summary.csv file from https://www.kaggle.com/datasets/harshitsama/us-grocery-and-gas-prices-2015-2026?resource=download
* pip install pandas as pd
 
### Installing
 
* https://github.com/rachelr801/miniproject3RachelWhite.git
 
### Executing program
 
* Make sure us_average_prices_item_summary.csv is in the same folder as main.py
* Install the required packages (matplotlib is needed for the charts):
```
pip install pandas matplotlib
```
* Run the program from the project folder:
```
python main.py
```
* The program loads the CSV into a pandas DataFrame, keeps ground beef, regular unleaded gasoline, and coffee, and prints the first and last price, dollar change, percent change, and average yearly change for each item
* Two charts are saved as PNG files in a `charts/` folder, which is created automatically the first time the program runs:
    * `charts/price_trends.png` - line chart of each item's price from its first date to its last date
    * `charts/price_percent_change.png` - bar chart of each item's total percent change
 
## Help
 
* `FileNotFoundError: ... us_average_prices_item_summary.csv` - the program looks for the CSV in the folder you run it from. Download the file from the Kaggle link above, place it next to main.py, and run the program from that folder:
```
cd miniproject3RachelWhite
python main.py
```
* `ModuleNotFoundError: No module named 'pandas'` (or `'matplotlib'`) - the packages are not installed in the Python you are using:
```
pip install pandas matplotlib
```
* `ValueError: Missing required columns` or `Items not found in the data` - the CSV is not the item summary file. The program needs the `item`, `first_date`, `last_date`, `first_price`, and `last_price` columns, and the items "Ground beef, 100% beef", "Gasoline, unleaded regular", and "Coffee, 100%, ground roast, all sizes". Use us_average_prices_item_summary.csv, not the monthly or wide files.
* The `charts/` folder is created each time the program runs and is listed in .gitignore, so the PNG files are not committed. Run the program again to regenerate them.
 
## Authors
 
Contributors names and contact info
 
ex. Dominique Pizzie  
ex. [@DomPizzie](https://twitter.com/dompizzie)
 
## Version History
 
* 0.2
    * Various bug fixes and optimizations
    * See [commit change]() or See [release history]()
* 0.1
    * Initial Release
 
## License
 
This project is licensed under the [NAME HERE] License - see the LICENSE.md file for details
 
## Acknowledgments
 
https://www.kaggle.com/datasets/harshitsama/us-grocery-and-gas-prices-2015-2026?resource=download