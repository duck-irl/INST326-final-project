
def test_add_train():
    #checks if a train is properly added to the station's trains list
    station = Station("A01", "Metro Center", ["RD"])
    train = Train("A01", "Metro Center", "B11", "Glenmont", "5", "RD", "8")
    station.add_train(train)
    assert len(station.trains) == 1
    assert station.trains[0] == train

def test_check_times_arriving():
    #checks if a train with estimated_time "ARR" returns an arriving message
    station = Station("A01", "Metro Center", ["RD"])
    train = Train("A01", "Metro Center", "B11", "Glenmont", "ARR", "RD", "8")
    station.add_train(train)
    result = station.check_times()
    assert result == ["RD line to Glenmont: Arriving"]

def test_check_times_boarding():
    #checks if a train with estimated_time "BRD returns a boarding message
    station = Station("A01", "Metro Center", ["RD"])
    train = Train("A01", "Metro Center", "B11", "Glenmont", "BRD", "RD", "8")
    station.add_train(train)
    result = station.check_times()
    assert result == ["RD line to Glenmont: Boarding"]
    

def test_check_times_skips_non_passenger():
    #checks if a train with estimated_time "---" is skipped and returns an empty line
    station = Station("A01", "Metro Center", ["RD"])
    train = Train("A01", "Metro Center", None, "No Passenger", "---", "No", None)
    station.add_train(train)
    result = station.check_times()
    assert result == [] 

def test_check_times_minutes():
    #checks if a train with a numeric estimated_time returns the correct minutes 
    station = Station("A01", "Metro Center", ["RD"])
    train = Train("A01", "Metro Center", "B11", "Glenmont", "3", "RD", "8")
    station.add_train(train)
    result = station.check_times()
    assert result == ["RD line to Glenmont: 3 min"]