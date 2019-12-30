import requests
import threading
from urllib.parse import urljoin
from be import create_app, db
from fe import conf

thread: threading.Thread = None


# 修改这里启动后端程序，如果不需要可删除这行代码
# def run_backend():
#     app = create_app({
#         'TESTING': True
#     })
#     yield app

def run_backend():
    create_app().run()

def pytest_configure(config):
    global thread
    print("frontend begin test")
    thread = threading.Thread(target=run_backend)
    thread.start()


def pytest_unconfigure(config):
    url = urljoin(conf.URL, "shutdown")
    requests.get(url)
    thread.join()
    print("frontend end test")
