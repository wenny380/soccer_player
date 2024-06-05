from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import traceback
import pandas as pd

links = ['https://fbref.com/en/matches/13878f62/Le-Havre-Lyon-September-15-2023-Division-1-Feminine',
         'https://fbref.com/en/matches/da74f2fe/Paris-Saint-Germain-Lyon-October-1-2023-Division-1-Feminine',
         'https://fbref.com/en/matches/c577e576/Lyon-Bordeaux-October-8-2023-Division-1-Feminine',
         'https://fbref.com/en/matches/78027557/Lyon-Saint-Etienne-October-14-2023-Division-1-Feminine',
         'https://fbref.com/en/matches/6df32e03/Stade-de-Reims-Lyon-October-22-2023-Division-1-Feminine',
         'https://fbref.com/en/matches/040b32bb/Paris-FC-Lyon-November-5-2023-Division-1-Feminine',
         'https://fbref.com/en/matches/faf3df46/Lyon-Montpellier-November-10-2023-Division-1-Feminine',
         'https://fbref.com/en/matches/51145236/Slavia-Prague-Lyon-November-14-2023-Champions-League',
         'https://fbref.com/en/matches/7214e79d/Lyon-Dijon-November-17-2023-Division-1-Feminine',
         'https://fbref.com/en/matches/49db0aff/Lyon-St-Polten-November-22-2023-Champions-League',
         'https://fbref.com/en/matches/013c6622/Guingamp-Lyon-November-26-2023-Division-1-Feminine',
         'https://fbref.com/en/matches/6da4bd3a/Lyon-Lille-December-8-2023-Division-1-Feminine',
         'https://fbref.com/en/matches/af4b1ba3/Lyon-Brann-December-13-2023-Champions-League',
         'https://fbref.com/en/matches/7ebb0d27/Fleury-Lyon-December-16-2023-Division-1-Feminine',
         'https://fbref.com/en/matches/db4a3116/Brann-Lyon-December-21-2023-Champions-League',
         'https://fbref.com/en/matches/cd755028/Barcelona-Lyon-May-25-2024-Champions-League']

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
    for link in links:
        driver.get(link)
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
        temp_df = pd.DataFrame(complete_stats, columns=columns)
        df = df.append(temp_df)

    # save dataframe to csv
    df.to_csv('player_stats.csv', index=False, encoding='utf-8-sig')
    print("Data saved to player_stats.csv")
except Exception as e:
    print(f"An error occurred:{e}")
    print(traceback.format_exc())
finally:
    driver.quit()
