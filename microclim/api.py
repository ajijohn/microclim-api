
import urllib

try:
    import simplejson as json
except :
    import json


import requests

__all__ = [
    'MicroclimApiClient'
]

################################################################################

class HttpException(Exception):
    def __init__(self, code, reason, error='Unknown Error'):
        self.code = code
        self.reason = reason
        self.error_message = error
        super(HttpException, self).__init__()

    def __str__(self):        
        return '\n Status: %s \n Reason: %s \n Error Message: %s\n' % (self.code, self.reason, self.error_message)

################################################################################


class HttpApiClient(object):
    """
    Base implementation for an HTTP
    API Client. Used by the different
    API implementation objects to manage
    Http connection.
    """

    def __init__(self, api_key,api_secret, base_url):
        """Initialize base http client."""
        #self.conn = http()
        # Microclim API key
        self.api_key = api_key
        # Microclim SECRET key
        self.api_secret = api_secret

        #base url 
        self.base_url = base_url

        #token uri
        token_uri='api/auth'
        response = requests.post(self.base_url+token_uri, data={'apikey': self.api_key, 'apisecret': self.api_secret})
        if (response.status_code == requests.codes.ok):
            # initialize with the token
            self.auth_token = json.loads(response.text)['token']


    def _http_request(self, service_type, **kwargs):
        """
        Perform an HTTP Request using base_url and parameters
        given by kwargs.
        Results are expected to be given in JSON format
        and are parsed to python data structures.
        """

        headers = {'Authorization': 'Bearer '+self.auth_token}

        response = requests.get(self.base_url+service_type, params=kwargs,headers=headers)
        return response.headers, response


    def _is_http_response_ok(self, response):
        return response['status'] == '200' or response['status'] == 200

    def _get_params(self,
                    latS = None,
                    latN = None,
                    lonW = None,
                    lonE = None,
                    variable = None,
                    shadelevel=None,
                    hod=None,
                    interval=None,
                    aggregation=None,
                    enddate=None,
                    outputformat=None,
                    startdate=None,
                    requestId=None
                    ):


        params = {}

        if latS:
            params['latS'] = latS
        if latN:
            params['latN'] = latN
        if lonW:
            params['lonW'] = lonW
        if lonE:
            params['lonE'] = lonE
        if variable:
            params['variable'] = variable
        if shadelevel:
            params['shadelevel'] = shadelevel
        if hod:
            params['hod'] = hod
        if interval:
            params['interval'] = interval
        if aggregation:
            params['aggregation'] = aggregation
        if enddate:
            params['enddate'] = enddate
        if outputformat:
            params['outputformat'] = outputformat
        if startdate:
            params['startdate'] = startdate
        if requestId:
            params['requestId'] = requestId

        return params


    def _create_query(self, category_type, params):
        header, response = self._http_request(category_type , **params)
        resp =  response.text
        if not (response.status_code == requests.codes.ok):
            raise response.raise_for_status()
        return resp


################################################################################


class MicroclimApiClient(HttpApiClient):

    def __init__(self, api_key,api_secret,ip):
        self.ip = ip
        self.api_url  = 'http://' + ip
        base_url = self.api_url
        super(MicroclimApiClient, self).__init__(api_key,api_secret,base_url)


    def request(self, latS = None,
                    latN = None,
                    lonW = None,
                    lonE = None,
                    variable = None,
                    shadelevel=None,
                    hod=None,
                    interval=None,
                    aggregation=None,
                    enddate=None,
                    outputformat=None,
                    startdate=None):
        """
        Spawns/Starts a filtering job on Microclim
        # For eg regions=1:900-1000&&subpops=CHB&format=reformat&nfs=yes
        
        Args: 
        *Note that none of the arguments are required
          latN         : latN Bounding box Lat N.
            type : [number]
          latS          : latS Bounding box Lat S.
            type : [number]
          lonW          : lonW Bounding box Lat W.
            type : [number]
          lonE            : onE Bounding box Lat E
            type : [number]
          variable         : Microclimate Variable.
            type : [number]
          startdate  : YYYYMMDDHH where YYYY is year, MM is month, DD is day, and HH is hour.
            type:[string]
          enddate :  YYYYMMDDHH where YYYY is year, MM is month, DD is day, and HH is hour.
             type:[string]
           file : Output type (CSV or netCDF)
              type:[string]
           shadelevel : percentage shade
               type:[string]
           hod : height in meters; above or below the surface
                type:[string]
           interval : time interval
                 type:[string]
           ggregation : aggregation metric
             type:[string]

        Returns:
          Request Id in a string form

        Raises:
          HttpException with the error message from the server
        """

        params = self._get_params(latS = latS,
                    latN = latN,
                    lonW = lonW,
                    lonE = lonE,
                    variable = variable,
                    shadelevel=shadelevel,
                    hod=hod,
                    interval=interval,
                    aggregation=aggregation,
                    enddate=enddate,
                    outputformat=outputformat,
                    startdate=startdate)

        return self._create_query('microclim/request', params)

    def status(self, requestId=None):
        """
        Takes the request id and gives the status

        Args: 
          request id: Identifier of the filtering job - Fetched from request

        Returns:
          Job id with status

        Raises:
          HttpException with the error message from the server
        """
        params = self._get_params(requestId = requestId)

        return self._create_query('microclim/status', params)

    def requests(self):
        """
        Returns the details of all the jobs.

        Args:
          None

        Returns:
          All the jobs

        Raises:
          HttpException with the error message from the server
        """
        params = self._get_params()

        return self._create_query('requests', params)

    def get_details(self, requestId=None):
        """
        Details of the request -

        
        Args: 
            request          : Request Id
              type : [string]


        Returns:
          Details of the filtering job

        Raises:
          HttpException with the error message from the server
        """

        params =  self._get_params(requestId = requestId)

        return self._create_query('microclim/fetch', params)

    def poke(self, active=None):
        """
        Health of the service

        Args:
              active : Whether to check if any jobs are pending
              type : [bool]
        Returns:
          Basic status of the API endpoint
        Raises:
          HttpException with the error message from the server
        """

        params =  self._get_params(active = active)

        return self._create_query('poke', params)



################################################################################    
if __name__ == '__main__':
    print("Please enter Microclim api key,api secret with IP(With Port)")
    #curl -X POST -H 'Content-Type: application/json'
    # -d '{ "apikey": "07d4d584c04941a25e291feb8881c685",
    #  "apisecret": "9ef6bbb24a855fbb765f3890e05592f4" }'
    # localhost:3000/api/auth
    KEY = '07d4d584c04941a25e291feb8881c685'
    SECRET = '9ef6bbb24a855fbb765f3890e05592f4'
    IP='localhost:3000/'

    #Initialize

    microclim_client = MicroclimApiClient(KEY,SECRET,IP)
    job_status = microclim_client.status(requestId = '3e1613c0-21e2-4c1a-ad9c-45fb9370c1a5')
    print("Request Status is " + job_status )

    #Without request
    jobs = microclim_client.requests()

    print("Jobs " + jobs )
