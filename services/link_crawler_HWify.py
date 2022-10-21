import re
import sys
import time
import os
import pyperclip
from services.constants import N_QUESTIONS_CRAWLE_SUCCESSFULLY, NO_QUESTION_YET, GENERAL_ERROR
from services.slack import Slack
from bs4 import BeautifulSoup
from repository.Model.Question import Question
from repository.question_repository import QuestionRepository
import pyautogui
import webbrowser
import subprocess
from services import image_service
from util.browser_driver import BrowserDriver
from util.mysql_db_manager import MySqlDBManager
from selenium.webdriver.common.by import By
from services.constants import chrome_path
from services.constants import firefox_path
from services.constants import search_url
from services.constants import main_url
from services.constants import storagePath
from services.constants import cookiePath
from services.constants import sessionPath

question_repository = QuestionRepository()
mysql_db_manager = MySqlDBManager('admin',
                                  'QuizPlus123',
                                  'quizplusdevtestdb.c4m3phz25ns8.us-east-1.rds.amazonaws.com',
                                  'chegg_general_crawler',
                                  '3306')


class HWifyCrawler:
    def _start_crawling(self):
        flag = 0
        dx, dy = self.set_resolution()
        time.sleep(1)
        while True:
            # Comment: Here the first K not-crawled questions retrived which is better than hitting everytime on DB to get first not crawled
            questions = question_repository.get_first_not_answer_retrived_k_questions(mysql_db_manager, 1000)
            try:
                for question in questions:
                    flag = 1
                    self.pyautogui_search(dx,dy,question)
                    # self.selenium_search(question)


            except Exception as e:
                print(str(e))
                # Slack().send_message_to_slack(GENERAL_ERROR, str(e))
                sys.exit()
            if flag == 0:
                print("Sorry But there is no question yet, wait the crawling process")
                # Slack().send_message_to_slack(NO_QUESTION_YET, " ")

    def set_resolution(self):
        dx, dy = image_service.get_resolution()
        return dx, dy

    def pyautogui_search(self, dx, dy, question):
        # get url from Database and copy it
        webbrowser.open_new("https://homeworkify.net/")
        time.sleep(5)
        pyautogui.scroll(-600)
        time.sleep(5)
        pyautogui.moveTo(dx * 590, dy * 190, 1)
        time.sleep(1)
        pyautogui.click(button='left')
        time.sleep(.3)
        pyautogui.typewrite(question.url)
        pyautogui.moveTo(dx * 1300, dy * 190, 1)
        time.sleep(1)
        pyautogui.click(button='left')
        time.sleep(1)
        status = self._save_web_page(dx, dy)
        if status.find("No solution found!") != -1:
            #no answer
            print("no answer")
        elif status.find("We have solution for your question!") != -1:
            print("answer found")
            time.sleep(30)
        else:
            print("unknown")
            time.sleep(30)




    def selenium_search(self, question):
        driver = BrowserDriver().driver
        driver.get("https://homeworkify.net/")
        driver.maximize_window()
        time.sleep(2)
        element = driver.find_element(By.ID, 'hw-header-input')
        element.send_keys(question.url)
        time.sleep(1)
        element = driver.find_element(By.CLASS_NAME, 'hw-header-button')
        element.click()
        time.sleep(2)
        try:
            status = driver.find_element(By.XPATH,
                                         '//*[@id="et-boc"]/div/div/div[1]/div[2]/div/div[1]/div/div[2]/div/h2').text
            if status == 'We have solution for your question!':
                # there is an answer, so we open it and store it
                time.sleep(30)
                element = driver.find_element(By.ID, 'view-solution')
                element.click()
                time.sleep(2)
            elif status == 'No solution found!':
                # there is no solution
                print("there is No solution")

        except Exception as e:
            print("there is an Error")

    def _save_web_page(self, dx, dy):
            pyperclip.copy("")

            # print("clicking to get soruce html")
            # time.sleep(1)
            # pyautogui.hotkey('ctrl', 'u')
            # time.sleep(1)
            # pyautogui.moveTo(dx * 400, dy * 420, 1)
            # pyautogui.click(button='left')
            # # html = pyautogui.hotkey('ctrl', 'a')
            # time.sleep(1)
            pyautogui.hotkey('ctrl', 'a')
            time.sleep(1)
            pyautogui.hotkey('ctrl', 'c')
            time.sleep(1)
            html = pyperclip.paste()
            time.sleep(1)
            pyautogui.moveTo(dx * 1500, dy * 190, 1)
            pyautogui.click(button='left')
            time.sleep(1)
            #pyautogui.hotkey('ctrl', 'w')
            return html