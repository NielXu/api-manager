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
