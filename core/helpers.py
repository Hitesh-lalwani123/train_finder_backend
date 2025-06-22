from constants import stations
from visualizer import visualize_connections
from fastapi import FastAPI, BackgroundTasks

travel_from = "KCG"
travel_to = "BPL"
def filter_data(train_number,data,background_tasks):
    train_data = data[train_number]
    result = []
    for route in train_data:
        for fare_class in train_data[route]:
            if 'AVL' in train_data[route][fare_class][0] or 'RAC' in train_data[route][fare_class][0]:
                result.append(route)
    result = find_connection_pairs(result,background_tasks)
    for val in result:
        if val == 'CHZ-BPL':
            result = val
            break
    return {train_number: result}


def find_connection_pairs(data,background_tasks):
    results = []
    possible_route = []
    def find_route1(start_ind,end_ind):
        possible_pairs = []
        for val in possible_route:
                if val[0] <= end_ind and val[1]>=15:
                    possible_pairs.append(f"{find_station(val[0])},{find_station(val[1])}")
        if possible_pairs:
            return possible_pairs
        else: 
            return None
    def find_route2(start_ind,end_ind):
        possible_pairs = []
        for val in possible_route:
                if val[0] <= 8 and val[1]>=start_ind:
                    possible_pairs.append(f"{find_station(val[0])},{find_station(val[1])}")
        if possible_pairs:
            return possible_pairs
        else:     
            return None
    connection_pairs = []
    
    for route in data:
        from_st = route.split('-')[0]
        to_st = route.split('-')[1]
        start_ind = 0
        end_ind = 0
        for i in range(len(stations)):
            if stations[i] == from_st:
                start_ind = i
            if stations[i] ==  to_st:
                end_ind = i
        if start_ind <= 8 and end_ind >= 15:
            # print("Valid route: ", route)
            results.append(route)
        elif start_ind <=8 and end_ind < 15:
            if_route = find_route1(start_ind,end_ind)
            if if_route:
                # print("Valid route: ",route,if_route)
                results.append([route,if_route])
            else:
                possible_route.append([start_ind,end_ind])
        elif start_ind > 8 and end_ind >= 15:
            if_route = find_route2(start_ind,end_ind)
            if if_route:
                # print("Valid route: ",if_route,route)
                results.append([if_route,route])
            else:
                possible_route.append([start_ind,end_ind])
            
        connection_pairs.append((start_ind,end_ind))
    return results
    # background_tasks.add_task(visualize_connections, connection_pairs,stations)

def find_ind(station: str):
    for i in range(stations):
        if(stations[i] == station):
            return i
    return None
def find_station(ind: int):
    return stations[ind]