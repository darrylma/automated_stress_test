#!/usr/bin/python
import re
import os
import sys
import time
import requests
from time import gmtime, strftime
from mechanize import Browser
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from flask import Flask, render_template, redirect, url_for,request
from flask import make_response
app = Flask(__name__)
br = Browser()
cwd = os.getcwd()

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
chrome_options = Options()
chrome_options.add_experimental_option('prefs', {
    'credentials_enable_service': False,
    'profile': {
        'password_manager_enabled': False
    }
})

def open_MCP(MSISDN):
    with open('log_file.txt', 'a') as logfile:
        logfile.write("Testing with MSISDN " + MSISDN + "\n")

    # Ignore robots.txt
    br.set_handle_robots( False )
    # Google demands a user-agent that isn't a robot
    br.addheaders = [('User-agent', 'Firefox')]

    # Retrieve the Google home page, saving the response
    #br.open( "http://google.com" )
    driver = webdriver.Chrome("chromedriver.exe", chrome_options=chrome_options)
    driver.get("https://mcp.digi.com.my/DigiPortal/appmanager/MCP/Web")

    # Login to MCP
    #driver.find_element_by_id("username").send_keys("DARRYLMA")
    #driver.find_element_by_id("password").send_keys("DARRYLMA1985!x1")
    driver.find_element_by_id("username").send_keys("SOONJENN")
    driver.find_element_by_id("password").send_keys("H8peless#")
    driver.find_element_by_id('loginButton').click()

    # Search for customer quota
    time.sleep(1)
    element_to_hover = driver.find_element_by_link_text("Post Sales Service")
    hover = ActionChains(driver).move_to_element(element_to_hover)
    hover.perform()

    driver.find_element_by_link_text("Internet Services").click()
    driver.find_element_by_id("msisdn").send_keys(MSISDN)
    driver.find_element_by_xpath("//button[contains(text(),'Retrieve Quota')]").click()

    time.sleep(1)
    #quota_table = driver.find_element_by_xpath('//form[@id="subcriberInfo"]/table/tbody')
    row_count = len(driver.find_elements_by_xpath("//form[@id='subcriberInfo']/table/tbody/tr"))
    #print row_count

    i=0
    result = strftime("%Y-%m-%d %H:%M:%S\n", time.localtime())
    result = result + 'MSISDN: ' + MSISDN + '\n'
    while i < row_count-1:
        i+=1
        print "\n"
        quota_description = driver.find_element_by_xpath('//form[@id="subcriberInfo"]/table/tbody/tr[' + str(i+1) + ']/td[2]').text
        quota_balance = driver.find_element_by_xpath('//form[@id="subcriberInfo"]/table/tbody/tr[' + str(i+1) + ']/td[5]').text
        quota_consumed = driver.find_element_by_xpath('//form[@id="subcriberInfo"]/table/tbody/tr[' + str(i+1) + ']/td[6]').text
        quota_total = driver.find_element_by_xpath('//form[@id="subcriberInfo"]/table/tbody/tr[' + str(i+1) + ']/td[7]').text

        quota_description_string = quota_description
        if len(quota_balance) > 5:
            quota_balance_string = quota_balance[:-5] + "," + quota_balance[-5:]
        else:
            quota_balance_string = quota_balance
        quota_consumed_string = quota_consumed
        quota_total_string = quota_total[:-5] + "," + quota_total[-5:]

        with open('log_file.txt', 'a') as logfile:
            logfile.write(strftime("  %Y-%m-%d %H:%M:%S\n", time.localtime()))
            logfile.write(quota_description_string + "\n")
            logfile.write(quota_balance_string + "\n")
            logfile.write(quota_consumed_string + "\n")
            logfile.write(quota_total_string + "\n\n")

        result_one = quota_description_string + ": " + quota_balance_string + "/" + quota_total_string + " MB\n"
        result += result_one

    driver.close()
    result += '\n'
    return result

def create_log_file():
    with open('log_file.txt', 'w') as logfile:
        logfile.write("Start Testing\n")
        logfile.write(strftime("%Y-%m-%d %H:%M:%S\n\n", time.localtime()))

def close_log_file():
    with open('log_file.txt', 'a') as logfile:
        logfile.write("End Testing\n")
        logfile.write(strftime("%Y-%m-%d %H:%M:%S\n\n", time.localtime()))
    logfile.close()

def downloadFile(url, directory) :
  localFilename = url.split('/')[-1]
  with open(directory + '/' + localFilename, 'wb') as f:
    start = time.clock()
    r = requests.get(url, stream=True)
    total_length = r.headers.get('content-length')
    print total_length
    dl = 0
    if total_length is None: # no content length header
      f.write(r.content)
    else:
      for chunk in r.iter_content(1024):
        dl += len(chunk)
        f.write(chunk)
        #done = int(50 * int(dl) / int(total_length))
        #sys.stdout.write("\r[%s%s] %s bps" % ('=' * done, ' ' * (50-done), dl//(time.clock() - start)))
        #print ''
  return ((time.clock() - start),total_length)

def watchVideo(url) :
    # Ignore robots.txt
    br.set_handle_robots( False )
    # Google demands a user-agent that isn't a robot
    br.addheaders = [('User-agent', 'Firefox')]

    # Retrieve the Google home page, saving the response
    #br.open( "http://google.com" )
    driver = webdriver.Chrome("chromedriver.exe", chrome_options=chrome_options)
    if url.find("youtube"):
        driver.get(url+"?rel=0&autoplay=1")
    driver.get(url)
    start = time.clock()
    play_button = driver.find_element_by_xpath('//div[@class="ytp-left-controls"]/button')
    value = play_button.get_attribute("aria-label")
    while value == "Pause":
        time.sleep(1)
        value = play_button.get_attribute("aria-label")
    driver.close()
    return ((time.clock() - start))

@app.route('/')
def showMainPage():
    return render_template('index.html')

@app.route('/check_quota', methods=['GET', 'POST'])
def check_quota():
    if request.method == 'POST':
        MSISDN = request.form['param']
        create_log_file()
        result = open_MCP(MSISDN)
        resp = make_response('{"response": '+result+'}')
        resp.headers['Content-Type'] = "application/json"
        close_log_file()
        return resp

@app.route('/check_speed', methods=['GET', 'POST'])
def check_speed():
    if request.method == 'POST':
        if len(sys.argv) > 1 :
              url = sys.argv[1]
        else :
              url = "http://digiretail.azurewebsites.net/video/twilight.mp4"
        directory = cwd + "\Downloads"
        (time_elapsed, filesize) = downloadFile(url, directory)
        result = strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        result = result + "\nDownload Speed " + str(round(float(filesize)/time_elapsed/1024,2)) + " kBps\n\n"
        resp = make_response('{"response": '+result+'}')
        resp.headers['Content-Type'] = "application/json"
        return resp

@app.route('/download', methods=['GET', 'POST'])
def download():
    if request.method == 'POST':
        url = request.form['param']
        directory = cwd + "\Downloads"
        (time_elapsed, filesize) = downloadFile(url, directory)
        result = strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        result = result + "\nDownloaded " + str(round(float(filesize)/1024/1024,2)) + " MB file\n\n"
        resp = make_response('{"response": '+result+'}')
        resp.headers['Content-Type'] = "application/json"
        return resp

@app.route('/watch', methods=['GET', 'POST'])
def watch():
    if request.method == 'POST':
        url = request.form['param']
        time_elapsed = watchVideo(url)
        result = strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        result = result + "\nWatched video for " + str(round(time_elapsed,0)) + " seconds\n\n"
        resp = make_response('{"response": '+result+'}')
        resp.headers['Content-Type'] = "application/json"
        return resp

if __name__ == "__main__":
    app.run(debug = True)
    app.run(host='0.0.0.0', port=5000)
