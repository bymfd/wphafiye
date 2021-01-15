from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
import base64
import time
import os
from datetime import datetime
from pathlib import Path

# Chrome driver yoluu tam girin
# isterseniz en güncel sürümü buradan indirebilirsiniz : https://chromedriver.chromium.org/
driverLocation = Path(__file__).parent / "chromedrivers/linux/chromedriver"


class Scraper:
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument("--window-size=1920x1080")
        chrome_options.add_argument("user-data-dir=~/Library/Application Support/Google/Chrome/Default/Cookies")
        self.driver = webdriver.Chrome(driverLocation)
        print("Whattsapp ekranı açılıyor ")
        self.driver.get('https://web.whatsapp.com')
        print("QR kodu okutup giriş yaptıktan sonra \"Yeni sohbet\" tuşuna basıp Enter' a basın ")
        input()

    def scrapeImages(self, name):
        try:

            contact_name = name
            try:
                contact = self.driver.find_element_by_xpath("//span[@title=\"" + contact_name + "\"]")
            except:
                print("İsim listede yok gibi arama kutusu deneniyor")
                search_box_xpath = '//div[@class="_1awRl copyable-text selectable-text"][@contenteditable="true"][@data-tab="3"]'
                search_box = WebDriverWait(self.driver, 50).until(
                    lambda driver: self.driver.find_element_by_xpath(search_box_xpath))
                search_box.click()
                search_box.send_keys(contact_name)
                time.sleep(2)
                contact = self.driver.find_element_by_xpath("//span[@title=\"" + contact_name + "\"]")
            contact.click()
            print("Kişi Bulundu")
            menu = self.driver.find_element_by_xpath("(//div[@title=\"Diğer seçenekler\"])[2]")
            menu.click()
            time.sleep(2)
            try:
                info = self.driver.find_element_by_xpath("//div[@title=\"Kişi bilgisi\"]")
            except:
                info = self.driver.find_element_by_xpath("//div[@title=\"Grup bilgisi\"]")
            info.click()
            time.sleep(1)
            numara = self.driver.find_element_by_xpath('//*[@id="app"]/div/div/div[2]/div[3]/span/div/span/div/div/div[1]/div[4]/div[3]/div/div/span/span').text
            print ("Kişi Numarası: "+numara)

            print("==================Resim Kaydı Deneniyor====================")
            while True:
                try:

                    image_xpath = '//img[@class="_3t3gU rlUm6 _1VzZY"]'
                    image = WebDriverWait(self.driver, 20).until(
                        lambda driver: self.driver.find_element_by_xpath(image_xpath))
                    image_src = image.get_attribute("src")
                    image_name = image_src.rsplit('/', 1)[
                        1]  
                    result = self.driver.execute_async_script("""
                        var uri = arguments[0];
                        var callback = arguments[1];
                        var toBase64 = function(buffer){for(var r,n=new Uint8Array(buffer),t=n.length,a=new Uint8Array(4*Math.ceil(t/3)),i=new Uint8Array(64),o=0,c=0;64>c;++c)i[c]="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/".charCodeAt(c);for(c=0;t-t%3>c;c+=3,o+=4)r=n[c]<<16|n[c+1]<<8|n[c+2],a[o]=i[r>>18],a[o+1]=i[r>>12&63],a[o+2]=i[r>>6&63],a[o+3]=i[63&r];return t%3===1?(r=n[t-1],a[o]=i[r>>2],a[o+1]=i[r<<4&63],a[o+2]=61,a[o+3]=61):t%3===2&&(r=(n[t-2]<<8)+n[t-1],a[o]=i[r>>10],a[o+1]=i[r>>4&63],a[o+2]=i[r<<2&63],a[o+3]=61),new TextDecoder("ascii").decode(a)};
                        var xhr = new XMLHttpRequest();
                        xhr.responseType = 'arraybuffer';
                        xhr.onload = function(){ callback(toBase64(xhr.response)) };
                        xhr.onerror = function(){ callback(xhr.status) };
                        xhr.open('GET', uri);
                        xhr.send();
                        """, image_src)
                    if type(result) == int:
                        raise Exception("İstek Reddedildi %s" % result)
                    final_image = base64.b64decode(result)
                    filename = 'images/' +numara.strip("+").strip()+ '.jpg'  # I assume you have a way of picking unique filenames
                    with open(filename, 'wb') as f:
                        f.write(final_image)
                        print("Kaydediliyor " + filename + "")

                    close_image_button = self.driver.find_element_by_xpath('//div[@title="Yeni sohbet"]')
                    close_image_button.click()

                except Exception as e:
                    try:
                        close_image_button = self.driver.find_element_by_xpath('//div[@title="Yeni sohbet"]')
                        close_image_button.click()

                    except Exception as err:
                        print("")

                        break

        except Exception as e:
            print(e)
            self.driver.quit()

    def quitDriver(self):
        print("Quit")
        self.driver.quit()
os.system('clear')
print ("""

                                     
TR Whatsapp profil potoğrafı kaydedici
                                 
    )               (      (     
 ( /(  (        )   )\ )   )\ )  
 )\()) )\ )    (   (()/(  (()/(  
((_)\ (()/(    )\  '/(_))  ((_)) 
| |(_) )(_)) _((_))(_) _|  _| |  
| '_ \| || || '  \()|  _|/ _` |  
|_.__/ \_, ||_|_|_| |_|  \__,_|  
       |__/                      




""")

scraper = Scraper()
isimler = ["Aa", "Yusuf"]



for i in isimler:
    print("===================Yeni Kişi Deneniyor=================")

    scraper.scrapeImages(i)

