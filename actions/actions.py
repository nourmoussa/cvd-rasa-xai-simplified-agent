# This is a simple example for a custom action which utters "Hello World!"

#from typing import Any, Text, Dict, List
#from rasa_sdk import Action, Tracker
#from rasa_sdk.executor import CollectingDispatcher
#from rasa_sdk.events import SlotSet
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []


# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


import time
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher
import requests
import json

# This will be replaced with a representation of risks for different slot values
# todo: should include text for naming, is it addressable, and map to a live domain (to connect to a motivation type)
# This db is the knowledge base for risk factors a person may have, and if and how they can be addressed
 # Answers to the assessment questions (slots) provide the specific situation of an individual
 # 
 # The key is the risk factor label
 # The value should probably be a type dict, rather than array.   
 # factor_slot: [slot_name, risk_values, factor_explain, factor_type, factor_mot] 
 # 0 - slot_name: required slots in assessment form (and load in buttons)
 # 1 - risk_values: how much the attribute adds to the total risk
 # 2 - factor_explain: text to explain what the factor means
 # 3 - factor_type can be fixed, environmental, behavioural, management   
 # 4 - factor_mot: motivation category driving this factor - to be used to find relationships/groups
 # 5 - factor_resource: suggestiomn to read resource to reduce risk (only for )

# this knowledge base reflects prediction and management variables
# risk_db = {
#     "Man": ["gender",0.5, "Man", "fixed", ""],  # fix
#     "Woman": ["gender", 1.0, "Woman", "fixed", ""],
#     # "diagnosed_under_6months": ["age",1.0, "having been diagnosed under 6 months ago", "fixed", ""],
#     # "diagnosed_over_6months": ["age", 1.0, "having been diagnosed over 6 months ago", "fixed", ""],
#     "affirm_a": ["alco",1.0, "Drinking alcohol", "fixed", ""],
#     "deny_a": ["alco",0.0, "Not drinking alcohol", "fixed", ""],
#     "deny_s": ["smoke", 0.0, "smoking", "fixed", ""],
#     "affirm_s": ["smoke",1.0, "not smoking", "fixed", ""],
#     "affirm_pe": ["daily_activity", 0.3, "interferring with daily activity", "fixed", ""],
#     "deny_pe": ["daily_activity", 0.0, "not interferring with daily activity", "fixed", ""]
# }

sleep_time = 0.5 # not woking when in loop, it flushes all messages together

factor_slots = ["gender", "alco", "age", "smoke", "daily_activity", "height", "weight"]

class RiskAssessment(Action):

    def name(self) -> Text:
        return "action_risk_assessment"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        try:
            url = 'http://127.0.0.1:5000'
            payload = json.dumps({
                # "age": int(tracker.get_slot("age")),
                "age":tracker.get_slot("age"),
                "gender": int(tracker.get_slot("gender")),
                "height": tracker.get_slot("height"),
                "weight": tracker.get_slot("weight"),
                "smoke": int(tracker.get_slot("smoke")),
                "alco": int(tracker.get_slot("alco")),
                "active": int(tracker.get_slot("daily_activity"))
                })
            headers = {
                'Content-Type': 'application/json'
            }

            response = requests.request("POST", url, headers=headers, data=payload)
            result=response.json()
            if result["result"]==1:
                dispatcher.utter_message(text="you have cardio problems")
            elif result["result"] == 0:
                dispatcher.utter_message(text="you are healthy")  
            
        except: 
            dispatcher.utter_message(text="error")
            return []
        #     r = requests.post(url, json={"age":tracker.get_slot("age"),"gender":tracker.get_slot("gender"),"height":tracker.get_slot("height"),"weight":tracker.get_slot("weight"),"smoke":tracker.get_slot("smoke"),"alco":tracker.get_slot("alco"),"active":tracker.get_slot("active")})   
        #     dispatcher.utter_message(text="r")
        # except: 
        #     dispatcher.utter_message(text="error")
        #     return []
            # dispatcher.utter_message(text="test")

            # url = "http://127.0.0.1:5000"

            # payload = json.dumps({

            # "age": int(tracker.get_slot("age")),

            # "gender": int(tracker.get_slot("gender")),

            # "height": int(tracker.get_slot("height")),

            # "weight": int(tracker.get_slot("weight")),

            # "smoke": int(tracker.get_slot("smoke")),

            # "alco": int(tracker.get_slot("alco")),

            # "active": int(tracker.get_slot("active"))
            # })

            # headers = {

            # 'Content-Type': 'application/json'
            # }

            # response = requests.request("POST", url, headers=headers, data=payload)
            # dispatcher.utter_message(text=response.text)


    #     # print(risk_db.keys()) 
    #     Risk = 0.0
    #     factor_risk = 0.0
    #     # slots to be processed (others may not be used here)
    #     # All slots should have been filled

    #     for x in factor_slots:
    #         factor_key = tracker.get_slot(x)
    #         print("key: ",factor_key)
    #         dict = risk_db[factor_key]
    #         print("dict", dict)
    #         factor_risk = dict[1]
    #         Risk = Risk +  factor_risk
    #         factor_explain = dict[2]
    #         factor_type = dict[3]
    #         if factor_type == "environmental" or "management":
    #             if factor_risk > 0.0:
    #                 print("{factor_explain} adds {factor_risk} to your total risk ") 
    #         # add all types of risks        
    #         Risk = Risk +  factor_risk
    #    # todo: have many varaibles and finish with the coding assessment formula 
    #     msg = f"Your total risk is {Risk}. You might be able to reduce it"
    #     dispatcher.utter_message(text=msg)  
    #     # This could be followed in the rule/story by an offer to discuss ways to reduce it

        # return []

# # describes what factors the person could change
# class RiskManagement(Action):
#     def name(self) -> Text:
#         return "risk_management"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

#         # print(risk_db.keys()) 
#         Risk = 0.0
#         factor_risk = 0.0
#         # slots to be processed (others may not be used here)
#         # All slots should have been filled

#         for x in factor_slots:
#             factor_key = tracker.get_slot(x)
#             #print("key: ",factor_key)
#             dict = risk_db[factor_key]
#             print("dict", dict)
#             factor_risk = dict[1]
#             Risk = Risk +  factor_risk
#             factor_explain = dict[2]
#             factor_type = dict[3]
#             if factor_type == "environmental" or "management":
#                 if factor_risk > 0.0:
#                     print("{factor_explain} adds {factor_risk} to your total risk ")
#                     msg = f"{factor_explain} adds {factor_risk} to your total risk "
#                     print(msg)
#                     # dispatcher.utter_message(text=msg) 
#                     # time.sleep(sleep_time)
#                     slow_response(msg, dispatcher)
#                 Risk = Risk +  factor_risk

#         return []

def slow_response (msg, dispatcher: CollectingDispatcher):
    time.sleep(sleep_time)
    dispatcher.utter_message(text=msg) 
    return []

#age 
class ActionReceiveAge(Action):
    def name(self) -> Text:
        return "action_set_age"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        age = tracker.latest_message['age']

        dispatcher.utter_message(text="Your age is {age}")
        #return [SlotSet("age")]
        return[]

#BMI
class WeightSET(Action):
    def name(self) -> Text:
        return "action_set_weight"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        try:
       
           tracker.get_slot("weight")
        except:
            dispatcher.utter_message(text="Error Occur!")

        dispatcher.utter_message(text="Weight set")
        return []
        #return [SlotSet("weight", weight)]

class HeightSET(Action):
    def name(self) -> Text:
        return "action_set_height"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        try:
            tracker.get_slot("height")
        except:
            dispatcher.utter_message(text="Error Occur!")
        dispatcher.utter_message(text="Height set")
        return []


# def convert_cm_to_meter(height):
#     return float((height)/100)

def bmi_calculation(weight, height):
    #return float((weight)/(height*height))
    return float(weight)/((height**2))

def get_bmi_status(bmi):
    if bmi < 15:
       return  "Unfortunately, you fall into the severely underweight percentile."
    elif bmi >= 15 and bmi <16:
        return "Severely underweight"
    elif bmi >=16 and bmi < 18.5:
        return "Underweight"
    elif bmi >= 18.5 and bmi < 25: 
        return "Good news! You fall into the normal healthy BMI percentile."
    elif  bmi >= 25 and bmi <30:
        return "Unfortunately, you fall into the overweight percentile. It is important to focus on factors you can control, such as weight. Weight gain increases blood pressure, insulin resistance and cholesterol, which affect the CVD risk."
    elif bmi>= 30 and bmi <35:
        return "Unfortunately, you fall into the moderately obese percentile. It is important to focus on factors you can control, such as weight. Weight gain increases blood pressure, insulin resistance and cholesterol, which affect the CVD risk."
    # elif bmi >= 35 and bmi <40:
    #     return "Unfortunately, you fall into the severely overweight percentile. It is important to focus on factors you can control, such as weight. Weight gain increases blood pressure, insulin resistance and cholesterol, which affect the CVD risk."
    else:
        return "Unfortunately, you fall into the severely overweight percentile. It is important to focus on factors you can control, such as weight. Weight gain increases blood pressure, insulin resistance and cholesterol, which affect the CVD risk."


class CalculeteBMI(Action):
    def name(self) -> Text:
        return "action_calculate_bmi"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        try:
            height =  float(tracker.get_slot("height"))
            print(height)
            # height = convert_cm_to_meter(height)
       
            weight = float(tracker.get_slot("weight"))
            print(weight)
            bmi = bmi_calculation(weight, height)
            bmi_status = get_bmi_status(bmi)
            dispatcher.utter_message(text="Your BMI is: "+ str(round(bmi, 2))+ ". " + bmi_status)
        except:
            dispatcher.utter_message(text="Error Occur!")
            return []
