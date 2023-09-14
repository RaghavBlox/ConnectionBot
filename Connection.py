from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import time
import csv
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

options = webdriver.ChromeOptions()
driver = webdriver.Chrome(options=options)
driver.get('https://www.linkedin.com')
time.sleep(2)

username = driver.find_element(By.XPATH, "//input[@name='session_key']")
password = driver.find_element(By.XPATH, "//input[@name='session_password']")


username.send_keys('EmailorUsername')
password.send_keys('Password')
time.sleep(2)

submit = driver.find_element(By.XPATH, "//button[@type='submit']").click()
print('logged in')


# Define the CSV file path
csv_file_path = 'test.csv'

# Function to send messages to connected people
def send_messages_to_connected(connection, messages) -> str:
    driver.get(connection)
    wait = WebDriverWait(driver, 10)
    error= ''
    try:
        h1_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "h1"))
        )
        name = h1_element.text

        # Wait for the "Message" button to appear
        message_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//button[contains(@class,'artdeco-button--primary')]/span[text()='Message']"))
        )
        # message_button.click()
        driver.execute_script("arguments[0].click();", message_button)

        message_input = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@role='textbox' and @aria-multiline='true']")))
        message_input.click()

        #type message
        paragraphs = driver.find_elements(By.TAG_NAME,"p")
        paragraphs[-5].send_keys(messages)


        #send message
        submit = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div button.msg-form__send-button'))
        )
        time.sleep(2)
        driver.execute_script("arguments[0].click();", submit)
        print('Next click')
        time.sleep(2)

        #close button
        close_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'msg-overlay-bubble-header__control') and ( contains(., 'Close your conversation') or contains(., 'Close your draft conversation'))]")))
        driver.execute_script("arguments[0].click();", close_button)
        time.sleep(2)
    except Exception as e:
        error = f"Error: {e}"
        print(f"Error: {e}")
    return error

# Function to send messages to non-connected people with connect button
def send_messages_to_non_connected_with_connect(connection, messages)-> str:
    driver.get(connection)
    wait = WebDriverWait(driver, 10)
    error =''
    try:
        h1_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "h1"))
        )
        name = h1_element.text

        connect_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, f'//button[@aria-label="Invite {name} to connect"]'))
        )
        driver.execute_script("arguments[0].click();", connect_button)

        addNote = driver.find_element(By.XPATH, "//button[@aria-label='Add a note']")
        driver.execute_script("arguments[0].click();", addNote)
        print('Add a note button clicked')
        time.sleep(2)

        message_input = driver.find_element(By.XPATH, "//textarea[@name='message']")
        message = f"Hello {name}, {messages}"
        message_input.send_keys(message)
        print(message)
        time.sleep(2)

        send = driver.find_element(By.XPATH, "//button[@aria-label='Send now']")
        driver.execute_script("arguments[0].click();", send)
        print('Next click')
        time.sleep(2)
    except Exception as e:
        error = f"Error: {e}"
        print(f"Error: {e}")
    return error

# Function to send messages to non-connected people without connect button
def send_messages_to_non_connected_without_connect(connection, messages):
    driver.get(connection)
    wait = WebDriverWait(driver, 10)
    try:
            h1_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "h1"))
            )
            name = h1_element.text

            #more button
            more_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, f'//button[@aria-label="More actions"]'))
            )
            driver.execute_script("arguments[0].click();", more_button)

            #connect button
            connect_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, f'div[aria-label="Invite {name} to connect"]'))
            )
            driver.execute_script("arguments[0].click();", connect_button)

            # Click "Add a note" button
            addNote = driver.find_element(By.XPATH, "//button[@aria-label='Add a note']")
            driver.execute_script("arguments[0].click();", addNote)
            print('Add a note button clicked')
            time.sleep(2)

            # Add a personalized message with the name
            message_input = driver.find_element(By.XPATH, "//textarea[@name='message']")
            message = f"Hello {name}, {messages}"
            message_input.send_keys(message)
            print(message)
            time.sleep(2)
                
            #Perform additional actions (e.g., sending a connection request)
            send = driver.find_element(By.XPATH, "//button[@aria-label='Send now']")
            driver.execute_script("arguments[0].click();", send)
            print('Next click')
            time.sleep(2)
    except Exception as e:
        print(f"Error: {e}")

# Open the CSV file and process each row
with open(csv_file_path, 'r', newline='', encoding='utf-8') as csvfile:
    csvreader = csv.DictReader(csvfile)
    
    for row in csvreader:
        connection = row['yourConnections']
        messages = row['Message']
        e=''
        try:
            e = send_messages_to_connected(connection, messages)
            if e != '':
                e =''
                e = send_messages_to_non_connected_with_connect(connection, messages)
                if e!= '':
                    send_messages_to_non_connected_without_connect(connection, messages)

        except Exception as e:
            print(f"Error: {e}")

# Close the browser when done
driver.quit()