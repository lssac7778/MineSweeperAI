# -*- coding: utf-8 -*-
"""
Created on Sat Nov 23 18:02:19 2019

@author: Isaac
"""

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.action_chains import ActionChains


from bs4 import BeautifulSoup
import time
import random
from abc import *

from main import MineSweeperAI, MineGround

def initDriver():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")
    driver = webdriver.Chrome('chromedriver', chrome_options=chrome_options)
    return driver


 
class MinsweeperWebEnv(metaclass=ABCMeta):
    @abstractmethod
    def getPane(self, driver, size):
        pass
 
    @abstractmethod
    def checkBombIndex(self, driver, pos):
        pass

    @abstractmethod
    def resetGame(self, driver):
        pass


class minesweeperonline(MinsweeperWebEnv):
    link = "http://minesweeperonline.com"

    def getPane(self, driver):
        ai = MineSweeperAI()
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        
        game = soup.find('div', {'id':'game'})
        posvals = []
        
        done = False
        
        maxx = -1
        maxy = -1
        
        for block in game.find_all('div', {'class':'square'}):
            
            text = block['id']
            idx = text.index("_")
            x = int(text[:idx])
            y = int(text[idx+1:])
            if x < 1 or y < 1:
                continue
            
            maxx = max(maxx, x)
            maxy = max(maxy, y)

            
            x ,y = x-1, y-1
            bclass = block['class'][1]
            if "open" in bclass:
                
                num = bclass[bclass.index("open") + 4:]
                num = int(num)
                posvals.append((x, y, str(num)))
            
            elif "bombflagged" in bclass:
                posvals.append((x, y, ai.flag))
            
            elif "bombrevealed" in bclass or "bombdeath" in bclass:
                posvals.append((x, y, ai.bomb))
                done = True
        
        
        pane = [[ai.block for _ in range(maxy)] for _ in range(maxx)]
        
        for x, y, val in posvals:
            pane[x][y] = val
        
        self.pane = pane
        return pane, done
    
    def checkBombIndex(self, driver, pos):
        idd = str(pos[0]+1) + "_" + str(pos[1]+1)
        
        # button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, idd)))
        
        btn = driver.find_elements_by_xpath('//*[@id="' + idd + '"]')
        button = btn[0]
        button.click()

        # ActionChains(driver).move_to_element(button).click(button).perform()
        
        # try:
        #     button.click()
        # except:
        #     try:
        #         button.send_keys(Keys.ENTER)
        #     except:
        #         driver.execute_script("arguments[0].click();", button)
        #         time.sleep(0.1)
    
    def flagIndex(self, driver, poses):
        actionChains = ActionChains(driver)
        for pos in poses:
            idd = str(pos[0]+1) + "_" + str(pos[1]+1)
            btn = driver.find_elements_by_id(idd)[0]
            actionChains = actionChains.move_to_element(btn).context_click(btn)
        
        actionChains.perform()
    
    
    def resetGame(self, driver):
        try:
            btn = driver.find_element_by_class_name("facedead")
        except:
            try:
                btn = driver.find_element_by_class_name("facewin")
            except:
                btn = driver.find_element_by_class_name("facesmile")
                
        btn.click()

class minesweeperdotonline(MinsweeperWebEnv):
    link = "https://minesweeper.online/"
    
    def getPane(self, driver):
        ai = MineSweeperAI()
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        
        game = soup.find('div', {'id':'game'})
        posvals = []
        done = False
        
        
        maxi, maxj = 0, 0

        for cell in game.find_all('div', {'class':'cell'}):
                
            i,j = int(cell['data-x']), int(cell['data-y'])
            classd = cell['class']
            
            maxi = max(maxi, i)
            maxj = max(maxj, j)
            
            if "hd_opened" in classd:
                hdtype = int(classd[-1][len("hd_type"):])
                if hdtype==10 or hdtype==11:
                    posvals.append((i, j, ai.bomb))
                    done = True
                else:
                    posvals.append((i, j, str(hdtype)))
        

        pane = [[ai.block for _ in range(maxj+1)] for _ in range(maxi+1)]
        
        
        for i, j, val in posvals:
            pane[i][j] = val
        
        return pane, done
    
    def checkBombIndex(self, driver, pos):
        idd = "cell_" + str(pos[0]) + "_" + str(pos[1])
        btn = driver.find_elements_by_id(idd)
        btn[0].click()

    def resetGame(self, driver):
        btn = driver.find_element_by_id("top_area_face")
        btn.click()


if __name__=="__main__":
    ai = MineSweeperAI()
    mg = MineGround()
    env = minesweeperonline()
    
    driver = initDriver()
    
    driver.get(env.link)
    da = Alert(driver)
    print("start")
    time.sleep(3)
    # input("enter to start")
    
    playnum = 1
    # delay = (0.07, 0.10)
    delay = (0, 0)

    
    for _ in range(playnum):
        env.resetGame(driver)
        time.sleep(2)
        pane, done = env.getPane(driver)
        allbomb = []
        while not done:
            
            b, nb = ai.main(pane)
            allbomb += b
            for notbomb in nb:
                time.sleep(random.uniform(*delay))
                env.checkBombIndex(driver, tuple(notbomb))
            
            pane, done = env.getPane(driver)
            for nx, ny in allbomb:
                pane[nx][ny] = ai.flag





