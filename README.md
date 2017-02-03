microclim-api
=============

Official Microclim API Wrapper.

# Installation
```
git clone https://github.com/trenchproject/microclim-api.git microclim-api
```


# Usage
```python
from microclim.api import MicroclimApiClient
```

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
#sample values - Around Denver
request_tracking_id = microclim_client.request(latS = 39.4001220001459,
                    latN = 39.91394967016644,
                    lonW = -106.50764465332031,
                    lonE = -105.92399597167969,
                    variable = 'Tsurface',
                    shadelevel='0',
                    hod='7',
                    interval='0',
                    aggregation='0',
                    enddate='19810128',
                    outputformat='csv',
                    startdate='19810101')

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





