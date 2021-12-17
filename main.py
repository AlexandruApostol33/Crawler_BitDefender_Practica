# Import code:
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from datetime import datetime
import json


# functia de gasit pretul unui produs

def get_site_info(driver, link_site):
    driver.get(link_site)
    lista_nume = []
    lista_pret = []
    ora_interogare = []
    try:
        container_ul = driver.find_elements(By.TAG_NAME, "ul")
        for prod in container_ul:
            container_li = prod.find_elements(By.CLASS_NAME, "Products-item")
            for container_a in container_li:
                nume_produs = container_a.find_element(By.CLASS_NAME, "Product-nameHeading")
                pret_produs = container_a.find_element(By.CLASS_NAME, "Price-current")
                lista_nume.append(nume_produs.text)
                lista_pret.append(pret_produs.text)
                now = datetime.now()
                dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
                ora_interogare.append(dt_string)
    except Exception as fail_fetch_info:
        print(fail_fetch_info)
        pass
    return lista_nume, lista_pret, ora_interogare


def produs_nou(lista_nume_interogare_curenta, lista_preturi_interogare_curenta, ora_interogare_curenta,
               lista_nume_produs_anterioare, lista_preturi_produs_anterioare, ora_interogare_anterioara):
    i = 0
    for prod in lista_nume_interogare_curenta:
        if prod not in lista_nume_produs_anterioare:
            lista_nume_produs_anterioare.append(prod)
            lista_preturi_produs_anterioare.append(lista_preturi_interogare_curenta[i])
            ora_interogare_anterioara[i] = ora_interogare_curenta[i]
        i += 1
    return lista_nume_produs_anterioare, lista_preturi_produs_anterioare, ora_interogare_anterioara


def produs_eliminat(lista_nume_interogare_curenta, lista_nume_produs_anterioare, lista_preturi_produs_anterioare,
                    ora_interogare_anterioara):
    i = 0
    for prod in lista_nume_produs_anterioare:
        if prod not in lista_nume_interogare_curenta:
            lista_nume_produs_anterioare.pop(i)
            lista_preturi_produs_anterioare.pop(i)
            ora_interogare_anterioara.pop(i)
        i += 1
    return lista_nume_produs_anterioare, lista_preturi_produs_anterioare, ora_interogare_anterioara


def update_preturi(lista_preturi_interogare_curenta, ora_interogare_curenta, lista_nume_produs_anterioare,
                   lista_preturi_produs_anterioare, ora_interogare_anterioara):
    for i in range(len(lista_nume_produs_anterioare)):
        if lista_preturi_produs_anterioare[i] != lista_preturi_interogare_curenta[i]:
            lista_nume_produs_anterioare[i] = lista_preturi_interogare_curenta[i]
            ora_interogare_anterioara[i] = ora_interogare_curenta[i]
            # print(i, '\n')
            # print(lista_preturi_interogare_curenta[i], "\n")

        # else:
        # print("sal" "\n")
    return lista_preturi_produs_anterioare, ora_interogare_anterioara


def interogari(lista_nume_produs_anterioare, lista_preturi_produs_anterioare, ora_interogare_anterioara, link_site,
               driver):
    time.sleep(1)
    lista_nume, lista_pret, ora_interogare = get_site_info(driver, link_site)
    # print (lista_nume,"\n", lista_pret, "\n", ora_interogare)
    lista_nume_produs_anterioare, lista_preturi_produs_anterioare, ora_interogare_anterioara = produs_nou(
        lista_nume_produs_anterioare, lista_preturi_produs_anterioare, ora_interogare_anterioara, lista_nume,
        lista_pret, ora_interogare)
    lista_nume_produs_anterioare, lista_preturi_produs_anterioare, ora_interogare_anterioara = produs_eliminat(
        lista_nume, lista_nume_produs_anterioare, lista_preturi_produs_anterioare, ora_interogare_anterioara)
    lista_preturi_produs_anterioare, ora_interogare_anterioara = update_preturi(lista_pret, ora_interogare,
                                                                                lista_nume_produs_anterioare,
                                                                                lista_preturi_produs_anterioare,
                                                                                ora_interogare_anterioara)
    # time.sleep(5)
    return lista_nume_produs_anterioare, lista_preturi_produs_anterioare, ora_interogare_anterioara
    # update_preturi(lista_pret)


def write_to_json(lista_nume_produs, lista_pret_produs, lista_ora_interogare):
    data = {}
    data['MediaGalaxy'] = []
    for i in range(len(lista_nume_produs)):
        data['MediaGalaxy'].append({
            'Nume Produs': lista_nume_produs[i],
            'Preturi Produs': lista_pret_produs[i],
            'Data Interogare': lista_ora_interogare[i]
        })
    with open('data.txt', 'w') as outfile:
        json.dump(data, outfile, indent=2)


if __name__ == '__main__':

    link_site = 'https://mediagalaxy.ro/telefoane/cpl/'
    options = webdriver.ChromeOptions()
    options.add_argument("start-maximized")
    options.add_argument("--headless")
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 ' \
                 'Safari/537.36 '
    options.add_argument(f'user-agent={user_agent}')
    driver = webdriver.Chrome(options=options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                                                                         'AppleWebKit/537.36 (KHTML, like Gecko) '
                                                                         'Chrome/85.0.4183.102 Safari/537.36'})
    driver = webdriver.Chrome(options=options)
    time.sleep(4)
    lista_nume_produs_anterioare, lista_preturi_produs_anterioare, ora_interogare_anterioara = get_site_info(driver,
                                                                                                             link_site)
    print(lista_nume_produs_anterioare, "\n", lista_preturi_produs_anterioare, "\n", ora_interogare_anterioara, "\n")

    while True:
        # print(lista_nume_produs_anterioare, lista_preturi_produs_anterioare, ora_interogare_anterioara)
        lista_nume_produs_anterioare, lista_preturi_produs_anterioare, ora_interogare_anterioara = interogari(
            lista_nume_produs_anterioare, lista_preturi_produs_anterioare, ora_interogare_anterioara, link_site, driver)
        print(lista_nume_produs_anterioare, "\n", lista_preturi_produs_anterioare, "\n", ora_interogare_anterioara,
              "\n")
        print("Done 1\n")
        time.sleep(2)
        write_to_json(lista_nume_produs_anterioare, lista_preturi_produs_anterioare, ora_interogare_anterioara)
        # time.sleep(10)
