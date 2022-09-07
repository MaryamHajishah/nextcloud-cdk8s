#!/usr/bin/env python
#from importlib.metadata import metadata
#from sys import api_version
from constructs import Construct
from cdk8s import App, Chart

from mariadb import MariaDb
from nextcloud import NextCloud


class NextCloudCharts(Chart):
    def __init__(self, scope: Construct, id: str):
        super().__init__(scope, id)
        label = {"app": "hello-k8s"}

        MariaDb(self, 'mymariadb')
        NextCloud(self, 'mynextcloud')
        #MariaDb(self, 'ghost', image='ghost', container_port=2368)


app = App()
NextCloudCharts(app, "hamravesh")

app.synth()
