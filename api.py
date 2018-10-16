import json
import requests
from collections import OrderedDict


def send(request):
    "Send the request to the api server and return response as json file"
    return json.loads(requests.get(request.full_url).text)


class Request():
    """
    @param:
    -------
    url:\n
    base url, can include '?' at the end indicates that param starts from here\n
    param_map:\n
    a map that stores param names as keys and params as values.
    It is recommended to use collections.OrderedDict since for some urls, orders of params
    are important. The params can be either a single element, or a list with multiple elements.
    If it is a list, the first element of the list is the separator, which means that
    how each element in the list will be separated.\n
    replacer:\n
    a map, store patterns as keys and what will be replaced as values.
    """
    def __init__(self, url, param_map, replacer={}):
        self.full_url = self._conca(url, param_map, replacer)
    
    def _conca(self, url, param_map, replacer):
        full = url
        for param_name in param_map:
            param = param_map[param_name]
            if type(param) == list:
                full += self._conca_list(param_name, param)
            else:
                full += param_name + "=" + param + "&"
        for r in replacer:
            full = full.replace(r, replacer[r])
        return full[:-1]
    
    def _conca_list(self, pname, plist):
        result = pname+"="
        sep = plist[0]
        for i in range(1, len(plist)):
            result += plist[i]
            if i != len(plist) - 1:
                result += sep
        return result + "&"