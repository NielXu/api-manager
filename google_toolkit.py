import api
import json
import config
import os
from google.cloud import translate


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
    


class GoogleTranslate():
    '''Tool for translating texts using Google Translate API.
    @param:
    -------
    text:
        The text that will be translated, can be a str or list
    target:
        The target language, should be language code.
        See: https://cloud.google.com/translate/docs/languages
    key_location:
        Your application credential location, should be a json file.
        See: https://cloud.google.com/translate/docs/quickstart-client-libraries
    '''
    def __init__(self, text, target, key_location):
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = key_location
        client = translate.Client()
        self.trans = client.translate(
            text,
            target_language=target
        )
    
    def trans_map(self):
        '''Get a map that use input text as keys and translated text
        as values.
        '''
        result = {}
        if type(self.trans) == list:
            for t in self.trans:
                result[t['input']] = t['translatedText']
        else:
            result[self.trans['input']] = self.trans['translatedText']
        return result

def distancematrix_example():
    print("++++++++++ GOOGLE DISTANCE MATRIX ++++++++++")
    origins = [
        "1235 Military Trail",
        "29 Rosebank Dr"
    ]
    des = [
        "2025 Midland Ave",
        "yorkdale shopping center"
    ]
    key = config.googlemap_key
    g = GoogleDistMatrix(origins, des, key)
    print("Distance Table:")
    dt = g.dist_table()
    for row in dt:
        print(row)
    
    print("Distance Matrix:")
    dm = g.dist_matrix()
    for row in dm:
        print(row)
    
    print("Duration Table:")
    durt = g.dura_table()
    for row in durt:
        print(row)
    
    print("Duration Matrix:")
    durm = g.dura_matrix()
    for row in durm:
        print(row)
    
    print("Distance between origins and destinations")
    for o in origins:
        for d in des:
            print(o+" to "+d+" is "+g.dist(o, d))
    print()

def trans_example():
    print("++++++++++ GOOGLE TRANSLATE ++++++++++")
    text = [
        "Hello world!",
        "This is a tool for translation"
    ]
    target = "zh-CN"
    loc = config.googletrans_key_loc
    g = GoogleTranslate(text, target, loc)
    print(g.trans_map())


if __name__ == '__main__':
    distancematrix_example()
    trans_example()