from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def send_callback(driver,url):
    driver.get(url)
    driver.maximize_window()
    time.sleep(3)
    driver.execute_script("window.scrollTo(0, 400);")
    WebDriverWait(driver, 200).until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[2]/div[1]/button')))
    driver.find_element_by_class_name("call_doc_btn").click()
    WebDriverWait(driver, 200).until(EC.visibility_of_element_located((By.ID, "send_request_to_doctor")))
    form = driver.find_element_by_id("send_request_to_doctor")
    rows = form.find_elements_by_class_name('form-control')
    rows[0].send_keys('test')
    rows[1].send_keys('test@test.com')
    rows[2].send_keys('test')
    rows[3].send_keys('test')
    form.find_element_by_css_selector('button').click()
    WebDriverWait(driver, 200).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="call_a_doctor"]/div/div/div/p')))
    if driver.find_element_by_xpath('//*[@id="call_a_doctor"]/div/div/div/p').is_displayed():
        return 'success'
    else:
        return 'fail'

def send_offer(driver,url):
    driver.get(url)
    WebDriverWait(driver, 200).until(EC.visibility_of_element_located((By.CLASS_NAME, "h_o_s")))
    form = driver.find_element_by_css_selector("div.request_step.request_inner_1")
    form.find_element_by_id('dis').send_keys('test')
    form.find_element_by_id('desc').send_keys('test')
    driver.find_element_by_css_selector('button.btn.btn-raised.btn-primary.h_o_s').click()
    # WebDriverWait(driver, 200).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="call_a_doctor"]/div/div/div/p')))
    # driver.close()
    WebDriverWait(driver, 200).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div.request_step.request_inner_2")))
    form = driver.find_element_by_css_selector("div.request_step.request_inner_2")
    divs = form.find_elements_by_css_selector('div.row')
    rows = divs[0].find_elements_by_css_selector('div.form-group.label-floating.is-empty > input.form-control')
    rows[0].send_keys('test')
    rows[1].send_keys('test')
    rows[2].send_keys('5')
    rows = divs[1].find_elements_by_css_selector('div.form-group.label-floating.is-empty > input.form-control')
    rows[0].send_keys('test')
    rows[1].send_keys('test')

    rows = divs[3].find_elements_by_css_selector('div.form-group.label-floating.is-empty > input.form-control')
    rows[0].send_keys('test')
    rows[1].send_keys('test')
    rows = divs[4].find_elements_by_css_selector('div.form-group.label-floating.is-empty > input.form-control')
    rows[0].send_keys('test@test.com')
    rows[1].send_keys('test')
    driver.find_element_by_css_selector('button.btn.btn-raised.btn-warning.h_o_s.request_send').click()
    WebDriverWait(driver, 200).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div.thx')))
    if driver.find_element_by_css_selector('div.thx').is_displayed():
        return 'success'
    else:
        return 'fail'
driver = webdriver.PhantomJS()
print ('russian callback:',send_callback(driver,"https://bookinghealth.ru/"))
print ('russian get offer:',send_offer(driver,"https://bookinghealth.ru/order"))
print ('english callback:',send_callback(driver,"https://bookinghealth.com/"))
print ('english get offer:',send_offer(driver,"https://bookinghealth.com/order"))
driver.close()