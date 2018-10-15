import api
import json
import config


class GoogleDistMatrix():
    '''Tool for Google Distance Matrix API, can get distance matrices between
    origins and destinations.
    @param:
    -------
    origins:
        A list of addresses, or str if only one address
    destinations:
        A list of destinations, or str if only one address
    key:
        API key
    '''
    def __init__(self, origins, destinations, key):
        param_map = self._map(origins, destinations, key)
        replace = {" ":"+"}
        url = "https://maps.googleapis.com/maps/api/distancematrix/json?"
        req = api.Request(url, param_map, replace)
        self.data = api.send(req)
        self.origins = origins
        self.destinations = destinations
    
    def _map(self, origins, destinations, key):
        'Setup the param map'
        if type(origins) == list and len(origins) > 1:
            origins = ["|"] + origins
        if type(destinations) == list and len(destinations) > 1:
            destinations = ["|"] + destinations
        return {
            "origins": origins,
            "destinations": destinations,
            "key": key
        }
    
    def raw_table(self):
        '''Get the raw table of the data, which means the data
        are in json format that returned by google server. The label
        of the row are destinations, and the label of the columns
        are origins.
        '''
        rows = self.data['rows']
        table = []
        for row in rows:
            table.append(row['elements'])
        return table
    
    def dist_table(self):
        '''Get the distance table of the data, which means that each
        element in the table represents the distance between origin
        and destination. The label of the row are destinations,
        and the label of the columns are origins.
        @Element format:
        ---------------
            int(str)
        @Example:
        --------
            5099(5.1 km)
        '''
        raw = self.raw_table()
        table = []
        for row in raw:
            r = []
            for i in row:
                r.append(str(i['distance']['value'])+"("+i['distance']['text']+")")
            table.append(r)
        return table
    
    def dist_matrix(self):
        '''Get the distance in matrix format, each element
        represents the distance between origin to destination.
        `[
            o1-d1, o1-d2, o1-d3, ..., o1-dn
            o2-d1, o2-d2, o2-d3, ..., o2-dn
            ...
            om-d1, om-d2, om-d3, ..., om-dn
        ]`
        oi-dj means from origin i to destination j
        '''
        raw = self.raw_table()
        table = []
        for row in raw:
            r = []
            for i in row:
                r.append(i['distance']['value'])
            table.append(r)
        return table
    
    def dura_table(self):
        '''Get the duration table of the data, which means that each
        element in the table represents the time it takes to travel
        from origin to destination. The label of the row are destinations,
        and the label of the columns are origins.
        @Element format:
        ---------------
            int(str)
        @Example:
        --------
            504(8 mins)
        '''
        raw = self.raw_table()
        table = []
        for row in raw:
            r = []
            for i in row:
                r.append(str(i['duration']['value'])+"("+i['duration']['text']+")")
            table.append(r)
        return table
    
    def dura_matrix(self):
        '''Get the duration in matrix format, each element
        represents the time it takes to travel from origin
        to destination.
        `[
            o1-d1, o1-d2, o1-d3, ..., o1-dn
            o2-d1, o2-d2, o2-d3, ..., o2-dn
            ...
            om-d1, om-d2, om-d3, ..., om-dn
        ]`
        oi-dj means from origin i to destination j
        '''
        raw = self.raw_table()
        table = []
        for row in raw:
            r = []
            for i in row:
                r.append(i['duration']['value'])
            table.append(r)
        return table

    def dist(self, origin, des):
        '''Get distance between one origin and one destination.
        If the origin or destination is not included in the
        requests, None will be returned. Otherwise a distance in
        format `int(str)` will be returned.
        '''
        table = self.dist_table()
        row, col = -1, -1
        for i in range(0, len(self.origins)):
            if origin == self.origins[i]:
                row = i
        for i in range(0, len(self.destinations)):
            if des == self.destinations[i]:
                col = i
        if row != -1 and col != -1:
            return table[row][col]


if __name__ == '__main__':
    origins = [
        "17 wiggens crt",
        "28 rosebank dr"
    ]
    des = [
        "1235 Military Trail",
        "2260 Markham Rd"
    ]
    matrix = GoogleDistMatrix(origins, des, config.googlemap_key)
    # Pint distance table
    dist_table = matrix.dist_table()
    for i in range(len(dist_table)):
        p = ""
        for j in range(len(dist_table[i])):
            p += origins[i] + " to " + des[j] + ": " + dist_table[i][j] + "\t"
        print(p)
        dist_table = matrix.dist_table()
    print()
    # Print duration table
    dura_table = matrix.dura_table()
    for i in range(len(dura_table)):
        p = ""
        for j in range(len(dura_table[i])):
            p += origins[i] + " to " + des[j] + ": " + dura_table[i][j] + "\t"
        print(p)
    print()