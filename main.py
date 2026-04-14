import json
import os
import requests
from dataclasses import dataclass, field
from dotenv import load_dotenv

load_dotenv()

wmata_api_key = os.getenv("WMATA_API_KEY", "")

@dataclass
class Station:
    """Represents a station and its information.
    
    Attributes:
        code (str): The code of the station.
        name (str): The name of the station.
        lines (list[str]): A list of lines that the station serves.
        trains (list[Train]): A list of Train objects that are currently at the station.
    """
    code: str
    name: str
    lines: list[str]
    trains: list[Train] = field(default_factory=list)

    def add_train(self, train):
        self.trains.append(train)

    def check_times(self):
        # train.estimated_time is either a number, "ARR", "BRD" "---", or "" ("---" is for non-passenger trains)
        pass

@dataclass
class Train:
    """Represents a train and its information.

    Attributes:
        station_code (str): The code of the station where the train is located.
        station_name (str): The name of the station where the train is located.
        end_station_code (str): The code of the destination station.
        end_station_name (str): The name of the destination station.
        estimated_time (str): The estimated time for the train to arrive at
            the destination station. This is either a number (min),
            "ARR" (arriving), "BRD" (boarding), or
            "---" (non-passenger train).
    """
    station_code: str
    station_name: str
    end_station_code: str
    end_station_name: str
    estimated_time: str
    line: str
    car_count: str

def get_stations():
    """Get all stations from the WMATA API and return a list of
        Station objects.

    Returns:
        list[Station]: A list of Station objects.
    """
    station_list = []
    stations = requests.get(f"https://api.wmata.com/Rail.svc/json/" + \
                            f"jStations?api_key={wmata_api_key}").json()
    
    for station in stations["Stations"]:
        station_list.append(
            Station(
                station["Code"],
                station["Name"],
                [x for x in [station["LineCode1"], station["LineCode2"],
                            station["LineCode3"], station["LineCode4"]]
                            if x is not None]
            )
        )
    
    return station_list

def get_trains():
    """Get all trains from the WMATA API and return a list of Train objects.
    
    Returns:
        list[Train]: A list of Train objects.
    """
    train_list = []
    trains = requests.get(f"http://api.wmata.com/StationPrediction.svc/" + \
                            f"json/GetPrediction/All?api_key=" + \
                                wmata_api_key).json()
    
    for train in trains["Trains"]:
        train_list.append(
            Train(
                train["LocationCode"],
                train["LocationName"],
                train["DestinationCode"],
                train["DestinationName"],
                train["Min"],
                train["Line"],
                train["Car"]
            )
        )

    return train_list

def refresh_data():
    """Refresh the data by fetching the WMATA API.
    
    Returns:
        tuple(list[Station], list[Train]): A tuple containing a list of
            Station objects and a list of Train objects.
    """
    all_stations = get_stations()
    all_trains = get_trains()

    for station in all_stations:
        for train in all_trains:
            if train.station_code == station.code:
                station.add_train(train)

    return all_stations, all_trains

if __name__ == "__main__":
    stations, trains = refresh_data()
