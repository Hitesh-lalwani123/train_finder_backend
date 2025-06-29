from constants import stations
from visualizer import visualize_connections
from fastapi import FastAPI, BackgroundTasks
from constants import FARE_CLASS
travel_from = "KCG"
travel_to = "BPL"

def filter_data(train_number,data,from_station,to_station,background_tasks):
    print("Trying to find routes from:",from_station,"to:",to_station)
    try:
        train_data = data[train_number]
        result = []
        for route in train_data:
            searched_route = route.split(',')[0]
            for fare_class in train_data[route]:
                availibility = train_data[route][fare_class][0]
                fare_in_rupees = train_data[route][fare_class][1]
                if 'AVL' in availibility or 'RAC' in availibility:
                    if fare_class in FARE_CLASS:
                        route_with_class = f"{fare_class}:{route}:{fare_in_rupees}"
                        result.append(route_with_class)
        # print(result)
        result = find_connection_indices(result,from_station,to_station)
        # result = find_connection_pairs(result,from_station,to_station,background_tasks)
        return {train_number: result}
    except Exception as e:
        return {train_number: "Train not running on selected date/ No data found"}


def find_connection_indices(data,a,b):
    results = []
    
    for route_with_fare in data:
        route_data = route_with_fare.split(':')
        fare_class = route_data[0]
        route = route_data[1]
        fare = int(route_data[2][1:])
        searched_route = route.split(',')[0]
        actual_route = route.split(',')[1]
        from_st = searched_route.split('-')[0]
        to_st = searched_route.split('-')[1]
        start_ind = 0
        end_ind = 0
        for i in range(len(stations)):
            if stations[i] == from_st:
                start_ind = i
            if stations[i] ==  to_st:
                end_ind = i
        results.append([start_ind,end_ind,fare,fare_class])
    return find_optimal_path(find_ind(a),find_ind(b),results)

def find_connection_pairs(data,from_station,to_station,background_tasks):
    from_station = find_ind(from_station)
    to_station = find_ind(to_station)
    if from_station == None:
        print("from station not in list")
        from_station = 0
    if to_station == None:
        print("to station not in list")
        to_station = len(stations)-1
    print(from_station,to_station)
    results = []
    possible_route = []
    def find_route1(fare_class,start_ind,end_ind):
        possible_pairs = []
        for val in possible_route:
                if val[1] <= end_ind and val[2]>=to_station:
                    possible_pairs.append(f"{val[0]}:{find_station(val[1])},{find_station(val[2])}")
        if possible_pairs:
            return possible_pairs
        else: 
            return None
    def find_route2(fare_class,start_ind,end_ind):
        possible_pairs = []
        for val in possible_route:
                if val[1] <= from_station and val[2]>=start_ind:
                    possible_pairs.append(f"{val[0]}:{find_station(val[1])},{find_station(val[2])}")
        if possible_pairs:
            return possible_pairs
        else:     
            return None
    connection_pairs = []
    
    for route_with_fare in data:
        fare_class = route_with_fare.split(':')[0]
        route = route_with_fare.split(':')[1]
        searched_route = route.split(',')[0]
        actual_route = route.split(',')[1]
        from_st = searched_route.split('-')[0]
        to_st = searched_route.split('-')[1]
        start_ind = 0
        end_ind = 0
        for i in range(len(stations)):
            if stations[i] == from_st:
                start_ind = i
            if stations[i] ==  to_st:
                end_ind = i
        if start_ind <= from_station and end_ind >= to_station:
            results.append(route_with_fare)
        elif start_ind <=from_station and end_ind < to_station:
            if_route = find_route1(fare_class,start_ind,end_ind)
            if if_route:
                results.append([route_with_fare,if_route])
            else:
                possible_route.append([fare_class,start_ind,end_ind])
        elif start_ind > from_station and end_ind >= to_station:
            if_route = find_route2(fare_class,start_ind,end_ind)
            if if_route:
                results.append([if_route,route_with_fare])
            else:
                possible_route.append([fare_class,start_ind,end_ind])
            
        connection_pairs.append((start_ind,end_ind))
    # background_tasks.add_task(visualize_connections, connection_pairs,stations)
    return results

def find_ind(station: str):
    for i in range(len(stations)):
        if(stations[i].lower() == station.lower()):
            return i
    return None
def find_station(ind: int):
    return stations[ind]


def find_optimal_path(a,b,available_paths):
    def find_all_paths_with_labels(a, b, available_paths, min_segments=None, max_segments=None):
        # Filter valid forward-moving paths
        valid_paths = [arr for arr in available_paths if arr[0] <= arr[1]]
        all_results = []

        # Queue: (current_end, path_so_far, total_fare)
        queue = []

        for s, e, fare, label in valid_paths:
            if s <= a and e >= a:
                queue.append((e, [[s, e, fare, label]], fare))

        while queue:
            curr_end, path, total_fare = queue.pop(0)

            if path[0][0] <= a and curr_end >= b:
                if (min_segments is None or len(path) >= min_segments) and \
                (max_segments is None or len(path) <= max_segments):
                    all_results.append((path, total_fare))
                continue

            for s, e, fare, label in valid_paths:
                if s <= curr_end and e > curr_end:
                    new_path = path + [[s, e, fare, label]]
                    new_total_fare = total_fare + fare
                    queue.append((e, new_path, new_total_fare))

        # Sort and return only the paths (not fare)
        all_results.sort(key=lambda item: (
            len(item[0]),                  # fewer segments
            item[1],                      # lower total fare
            abs(item[0][0][0] - a),       # start closer to a
            abs(item[0][-1][1] - b)       # end closer to b
        ))
        all_paths = [path for path, _ in all_results]
        return all_paths
    all_paths = find_all_paths_with_labels(a, b, available_paths)
    valid_routes = []
    for val in all_paths:
        cost = 0
        segment_length = 0
        for item in val:
            cost += item[2]
            segment_length += 1
        if segment_length > 2:
            continue
        valid_routes.append([val,cost])
    valid_routes.sort(key=lambda item: (                 
        item[1]          
    ))
    final_routes = valid_routes[:3]
    print(final_routes)
    routes_dict_list = []
    for val in final_routes:
        route_details = val[0]
        total_fare = val[1]
        route_list = []
        for route in route_details:
            from_st = route[0]
            to_st = route[1]
            fare_class = route[3]
            curr_route_details = {
                "from_station":from_st,
                "to_station":to_st,
                "fare_class":fare_class
            }
            route_list.append(curr_route_details)
        routes_dict_list.append([route_list,total_fare])
    print(routes_dict_list)
    return routes_dict_list
