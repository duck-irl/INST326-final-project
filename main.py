import json
import os
import requests
from dotenv import load_dotenv

load_dotenv()

wmata_api_key = os.getenv("WMATA_API_KEY", "")

class Station:
    def __init__(self, code, name, lines, trains=[]):
        self.code = code
        self.name = name
        self.lines = lines
        self.trains = trains

    def add_train(self):
        pass

    def check_times(self):
        # train.estimated_time is either a number, "ARR", "BRD" "---", or "" ("---" is for non-passenger trains)
        pass

class Train:
    def __init__(self, current_station_code, current_station_name,
                 terminal_station_code, terminal_station_name,
                 estimated_time, line, car_count):
        self.station_code = current_station_code
        self.station_name = current_station_name
        self.end_station_code = terminal_station_code
        self.end_station_name = terminal_station_name
        self.estimated_time = estimated_time
        self.line = line
        self.car_count = car_count

def get_stations():
    station_list = []
    stations = requests.get(f"https://api.wmata.com/Rail.svc/json/" + \
                            f"jStations?api_key={wmata_api_key}").json()
    
    for station in stations["Stations"]:
        station_list.append(Station(
            station["Code"],
            station["Name"],
            [x for x in [station["LineCode1"], station["LineCode2"],
                         station["LineCode3"], station["LineCode4"]]
                         if x is not None]
        ))
    
    return station_list

def get_trains():
    train_list = []
    trains = requests.get(f"http://api.wmata.com/StationPrediction.svc/" + \
                            f"json/GetPrediction/All?api_key=" + \
                                wmata_api_key).json()
    
    for train in trains["Trains"]:
        train_list.append(Train(
            train["LocationCode"],
            train["LocationName"],
            train["DestinationCode"],
            train["DestinationName"],
            train["Min"],
            train["Line"],
            train["Car"]
        ))

    return train_list

def refresh_data():
    all_stations = get_stations()
    all_trains = get_trains()

    for station in all_stations:
        for train in all_trains:
            if train.station_code == station.code:
                station.add_train(train)

    return all_stations, all_trains

if __name__ == "__main__":
    stations, trains = refresh_data()
