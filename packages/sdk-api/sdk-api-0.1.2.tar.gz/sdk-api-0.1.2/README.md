# SDK-API

**SDK-API** is a simple library to access various services of the *superb data kraken (SDK)*  platform.

It is primarily intended to be used in an jupyter hub environment within
the platform itself, but can be configured for different environments as well.

## Installation and Supported Versions

```console
$ python -m pip install sdk-api
```

SDK-API officially supports Python 3.7+.

## Usage

Usage from a jupyter-notebook running within an instance of the SDK.
this presumes access/refresh tokens are accessible via variables of the executing environment (***SDK_ACCESS_TOKEN, SDK_REFRESH_TOKEN***).

```python
>>> import sdk.api
>>> client = sdk.api.SDKClient()
>>> organizations = client.get_all_organizations()
```

with explicit login:
``` python
>>> import sdk.api
>>> sdk.api.SDKClient(username='hasslethehoff', password='lookingforfreedom')
>>> organizations = client.get_all_organizations()
```

### Configuration

by default everything is configured for usage with the default instance of the SDK and comes with settings for various different instances.

overwriting settings:

``` python
>>> client = sdk.api.SDKClient(domain='mydomain.ai', client_id='my-client-id', api_version='v13.37')
```

