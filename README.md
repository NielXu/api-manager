# Intro
api-manager is a tool to simplify the process require to using some useful APIs. Users only need to focus on what they wanna receive instead of handling urls or requests by their own.


# Toolkits
- `api`
  This package contains general tools for requesting and receiving responses from server.
- `google_toolkit`
  It is for some of the common APIs offered by Google, including DistanceMatrix API, Translation API and so on.


# Dependency
Google translation:
```
pip install --upgrade google-cloud-translate
```

# API keys
Most of the APIs require a key for oAuth, therefore, it is important to register one before started to use the tools. Please notice that `config.py` is hidden for remote repo for security purpose, therefore, you might want to create you own `config.py` with sensitive data being stored in it.

# Get started
There are examples in different toolkits, run them and see the results.

Example of using GoogleDistanceMatrix API:
```python
origins = [     # A list of origins
    'origin0',
    'origin1',
    'origin2'
]
des = [         # A list of destinations
    'destination0',
    'destination1',
    'destination2'
]
key = '{Your Google API key here}'
g = GoogleDistMatrix(origins, des, key)
print(g.dist_table())   # Print distance table
print(g.dist_matrix())  # Print distance matrix
print(g.dura_table())   # Print duration table
print(g.dura_matrix())  # Print duration matrix
print(g.dist('origin0', # Print distance between origin0 to destination2
        'destination2'))
```

Example of using GoogleTranslate:
```python
text = [                # A list of words that will be translated
    'Hello World',
    'Google is good'
]
target = 'zh-CN'        # Target language, zh-CN: Chinese
loc = '{Your json file location}'
g = GoogleTranslate(text, target, loc)
print(g.trans_map())    # Print a map in {input:translated} format
```