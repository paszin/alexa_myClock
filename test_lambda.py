import aws_lambda as myClock

data = {
  "session": {
    "sessionId": "SessionId.01a92a9a-5535-6b4c6",
    "application": {
      "applicationId": "amzn1.echo-sdk-ams.app.fa0396ba-4d2190"
    },
    "attributes": {},
    "user": {
      "userId": "amzn1.ask.account.AFP3ZW"
    },
    "new": False
  },
  "request": {
    "type": "IntentRequest",
    "requestId": "EdwRequestId.21f",
    "timestamp": "2016-06-09T07:35:57Z",
    "intent": {
      "name": "TimeIntent",
      "slots": {}
    },
    "locale": "en-US"
  },
  "version": "1.0"
}


myClock.lambda_handler(data, None)