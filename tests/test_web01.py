import pytest
from seleniumaction import create_app
import multiprocessing as mp
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
import random
import socketio
import urllib.request

COUNTER = 0

@pytest.fixture()
def setup(request):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    request.cls.driver = driver
    yield request.cls.driver
    request.cls.driver.close()


@pytest.fixture()
def server():

    # port = random.randint(10000, 20000)
    global COUNTER
    port = 1234 + COUNTER
    COUNTER += 1

    # app, socketio = create_app()
    # app.config.update({
    #     "TESTING": False,
    # })
    
    def run_server():
        app, socketio = create_app()
        # app.config.update({
        #     "TESTING": False,
        # })
        socketio.run(app, port=port)

    # server_proc = mp.Process(
    #     target=socketio.run,
    #     args=(app,),
    #     kwargs={
    #         "debug": True,
    #         "port": port,
    #         "host": "0.0.0.0",
    #     },
    # )

    server_proc = mp.Process(
        target=run_server,
    )

    server_proc.start()
    time.sleep(5)
    yield f"http://localhost:{port}"
    server_proc.terminate()
    server_proc.join()


@pytest.mark.usefixtures("setup")
class TestExampleOne:

    def test_title(self, server):
        self.driver.get(server)
        assert self.driver.title == "Flask SocketIO Example"
        # get a div element with id="content"
        content = self.driver.find_element(By.ID,"content")
        # get the text from the div element
        assert content.text == "JS generated content"
    
    def test_socketio_connect(self, server):
        client = socketio.Client()
        client.connect(server)
        assert client.connected == True


