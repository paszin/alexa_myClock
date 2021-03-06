"""
Copy this code to your aws lambda function for your my clock skill.
"""

from __future__ import print_function
import time
import random
import urllib2

my_timezone = "pdt" ## Los Angeles
## or utc, gmt, est, ...
## for full list see https://github.com/progrium/timeapi/blob/master/timeapi.rb


def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    # if (event['session']['application']['applicationId'] !=
    #         "amzn1.echo-sdk-ams.app.[unique-value-here]"):
    #     raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])


def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return get_welcome_response()


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name == "TimeIntent":
        return timeIntent(intent, session)
    elif intent_name == "RandomFactTodayIntent":
        return randomFactTodayIntent(intent, session)
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here

# --------------- Functions that control the skill's behavior ------------------


def get_welcome_response():
    """ Give the current time and suggest what you can ask
    """

    session_attributes = {}
    date_str = urllib2.urlopen('http://www.timeapi.org/'+my_timezone+'/now?format=%20%25I:%25M').read()
    hours, minutes = date_str.split(':')
    speech_output = "Hi, It`s " + time2text(int(hours), int(minutes))
    reprompt_text = ""
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        speech_output, reprompt_text, should_end_session))


def handle_session_end_request():
    speech_output = "Have a nice day! "
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        speech_output, None, should_end_session))




def randomFactTodayIntent(intent, session):
    """ """
    
    session_attributes = {}
    should_end_session = True
    date_str = urllib2.urlopen('http://www.timeapi.org/'+my_timezone+'/now?format=%25-m%20%25e').read()
    month, day = date_str.split(' ')
    speech_output = getRandomFact(int(day), int(month))
    reprompt_text = speech_output
    return build_response(session_attributes, build_speechlet_response(
        speech_output, reprompt_text, should_end_session))


def timeIntent(intent, session):
    """ 
    Return Natural Language Text for the current time.
    """

    session_attributes = {}
    should_end_session = True
    date_str = urllib2.urlopen('http://www.timeapi.org/'+my_timezone+'/now?format=%20%25I:%25M').read()
    hours, minutes = date_str.split(':')
    speech_output = time2text(int(hours), int(minutes))
    reprompt_text = speech_output
    return build_response(session_attributes, build_speechlet_response(
        speech_output, reprompt_text, should_end_session))


# --helper for random fact

def getRandomFact(day, month):
    url = 'http://numbersapi.com/%i/%i/date' %(month, day)
    text = urllib2.urlopen(url).read()
    return text



# --helpers for the time

def closestDistanceToZero(number, maxn):
    number = number%maxn
    if abs(number-maxn) < number:
        return number-maxn
    return number


def getHour(hour):
    numbersText = ["TWELVE", "ONE", "TWO", "THREE", "FOUR", "FIVE", "SIX", "SEVEN", "EIGHT", "NINE", "TEN", "ELEVEN"]
    return numbersText[hour];

def getDirection(t):
    cases = {-2: "CLOSE TO", -1: "NEARLY", 0: "EXACTLY", 1: "", 2: "ALREADY"}
    return cases.get(t, "");

def getIntervalPrefix(minutes):
    cases = {0: "",5: "FIVE PAST",10: "TEN PAST", 15 : "QUARTER PAST", 20 : "TWENTY PAST", 25 : "FIVE TO HALF PAST", 30 : "HALF PAST", 35 : "TWENTYFIVE TO", 40 : "TWENTY TO", 45 : "QUARTER TO", 50 : "TEN TO", 55 : "FIVE TO"}
    return cases.get(minutes, "")

def getIntervalSuffix(minutes):
    if minutes == 0:
            return "O'CLOCK";
    else:
        return "";



def time2text(hour, minutes):
    
    hour = hour%12
    minutes_interval = 5 * (minutes/5)
    direction_number = closestDistanceToZero(minutes%5, 5)
    if (direction_number < 0):
        minutes_interval += 5
    
    output = ""
    
    output += getDirection(direction_number);
    output += " " + getIntervalPrefix(minutes_interval);
    output += " " + getHour(hour);
    output += " " + getIntervalSuffix(minutes_interval);
    
    return output

# --------------- Helpers that build all of the responses ----------------------


def build_speechlet_response(output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }

