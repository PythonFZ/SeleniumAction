import pytest
from seleniumaction import create_app
import multiprocessing as mp
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time

@pytest.fixture()
def setup(request):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    request.cls.driver = driver
    yield request.cls.driver
    request.cls.driver.close()

# @pytest.fixture()
# def client():
#     app, socketio = create_app()
#     app.config.update({
#         "TESTING": True,
#     })

#     # other setup can go here

#     yield socketio.test_client(app)

@pytest.mark.usefixtures("setup")
class TestExampleOne:
    def test_title(self):
        app, socketio = create_app()
        app.config.update({
            "TESTING": True,
        })
        server_proc = mp.Process(
            target=socketio.run,
            args=(app,),
            kwargs={
                "debug": True,
                "port": 5000,
                "host": "0.0.0.0",
            },
        )
        server_proc.start()
        time.sleep(3)


        self.driver.get("http://localhost:5000")
        assert self.driver.title == "Flask SocketIO Example"
        # get a div element with id="content"
        content = self.driver.find_element(By.ID,"content")
        # get the text from the div element
        assert content.text == "JS generated content"

        server_proc.terminate()

# def test_edit_user(client):
    # app, socketio = create_app()
    # app.config.update({
    #     "TESTING": True,
    # })
    # server_proc = mp.Process(
    #     target=socketio.run,
    #     args=(app,),
    #     kwargs={
    #         "debug": True,
    #         "port": 5000,
    #         "host": "0.0.0.0",
    #     },
    # )
    # server_proc.start()




    # response = client.app.test_client().get("/")
    # assert response.status_code == 200
    # assert b"Flask SocketIO Example" in response.data
    # assert b"JS generated content" in response.data
