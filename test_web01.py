import pytest


@pytest.mark.usefixtures("setup")
class TestExampleOne:
    def test_title(self):
        self.driver.get('https://github.com/pythonFZ')
        assert self.driver.title == "PythonFZ (Fabian Zills) · GitHub"
    
    # def test_title_blog(self):
    #     self.driver.get('https://www.delrayo.tech/blog')
    #     print(self.driver.title)
