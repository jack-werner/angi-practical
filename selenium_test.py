"this is a test for learning how selenium works"
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# url = "https://www.bbb.org/"
bbb_search_url = "https://www.bbb.org/search?find_country=USA&find_entity=10126-000&find_id=1362_3100-14100&find_latlng=32.834605%2C-83.651801&find_loc=Macon%2C%20GA&find_text=Roofing%20Contractors&find_type=Category&page=1&sort=Distance"
user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"

#configure headless and user-agent
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument(f"--user-agent={user_agent}")

x_path = '//*[@id="content"]/div/div[3]/div/div[1]/div[2]/div[4]'

print("initializing driver")
driver = webdriver.Chrome(options=chrome_options)
print("get bbb")
driver.get(bbb_search_url)

print(driver.title)

driver.quit()
