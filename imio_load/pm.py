# -*- coding: utf-8 -*-
import itertools
from urllib.parse import urlencode

from locust import HttpLocust, TaskSet, task

USERS = ["dgen", "chefPers"]
PASS = "meeting"


class SiteBrowser(TaskSet):
    def login(self):
        self.user = USERS[0]
        with self.client.post(
            "/login_form",
            {
                "__ac_name": self.user,
                "__ac_password": PASS,
                "came_from": "",
                "next": "",
                "target": "",
                "form.submitted": "1",
                "js_enabled": "0",
                "cookies_enabled": "1",
                "login_name": self.user,
                "pwd_empty": "0",
                "submit": "Log in",
            },
            catch_response=True,
        ) as resp:
            if not resp.content or "Mes points".encode() not in resp.content:
                resp.failure("Could not login")

    def logout(self):
        self.client.get("/logout")

    @task(1)
    def index(self):
        self.client.get("/")

    @task(2)
    def search_my_items(self):
        data = {
            "c11[]": self.user,
            "c1[]": "17211019ce69438ca3cc1b852b0c8d90",
            "c3[]": 20,
            "c7-operator[]": "or",
        }
        search_url = "/Members/{}/mymeetings/meeting-config-college/searches_items/@@faceted_query?{}"
        for i in itertools.count(start=0, step=20):
            data["b_start"] = i
            response = self.client.get(
                search_url.format(self.user, urlencode(data)), name="my_items"
            )
            if u"éléments suivants" not in response.text:
                break

    def on_start(self):
        self.login()

    def on_stop(self):
        self.logout()


class DGenSiteBrowser(SiteBrowser):
    login = "dgen"


class ChefPersBrowser(SiteBrowser):
    login = "chefPers"


class CMSUser(HttpLocust):
    task_set = SiteBrowser
    min_wait = 10000
    max_wait = 30000
