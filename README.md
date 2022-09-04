Line Parser
===

Line Parser is a flask hosted application, it has a single route `/`.
This route takes a `filename` corresponding to a file in app/test-files
and a `from` and `to` date to select the lines from request params.

The files should be structured exactly as below:
```
[Date in YYYY-MM-DDThh:mm:ssZ Format][space][Email Address][space][Session Id in GUID format]
```
For example:

```
2020-12-04T11:14:23Z jane.doe@email.com 2f31eb2c-a735-4c91-a122-b3851bc87355
```

It can be called as below:
```bash
curl -XPOST localhost:8279/ -H 'Content-Type: application/json' -d '{"filename":"sample1.txt", "from":"2020-07-06T23:00:00Z", "to": "2021-07-06T23:00:00Z"}'
```

The output is an array of the json representation of the lines queried ordered by eventTime
```JSON
[
  {
    "eventTime":"2000-01-01T03:05:58Z",
    "email":"test123@test.com",
    "sessionId":"97994694-ea5c-4da7-a4bb-d6423321ccd0"
  },
  {
    "eventTime":"2000-01-01T04:05:58Z",
    "email":"test456@test.com",
    "sessionId":"97994694-ea5c-4da7-a4bb-d6423321ccd1"
  }
]
```

If the inputs are incorrect or there is no data it will return and empty json array
```JSON
[]
```

The application its self does a recursive binary search on the file for the starting date
it then will iterate through from there until it reaches the end date or the end of the array, formats the strings to json data and returns it. 

I have designed the service with best effort to allow it to be reused in any larger context.

Testing was done to outline general use and some edge cases. Although more testing should be done on each functionality in the service class to indicate any regressions more specifically. In its current condition we would only know that the application regressed rather than what regressed. Testing should also be performed around our conditional checking of the date and file inputs.

Use `./build.sh` and then `./run.sh` in the scripts to start the application.

I have marked comments where we can improve in code. 
