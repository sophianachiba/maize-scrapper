Insctuction.

1. Create virtualenv:
virtualenv -p /usr/bin/python3 stree-food-parser

2. Activate:
cd stree-food-parser && source bin/activate

3. Clone project:
git clone https://github.com/kirimaks/street-food-scraper.git && cd street-food-scraper

4. Install requirements:
pip install -r requirements.txt

5. Run scraper:
cd street_food && scrapy crawl get-food -o food.csv
