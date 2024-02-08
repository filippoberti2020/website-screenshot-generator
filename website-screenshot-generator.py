from flask import Flask, render_template, request, send_file
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os

app = Flask(__name__)

options = webdriver.ChromeOptions()
options.headless = True
driver = webdriver.Chrome(options=options)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/screenshot', methods=['POST'])
def screenshot():
    url = request.form['url']
    screenshot_type = request.form['screenshotType']
    
    driver.get(url)
    
    if screenshot_type == 'fullpage':
        # Add code to capture full page screenshot
        # Refer to the search results for capturing a full page screenshot
        # Save the screenshot to a file
        driver.save_screenshot('full_page_screenshot.png')
    else:
        # Capture visible area screenshot
        S = lambda X: driver.execute_script('return document.body.parentNode.scroll'+X)
        driver.set_window_size(S('Width'),S('Height'))
        driver.find_element_by_tag_name('body').screenshot('visible_area_screenshot.png')

    driver.quit()
    
    # Provide the user with the option to download the screenshot
    if screenshot_type == 'fullpage':
        return send_file('full_page_screenshot.png', as_attachment=True)
    else:
        return send_file('visible_area_screenshot.png', as_attachment=True)

if __name__ == '__main__':
    app.run()
