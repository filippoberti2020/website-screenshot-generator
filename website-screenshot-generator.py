from flask import Flask, render_template, request, send_file
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os

app = Flask(__name__)

options = webdriver.ChromeOptions()
options.headless = True
driver = webdriver.Chrome(options=options)


def modify_url(url):
    if not url.startswith('http'):
        url = 'https://' + url
    if not url.startswith('www.'):
        url = url.replace('://', '://www.')
    return url


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/screenshot', methods=['POST'])
def screenshot():
    url = request.form['url']
    url = modify_url(url)  # Modify the URL to handle differents user input
    screenshot_type = request.form['screenshotType']
    
    driver.get(url)
    
    if screenshot_type == 'fullpage':
        # Add code to capture full page screenshot
        # Refer to the search results for capturing a full page screenshot
        # Save the screenshot to a file
        width=1920
        height= driver.execute_script("return Math.max( document.body.scrollHeight, document.body.offsetHeight, document.documentElement.offsetHeight);")
        driver.set_window_size(width,height)
        page_body=driver.find_element(By.TAG_NAME,"body")
        page_body.screenshot("full_page_screenshot.png")
        
    else:
        # Capture visible area screenshot
        driver.set_window_size(1920,1080)
        driver.save_screenshot('visible_area_screenshot.png')


    driver.quit()
    
    # Provide the user with the option to download the screenshot
    if screenshot_type == 'fullpage':
        return send_file('full_page_screenshot.png', as_attachment=True)
    else:
        return send_file('visible_area_screenshot.png', as_attachment=True)

if __name__ == '__main__':
    app.run()
