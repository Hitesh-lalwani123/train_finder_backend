
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
    return valid_routes[:3]
   
