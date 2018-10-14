import api
import json
import config


class GoogleDistMatrix():
    def __init__(self, origins, destinations, key):
        param_map = self._map(origins, destinations, key)
        replace = {" ":"+"}
        url = "https://maps.googleapis.com/maps/api/distancematrix/json?"
        req = api.Request(url, param_map, replace)
        self.data = api.send(req)
        self.origins = origins
        self.destinations = destinations
    
    def _map(self, origins, destinations, key):
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
        rows = self.data['rows']
        table = []
        for row in rows:
            table.append(row['elements'])
        return table
    
    def dist_table(self):
        raw = self.raw_table()
        table = []
        for row in raw:
            r = []
            for i in row:
                r.append(str(i['distance']['value'])+"("+i['distance']['text']+")")
            table.append(r)
        return table
    
    def dist_matrix(self):
        raw = self.raw_table()
        table = []
        for row in raw:
            r = []
            for i in row:
                r.append(i['distance']['value'])
            table.append(r)
        return table
    
    def dura_table(self):
        raw = self.raw_table()
        table = []
        for row in raw:
            r = []
            for i in row:
                r.append(str(i['duration']['value'])+"("+i['duration']['text']+")")
            table.append(r)
        return table
    
    def dura_matrix(self):
        raw = self.raw_table()
        table = []
        for row in raw:
            r = []
            for i in row:
                r.append(i['duration']['value'])
            table.append(r)
        return table

    def dist(self, origin, des):
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