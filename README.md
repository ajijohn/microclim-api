microclim-api
=============

Official Microclim API Wrapper.

# Installation
git clone https://github.com/huckley/microclim-api.git microclim-api

# Usage
from microclim.api import MicroclimApiClient

## Microclim API

```python
#KEY = 'test'
#SECRET = 'sec'
#IP='localhost:8008/'
microclim_client = MicroclimApiClient(KEY,SECRET,IP)
```

### Get health
```python
microclim_health = microclim_client.poke(active="True")
```


## Submit a filtering job
```python
#regions=1:900-1000&&subpops=CHB&format=reformat&nfs=yes
request_tracking_id = microclim_client.request(regions = '1:900-1000', subpops = 'CHB', format = 'reformat',nfs='yes')
print("Tracking id " + request_tracking_id )
```

### Status
```python
microclim_request_status = microclim_client.status(request = request_tracking_id)
```


### Get insights into your request (Not Implemented)
```python
microclim_request_insights = microclim_client.insight(request = request_tracking_id,type = 'throughput')
```

### Get details of your request.
```python
microclim_job_details = microclim_client.get_details(request = request_tracking_id)

```


### Get detail of all the requests.
```python
microclim_requests = request_tracking_id.jobs()
```





