import subprocess
from pathlib import Path

import selenium
import selenium.webdriver
import sys
import time


def book_zion_shuttle():
    options = selenium.webdriver.chrome.options.Options()
    options.add_argument("start-maximized")

    node_modules_bin = subprocess.run(
        ["npm", "bin"],
        stdout=subprocess.PIPE,
        universal_newlines=True,
        check=True
    )
    node_modules_bin_path = node_modules_bin.stdout.strip()
    chromedriver_path = Path(node_modules_bin_path) / "chromedriver"

    driver = selenium.webdriver.Chrome(
        options=options,
        executable_path=str(chromedriver_path),
    )

    driver.get("https://www.recreation.gov/ticket/300016/ticket/3010")

    # TODO: log in to recreation.gov, and set account_info equal to value associated w/ recaccount key in Local Storage. 
    # Store it as a string. It should start with {"access token": ....
    account_info = ""

    script = "localStorage.setItem('recaccount', '{}');".format(account_info)

    driver.execute_script(script)

    driver.get("https://www.recreation.gov/ticket/300016/ticket/3010")

    # 1618268400

    while time.time() < 1618585200:
        time.sleep(0.1)

    print("let's gooooo")

    driver.get("https://www.recreation.gov/ticket/300016/ticket/3010")

    input_element = driver.find_element_by_xpath("//input[@name='tourCalendarWithKey']")

    # TODO: Set the date in MM/DD/YYYY format
    input_element.send_keys("04/16/2021")

    drop_down = driver.find_element_by_xpath("//*[@id='guest-counter']")
    drop_down.click()

    num_guests = driver.find_element_by_xpath("//*[@id='guest-counter-number-field-General Public']")
    num_guests.clear()

    # TODO: Set the number of shuttle passes 
    num_guests.send_keys("1")

    close_button = driver.find_element_by_xpath("//*[@id='guest-counter-popup']/div/div[2]/div/button")
    close_button.click()    

    # TODO: Update xpath for real time slot
    time_slot = driver.find_elements_by_xpath("//input[@type='radio']")
    while len(time_slot) == 0:
        time_slot = driver.find_elements_by_xpath("//input[@type='radio']")

    action = selenium.webdriver.common.action_chains.ActionChains(driver)

    action.move_to_element_with_offset(time_slot[2],8,10)

    action.click()
    action.perform()

    for input in sys.stdin:
        if input.rstrip() == "quit":
            time_slot.click()
            return


if __name__ == "__main__":
    book_zion_shuttle()
