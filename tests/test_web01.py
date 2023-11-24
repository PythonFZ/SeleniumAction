import pytest
from seleniumaction import create_app
import multiprocessing as mp
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import socketio
import random
import copy

PORT = copy.deepcopy(int(random.randint(5000, 6000)))
# PORT = 5322

@pytest.fixture()
def setup():
    app, socketio = create_app()

    server_proc = mp.Process(
        target=socketio.run,
        args=(app,),
        kwargs={
            "debug": True,
            "port": PORT,
            "host": "0.0.0.0",
        },
    )
    server_proc.start()

    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    yield driver
    driver.close()
    server_proc.terminate()

def test_title(setup):
    driver = setup
    driver.get(f"http://localhost:{PORT}")
    assert driver.title == "Flask SocketIO Example"
    # get a div element with id="content"
    content = driver.find_element(By.ID,"content")
    # get the text from the div element
    assert content.text == "JS generated content"

# def test_connect_socketio(setup):
#     client = socketio.Client()
#     client.connect(f"http://localhost:{PORT}")
#     assert client.connected