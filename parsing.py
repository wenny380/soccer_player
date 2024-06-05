from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import traceback
import pandas as pd


columns=['Player', 'Pos', 'Age', 'Min', 'Gls', 'Ast', 'Sh', 'SoT', 'CrdY', 'CrdR', 'Touches', 'Tkl', 'Int',
             'Blocks', 'SCA', 'GCA', 'Cmp', 'Att', 'cpm%', 'PrgP', 'PrgC', 'TOatt', 'TOsucc']
df = pd.DataFrame(columns=columns)
# Path to the chromedriver executable
chrome_driver_path = 'C:/Users/Acer/Documents/Master/Diplome/chromedriver-win64/chromedriver.exe'

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument('--headless')  # Run in headless mode for better performance
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--blink-settings=imagesEnabled=false')

# Initialize the WebDriver with the specified Chrome driver
service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)
datastat = ['position','age', 'minutes','goals','assists','shots','shots_on_target','cards_yellow',
                    'cards_red','touches','tackles','interceptions','blocks','sca','gca','passes_completed','passes',
                    'passes_pct','progressive_passes','progressive_carries','take_ons','take_ons_won']
# Set page load timeout
driver.set_page_load_timeout(90)

try:
    driver.get('https://fbref.com/en/matches/da74f2fe/Paris-Saint-Germain-Lyon-October-1-2023-Division-1-Feminine')
    players = WebDriverWait(driver, 60).until(
        EC.presence_of_all_elements_located((By.XPATH, '//th[@data-stat="player"]'))
    )
    # extract player names
    players_list1 = [player.text.strip() for player in players if player.text != ""]
    for name in players_list1:
        if name == "Player" or name == "15 Players":
            players_list1.remove(name)
    players_list = []
    for x in players_list1:
        if x not in players_list:
            players_list.append(x)
    print(players_list)
    player_stat ={'players': players_list}
    for elem in datastat:
        player_stat[elem] = WebDriverWait(driver, 60).until(
        EC.presence_of_all_elements_located((By.XPATH, f'//td[@data-stat="{elem}"]'))
        )
    players_stats ={}
    for key, values in player_stat.items():
        if key == 'players':
            players_stats[key] = values
        else:
            players_stats[key] = [value.text for value in values if hasattr(value, 'text') and value.text != ""]

    for key, values in players_stats.items():
      print(f"{key}: {[value for value in values]}")

    complete_stats = list(zip(*players_stats.values()))
    print(complete_stats)
    df = pd.DataFrame(complete_stats, columns=columns)

    # save dataframe to csv
    df.to_csv('player_stats.csv', index=False, encoding='utf-8-sig')
    print("Data saved to player_stats.csv")
except Exception as e:
    print(f"An error occurred:{e}")
    print(traceback.format_exc())
finally:
    driver.quit()
