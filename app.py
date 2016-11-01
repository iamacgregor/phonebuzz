from flask import Flask, request
from twilio import twiml
from twilio.rest import TwilioRestClient
from threading import Timer

app = Flask(__name__)


@app.route("/phase1", methods=['GET', 'POST'])
def phase1():
    resp = twiml.Response()

    with resp.gather(action='/fizzBuzz') as gather:
        gather.say('How much Fizz Buzz output would you like? Please enter a number.')

    resp.redirect('/phase1')

    return str(resp)


@app.route("/phase2", methods=['GET', 'POST'])
def phase2():
    resp = twiml.Response()

    with resp.gather(action='/call') as gather:
        gather.say('Who would you like to call to play Phone Buzz?')

    resp.redirect('/phase2')

    return str(resp)


@app.route("/phase3", methods=['GET', 'POST'])
def phase3():
    resp = twiml.Response()

    with resp.gather(action='/callWithDelay', finishOnKey='*') as gather:
        gather.say('Please enter the number you would like to call to play Phone Buzz, followed by a pound sign, and then the amount of time you would like to delay until the call is made, in seconds.')

    resp.redirect('/phase3')

    return str(resp)

@app.route("/call", methods=['GET', 'POST'])
def call():
    resp = twiml.Response()

    from_number = request.values['From']

    if 'Digits' in request.values:
        to_number = request.values['Digits']
        makeCall(to_number, from_number, "http://f19a3de5.ngrok.io/phase1")
    else: 
        resp.say("Please enter a valid phone number.")
        resp.redirect('/phase2')

    return str(resp)

@app.route("/callWithDelay", methods=['GET', 'POST'])
def callWithDelay():
    resp = twiml.Response()

    from_number = request.values['From']

    if 'Digits' in request.values:
        try:
            if request.values['Digits'].find('#') == -1:
                resp.say("Please enter a valid delay.")
                resp.redirect('/phase3')
            else:
                split_digits = request.values['Digits'].split('#')
                to_number = split_digits[0]
                Timer(int(split_digits[1]), makeCall, (to_number, from_number, "http://f19a3de5.ngrok.io/phase1")).start()
        except:
            resp.say("Please enter a valid phone number.")
            resp.redirect('/phase3')
    else: 
        resp.say("Please enter a valid phone number and delay.")
        resp.redirect('/phase3')

    return str(resp)

def makeCall(to_number, from_number, url):
    account_sid = "AC513097598a727063562c3ce43c08830b"
    auth_token  = "5652cc037bc225d6fabf0479948a54a2"
    client = TwilioRestClient(account_sid, auth_token)
    new_call = client.calls.create(to=to_number, from_=from_number, url=url)

@app.route('/fizzBuzz', methods=['GET', 'POST'])
def fizzBuzz():
    resp = twiml.Response()

    if 'Digits' in request.values:
        choice = request.values['Digits']

        how_much = int(choice)
        fb = ""
        for i in range(1, how_much+1):
            if i%3==0 and i%5==0:
                fb += "Fizz Buzz, "
            elif i%3==0:
                fb += "Fizz, "
            elif i%5==0:
                fb += "Buzz, "
            else:
                fb += str(i) + ", "
        resp.say(fb)
        return str(resp)
    else:
        resp.say("Please enter a valid number.")

    resp.redirect('/phase1')

    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)