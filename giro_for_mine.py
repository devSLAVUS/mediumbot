from bs4 import BeautifulSoup
import requests
from datetime import datetime
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.utils import ChromeType
import time
import datetime
from pyvirtualdisplay import Display
from auth_data import log, pas

def get_all(znak):
            vesi = f"https://horo.mail.ru/prediction/{znak}/today/"
            request_vesi = requests.get(vesi)
            soup = BeautifulSoup(request_vesi.text, "lxml")
            giro = soup.find("div", class_ = "article__item article__item_alignment_left article__item_html")
            return giro

def get_weather(gorod):
            r = f"http://api.openweathermap.org/data/2.5/weather?q={gorod}&appid=12a7eeeda8c4becc9503870405c37f9e&units=metric"
            r = requests.get(r)
            data = r.json() 
            city = data["name"]
            cur_weather = data["main"]["temp"]
            weather_description = data["weather"][0]["main"]
            humidity = data["main"]["humidity"]
            pressure = data["main"]["pressure"]
            wind = data["wind"]["speed"]
            wd = "Посмотри в окно, не пойму что там за погода!"
            sunrise_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
            sunset_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunset"])
            length_of_the_day = datetime.datetime.fromtimestamp(data["sys"]["sunset"]) - datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
            open_weather = [city, cur_weather, weather_description, humidity, pressure, wind, sunrise_timestamp, sunset_timestamp, length_of_the_day]
            return open_weather
def maska(nums):
    zs = ["255.255.255.255", "1"]
    zl = ["255.255.255.254", 2]
    zo = ["255.255.255.252", 4]
    sq = ["255.255.255.248", 8]
    sg = ["255.255.255.240", 16]
    sj = ["255.255.255.224", 32]
    sb = ["255.255.255.192", 64]
    sv = ["255.255.255.128", 128]
    sa = ["255.255.255.0", 256]
    sp = ["255.255.254.0", 512]
    sh = ["255.255.252.0", 1024]
    fg = ["255.255.248.0", 2048]
    dfg = ["255.255.240.0", 4096]
    dsfsf = ["255.255.224.0", 8192]
    fghf = ["255.255.192.0", 16384]
    ytu = ["255.255.128.0", 32768]
    xcvf = ["255.255.0.0", 65536]
    sdr = ["255.254.0.0", 131072]
    serf = ["255.252.0.0", 262144]
    hgk = ["255.248.0.0", 524288]
    ghj = ["255.240.0.0", 1048576]
    tyh = ["255.224.0.0", 2097152]
    jk = ["255.192.0.0", 4194304]
    er = ["255.128.0.0", 8388608]
    hnhg = ["255.0.0.0", 16777216]
    gfh = ["254.0.0.0", 33554432]
    rdtt = ["252.0.0.0", 67108864]
    fghewrr = ["248.0.0.0", 134217728]
    rrzs = ["240.0.0.0", 268435456]
    zggs = ["224.0.0.0", 536870912]
    zvvs = ["192.0.0.0", 1073741824]
    zdfs = ["128.0.0.0", 2147483648]
    zsds = ["0.0.0.0", 4294967296]

    pool = {"32": zs, "31": zl,"30": zo, "29": sq, "28": sg, "27": sj, 
            "26": sb, "25": sv, "24": sa, "23": sp, "22": sh, "21": fg, "20": dfg}

    vivod = pool.get(nums, "Не найден")
    print (vivod)
    return "Маска: {}\nКоличество адресов: {}".format(vivod[0], vivod[1])

def download_image(dasboard, panelId, user_id):
#   time offsets
    six_hours = datetime.timedelta(hours=6)
    twelve_hours = datetime.timedelta(hours=12)

#   human date
    now = datetime.datetime.now()
    now6 = datetime.datetime.now() - six_hours
    now12 = datetime.datetime.now() - twelve_hours

    stimpenow = str(time.mktime(now.timetuple())).split('.')[0] + str(float(now.microsecond) / 1000000).split('.')[1][0:3]
    stimpe6 = str(time.mktime(now6.timetuple())).split('.')[0] + str(float(now.microsecond) / 1000000).split('.')[1][0:3]
    stimpe12 = str(time.mktime(now12.timetuple())).split('.')[0] + str(float(now.microsecond) / 1000000).split('.')[1][0:3]
    url6 = grafana_url + '/render/dashboard-solo/db/' + dasboard + '?orgId=1&from=' + stimpe6 + '&to=' + stimpenow + '&panelId=' + panelId + '&width=1000&height=500'
    url12 = grafana_url + '' + dasboard + '?orgId=1&from=' + stimpe12 + '&to=' + stimpenow + '&panelId=' + panelId + '&width=1000&height=500'
    for url in url6, url12:
        now = datetime.datetime.now()
        filedate = now.strftime("%Y%m%d_%I-%M-%S-%m")
        r = requests.get(url, verify = False, headers = headers, timeout = 30)
        folder = path + str(user_id) + "/"
        if os.path.exists(folder) is False:
            os.mkdir(folder)
        out = open(folder + str(dasboard) + "_" + filedate + ".png", "wb")
        out.write(r.content)
        out.close()
        time.sleep(0.12)

def get_pic():
    six_hours = datetime.timedelta(hours=6)
    twelve_hours = datetime.timedelta(hours=12)
    one_hours = datetime.timedelta(hours=24)
    now = datetime.datetime.now()
    now6 = datetime.datetime.now() - six_hours
    now12 = datetime.datetime.now() - twelve_hours
    #WINDOW_SIZE = "1920,1080"
    stimpenow = str(time.mktime(now.timetuple())).split('.')[0] + str(float(now.microsecond) / 1000000).split('.')[1][0:3]
    stimpe6 = str(time.mktime(now6.timetuple())).split('.')[0] + str(float(now.microsecond) / 1000000).split('.')[1][0:3]
    stimpe12 = str(time.mktime(now12.timetuple())).split('.')[0] + str(float(now.microsecond) / 1000000).split('.')[1][0:3]
    display = Display(visible=0, size=(800, 600))
    display.start()
    try:
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument('--no-sandbox')
        #WINDOW_SIZE = "1920,1080"
     #   chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
        if os.environ.get('SERVER_ENV') == 'local':
            driver = webdriver.Chrome(ChromeDriverManager(chrome_type=ChromeType.GOOGLE, cache_valid_range=5).install(), options=chrome_options)
        else:
            # driver = webdriver.Chrome(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM, cache_valid_range=5).install(), options=chrome_options)
            driver = webdriver.Chrome(executable_path='/usr/bin/chromedriver', options=chrome_options)

        driver.get(f'http://10.78.203.228:3000/d-solo/TTU8t0Dnz/otrs-titans?orgId=1&from={stimpe6}&to={stimpenow}&panelId=2')
        login_in = driver.find_element_by_name("user")
        pass_in = driver.find_element_by_name("password")
        login_in.clear()
        login_in.send_keys(log)
        pass_in.clear()
        pass_in.send_keys(pas)
        but_in = driver.find_element_by_class_name("css-w9m50q-button").click()
        time.sleep(2)
        driver.save_screenshot("/reenshot.png")
        driver.quit()
    
    except Exception as e:
        print('Ошибка при сохранении скриншота: {}'.format(e))
    display.stop()

def get_graf():
    six_hours = datetime.timedelta(hours=6)
    moth = datetime.timedelta(days=30)
    one_hours = datetime.timedelta(hours=24)
    now = datetime.datetime.now() + one_hours
    now6 = datetime.datetime.now() - six_hours
    now12 = datetime.datetime.now() - moth

    stimpenow = str(time.mktime(now.timetuple())).split('.')[0] + str(float(now.microsecond) / 1000000).split('.')[1][0:3]
    stimpe6 = str(time.mktime(now6.timetuple())).split('.')[0] + str(float(now.microsecond) / 1000000).split('.')[1][0:3]
    stimpe12 = str(time.mktime(now12.timetuple())).split('.')[0] + str(float(now.microsecond) / 1000000).split('.')[1][0:3]
    display = Display(visible=0, size=(800, 600))
    display.start()
    try:
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument('--no-sandbox')

        if os.environ.get('SERVER_ENV') == 'local':
            driver = webdriver.Chrome(ChromeDriverManager(chrome_type=ChromeType.GOOGLE, cache_valid_range=5).install(), options=chrome_options)
        else:
            # driver = webdriver.Chrome(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM, cache_valid_range=5).install(), options=chrome_options)
            driver = webdriver.Chrome(executable_path='/usr/bin/chromedriver', options=chrome_options)

        driver.get(f'http://10.78.203.228:3000/d-solo/TTU8t0Dnz/otrs-titans?orgId=1&from={stimpe12}&to={stimpenow}&panelId=10')
        login_in = driver.find_element_by_name("user")
        pass_in = driver.find_element_by_name("password")
        login_in.clear()
        login_in.send_keys(log)
        pass_in.clear()
        pass_in.send_keys(pas)
        but_in = driver.find_element_by_class_name("css-w9m50q-button").click()
        time.sleep(4)
        driver.save_screenshot("/grafshot.png")
        driver.quit()
    
    except Exception as e:
        print('Ошибка при сохранении скриншота: {}'.format(e))
    display.stop()

def get_zab():
    six_hours = datetime.timedelta(hours=6)
    moth = datetime.timedelta(days=30)
    now = datetime.datetime.now()
    now6 = datetime.datetime.now() - six_hours
    now12 = datetime.datetime.now() - moth
    WINDOW_SIZE = "1280,1024"
    stimpenow = str(time.mktime(now.timetuple())).split('.')[0] + str(float(now.microsecond) / 1000000).split('.')[1][0:3]
    stimpe6 = str(time.mktime(now6.timetuple())).split('.')[0] + str(float(now.microsecond) / 1000000).split('.')[1][0:3]
    stimpe12 = str(time.mktime(now12.timetuple())).split('.')[0] + str(float(now.microsecond) / 1000000).split('.')[1][0:3]
    display = Display(visible=0, size=(1280, 1024))
    display.start()
    try:
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
        if os.environ.get('SERVER_ENV') == 'local':
            driver = webdriver.Chrome(ChromeDriverManager(chrome_type=ChromeType.GOOGLE, cache_valid_range=5).install(), options=chrome_options)
        else:
            # driver = webdriver.Chrome(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM, cache_valid_range=5).install(), options=chrome_options)
            driver = webdriver.Chrome(executable_path='/usr/bin/chromedriver', options=chrome_options)
       
        driver.get(f'http://zabbix.denga.net/index.php?reconnect=1&form=default')
        login_in = driver.find_element_by_id("name")
        pass_in = driver.find_element_by_id("password")
        login_in.clear()
        login_in.send_keys('support')
        pass_in.clear()
        pass_in.send_keys('shEBb3Sb')
        but_in = driver.find_element_by_id("enter").click()
        time.sleep(1)
        driver.get(f'http://zabbix.denga.net/zabbix.php?action=problem.view&ddreset=1')
        time.sleep(2)
        driver.save_screenshot("/zabshot.png")
        driver.quit()
    except Exception as e:
        print('Ошибка при сохранении скриншота: {}'.format(e))
    display.stop()
