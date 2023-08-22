from django.shortcuts import render, redirect
from django.contrib.humanize.templatetags.humanize import intcomma
from pats.propClasses import Attributes, Root
from pats.propValueClasses import PvAttributes, PvRoot
import json
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from django.views.generic import TemplateView

class PatsTable():
    def __init__(self, account):
        self.account = account
        self.prop_url = "https://geo.co.crook.or.us/server/rest/services/publicApp/Pats_Tables/MapServer/11/query"
        self.params = {
            "where": f"account_id='{account}'",
            "outFields": "*",
            "returnGeometry": False,
            "f": "json"
        }
        self.maptaxlot = []

    def get_data(self):
        prop_response = requests.get(self.prop_url, params=self.params)
        prop_data = prop_response.json()
        return prop_data

    def process_data(self):
        prop_data = self.get_data()

        for elem in prop_data['features']:
            root = Root.from_dict(elem)
            mt = root.attributes.map_taxlot
            mt_find = mt[:mt.find('-', mt.find('-') + 1)]
            self.maptaxlot.append(mt_find.replace('-', ''))


    def account_query(account):

        data_pipeline = PatsTable(account=account)
        data_pipeline.process_data()

        #print(data_pipeline.maptaxlot)


patsTable = PatsTable(1001)
print(patsTable.get_data())


PatsTable.account_query(1001)


