import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc
import sys
import os
import re

sys.stdin.reconfigure(encoding='utf-8')
sys.stdout.reconfigure(encoding='utf-8')

options = uc.ChromeOptions()
options.add_argument("start-maximized")
options.add_argument("lang=hi")

time.sleep(15)

driver = uc.Chrome(options=options)

link = 'https://www.classcentral.com/'

driver.get(link)
content = driver.page_source

all_links = []

elems = driver.find_elements(By.XPATH, "//a[@href]")

for elem in elems:
    if elem.get_attribute("href") not in all_links:
        all_links.append(elem.get_attribute("href"))
    elif elem.get_attribute("href") in all_links:
        pass

for link in all_links:
    driver.get(link)
    time.sleep(5)

    try:
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, "sticky-footer")))
    except:
        pass

    max_height = driver.execute_script("return document.body.scrollHeight")
    height = 600
    for _ in range(50):
        if height >= max_height:
            break
        else:
            driver.execute_script(f"window.scrollTo(0, {height})")
            time.sleep(0.5)
            height += 600

    content = driver.page_source

    link = link.replace('https://www.classcentral.com/', '')

    content = content.replace('www.classcentral.com/', 'denizgedik.github.io/scraping_project/')

    x = re.findall(' href="/\w+', content)
    z = re.findall(' href="/\w+/\w+', content)

    z_alpha = re.findall(' href="https://denizgedik.github.io/scraping_project/report/"', content)
    z0 = re.findall(' href="https://denizgedik.github.io/scraping_project/report/\w+"', content)
    z1 = re.findall(' href="https://denizgedik.github.io/scraping_project/report/\w+[-]\w+/"', content)
    z2 = re.findall(' href="https://denizgedik.github.io/scraping_project/report/\w+[-]\w+[-]\w+/"', content)
    z3 = re.findall(' href="https://denizgedik.github.io/scraping_project/report/\w+[-]\w+[-]\w+[-]\w+/"', content)
    z4 = re.findall(' href="https://denizgedik.github.io/scraping_project/report/\w+[-]\w+[-]\w+[-]\w+[-]\w+/"', content)
    z5 = re.findall(' href="https://denizgedik.github.io/scraping_project/report/\w+[-]\w+[-]\w+[-]\w+[-]\w+[-]\w+/"', content)


    combo = z_alpha + z0 + z1 + z2 + z3 + z4 + z5

    q = [str(item)[:-2] + '.html"' for item in combo]

    print(q)
    numro = 0
    for item in combo:
        print(q[numro])
        content = content.replace(item, q[numro])
        numro += 1

    comb = x + z
    y = [str(item).replace(' href="/', ' href="https://denizgedik.github.io/scraping_project/') for
         item in comb]

    num = 0
    for item in comb:
        content = content.replace(item, y[num])
        num += 1

    content = content.replace(',r.p="/webpack/"', ',r.p="https://www.classcentral.com/webpack/"')

    content = content.replace('https://denizgedik.github.io/scraping_project/report/wp-content/', 'https://www.classcentral.com/report/wp-content/')
    content = content.replace('https://denizgedik.github.io/scraping_project/report/wp-includes/', 'https://www.classcentral.com/report/wp-includes/')


    yes = os.path.join('sites', f'{link}.html')
    if 'report' in yes:
        yes = yes.replace('/.html', '.html')
    print(yes)
    os.makedirs(os.path.dirname(yes), exist_ok=True)

    with open(yes, 'w', encoding='utf-8') as f:
        f.write(content)