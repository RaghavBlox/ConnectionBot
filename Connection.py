from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import time
import csv
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from fastapi import FastAPI, HTTPException
from fastapi import File, UploadFile

app = FastAPI()


@app.get("/open-linkedin-website")
async def open_linkedin_website():
    try:
        
        options = webdriver.ChromeOptions()
        #options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        driver = webdriver.Chrome(options=options)
        driver.get('https://www.linkedin.com')
        app.state.driver = driver
        time.sleep(2)
        return {"message": "LinkedIn website opened successfully."}
    except Exception as e:
        print("Exception: ", e)
        driver.save_screenshot("screenshot.png")
        


@app.post("/set-username-password")
async def set_username_password(username: str, password: str):
    try:
        driver = app.state.driver
        from selenium.webdriver.common.keys import Keys

        if not driver:
            raise HTTPException(status_code=400, detail="Driver not initialized. Open LinkedIn website first.")

        username_field = driver.find_element(By.XPATH, "//input[@name='session_key']")
        password_field = driver.find_element(By.XPATH, "//input[@name='session_password']")

        username_field.send_keys(username)
        password_field.send_keys(password)
        time.sleep(2)
        submit = driver.find_element(By.XPATH, "//button[@data-id='sign-in-form__submit-btn']").click()
        print('logged in')

        return {"message": "Username and password set successfully."}
    except Exception as e:
        print("Exception: ", e)
        driver.save_screenshot("screenshot.png")



# Function to send messages to connected people
def send_messages_to_connected(connection, messages) -> str:
    driver= app.state.driver
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
    driver= app.state.driver
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
    driver= app.state.driver
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


#send customised message according to csv file
@app.post("/upload-csv")
async def upload_csv(csv_file: UploadFile = File(...)):
    try:


        # Save the uploaded CSV file
        with open('uploaded.csv', 'wb') as f:
            f.write(await csv_file.read())

        return {"message": "CSV file uploaded successfully."}
    except Exception as e:
        return {"error": f"An error occurred while uploading the CSV file: {str(e)}"}

@app.post("/csv-messaging-functions")
async def run_messaging_functions():
    try:
        driver = app.state.driver
        if not driver:
            raise HTTPException(status_code=400, detail="Driver not initialized. Open LinkedIn website first.")

        csv_file_path = 'uploaded.csv'  # Use the uploaded CSV file
        print("csv readed")

        with open(csv_file_path, 'r', newline='', encoding='utf-8') as csvfile:
            csvreader = csv.DictReader(csvfile)

            for row in csvreader:
                connection = row['yourConnections']
                messages = row['Message']
                e = ''
                try:
                    e = send_messages_to_connected(connection, messages)
                    if e != '':
                        e = ''
                        e = send_messages_to_non_connected_with_connect(connection, messages)
                        if e != '':
                            send_messages_to_non_connected_without_connect(connection, messages)

                except Exception as e:
                    print(f"Error: {e}")

        # Close the browser when done
        driver.quit()
        return {"message": "Messaging functions completed successfully."}
    except Exception as e:
        print(f"Error: {e}")
        driver.save_screenshot("screenshot.png")
        return {"message": "Messaging functions completed successfully."}
    


#send connection request from filtered url link
#Eg: #https://www.linkedin.com/search/results/people/?geoUrn=%5B%22102713980%22%5D&origin=FACETED_SEARCH&serviceCategory=%5B%222461%22%2C%22220%22%2C%221836%22%2C%2250328%22%5D&page=2
@app.post("/connection-request")
async def connection_request(url: str, message: str):
    try: 
        driver = app.state.driver
        driver.get(url)

        wait = WebDriverWait(driver, 10)
        connect_buttons = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//button[contains(@class,'artdeco-button--secondary')]/span[text()='Connect']")))

        for btn in connect_buttons:
            try:
                btn.click()
                print('Connect button clicked')
                time.sleep(2)

                # Locate the <strong> tag within the parent element
                name_element = driver.find_element(By.XPATH, "//strong")
                
                # Extract the name from the <strong> tag
                name = name_element.text if name_element.is_displayed() else "LinkedIn User"
                print(name)

                # Click "Add a note" button
                addNote = driver.find_element(By.XPATH, "//button[@aria-label='Add a note']")
                driver.execute_script("arguments[0].click();", addNote)
                print('Add a note button clicked')
                time.sleep(2)

                # Add a personalized message with the name
                message_input = driver.find_element(By.XPATH, "//textarea[@name='message']")
                message = f"Hello {name}, {message}"
                message_input.send_keys(message)
                print(message)
                time.sleep(2)
                
                #Perform additional actions (e.g., sending a connection request)
                send = driver.find_element(By.XPATH, "//button[@aria-label='Send now']")
                driver.execute_script("arguments[0].click();", send)
                print('Next click')
                time.sleep(2)
                
                # close = driver.find_element(By.XPATH, "//button[@aria-label='Dismiss']")
                # driver.execute_script("arguments[0].click();", close)
                # print('Next click')
                time.sleep(2)
            except Exception as e:
                print(f"Error clicking button: {str(e)}")
    except Exception as e:
        print(f"Error: {e}")
        driver.save_screenshot("screenshot.png")
        return {"message": "Messaging connection request run successfully."}
