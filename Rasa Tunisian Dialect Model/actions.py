# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
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

from typing import Text, List, Any, Dict
import pickle
import catboost
import numpy as np
import pandas as pd

from rasa_sdk import Tracker, FormValidationAction, Action
from rasa_sdk.events import EventType, SlotSet
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict

class ValidateCreditRiskForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_credit_risk_form"

    def validate_duration_in_month(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `duration_in_month` value."""
        dispatcher.utter_message(text=f"Hachtek b credit 3ala {slot_value} chhar")
        return {"duration_in_month": slot_value}

    def validate_credit_amount(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `credit_amount` value."""

        dispatcher.utter_message(text=f"OK, hachtek b {slot_value} DNT")
        return {"credit_amount": slot_value}

    def validate_present_residence_since(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `present_residence_since` value."""

        dispatcher.utter_message(text=f"3andek {slot_value} resident fil bled")
        return {"present_residence_since": slot_value}

    def validate_number_credit(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `number_credit` value."""

        dispatcher.utter_message(text=f"Enti mekhou {slot_value} cridiet kbal hetha, OK")
        return {"number_credit": slot_value}

    def validate_number_people_maintenance(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `number_people_maintenance` value."""

        dispatcher.utter_message(text=f"Donc 3andek {slot_value} 3bed possible ykhalles fi blastek ken ma najjamtech")
        return {"number_people_maintenance": slot_value}
    
    
class Credit_risk_classifier(Action):
    """Credit_risk_classifier"""

    def name(self) -> Text:
        """Unique identifier of the action"""

        return "credit_risk_classifier"
    
    

    def run(self, dispatcher, tracker: Tracker, domain):
        
        slot_key = {
            'Duration_in_month': [tracker.get_slot('duration_in_month')],
            'Credit_amount': [tracker.get_slot('credit_amount')],
            'Installment_rate_in percentage_of_disposable_income': [4],
            'Present_residence_since': [tracker.get_slot('present_residence_since')], 
            'Age': [24], 
            'Number_credit': [tracker.get_slot('number_credit')],
            'Number_people_maintenance': [tracker.get_slot('number_people_maintenance')], 
            'Credit_history_critical account': [0],
            'Credit_history_delay in paying off': [0],
            'Credit_history_existing credits paid back duly till now': [1],
            'Credit_history_no credits taken': [0], 
            'Purpose_car (new)': [1],
            'Purpose_car (used)': [0], 
            'Purpose_domestic appliances': [0],
            'Purpose_education': [0], 
            'Purpose_furniture/equipment': [0], 
            'Purpose_others': [0],
            'Purpose_radio/television': [0], 
            'Purpose_repairs': [0], 
            'Purpose_retraining': [0],
            'Status_Sex_male:divorced/separated': [0], 
            'Status_Sex_male:married/widowed': [0],
            'Status_Sex_male:single': [0], 
            'Other_debtors_guarantors_guarantor': [0],
            'Other_debtors_guarantors_none': [1], 
            'Property_real estate': [1],
            'Property_savings agreement/life insurance': [0],
            'Property_unknown / no property': [0], 
            'Other_installment_plans_none': [1],
            'Other_installment_plans_store': [0], 
            'Housing_own': [1], 
            'Housing_rent': [0],
            'foreign_worker_yes': [1], 
            'Checking_account_<0 DM': [1],
            'Checking_account_>= 200 DM ': [0], 
            'Checking_account_no checking account': [0],
            'Present_employment_since_4<= <7 years': [0],
            'Present_employment_since_<1 years': [0],
            'Present_employment_since_>=7 years': [0],
            'Present_employment_since_unemployed': [0],
            'Savings_account_500 <= < 1000 DM': [0], 
            'Savings_account_<100 DM': [1],
            'Savings_account_>= 1000 DM': [0], 
            'Savings_account_no savings account': [0],
            'Telephone_yes': [0], 
            'Job_skilled employee / official': [0],
            'Job_unemployed/ unskilled  - non-resident': [0], 
            'Job_unskilled - resident': [1],
            'foreign_worker_yes': [1],
            'foreign_worker_no': [0]
        }


        inputData = np.array(pd.DataFrame(slot_key))


        prediction = ClassifierPipeline_credit().get_prediction(inputData)

        
        Risk = prediction

        if Risk == 1:
            Risk = f"Mabrouk, tnajjem tematta3 bel credit elli theb 3lih"
        else:
            Risk = f"Net2assfou ama mannajmouch na3tiwek credit, desoler"
        # always guess US for now
        return [SlotSet("risk", Risk)]

class ClassifierPipeline_credit:
    """Load in classifier & encoders"""

    def name(self) -> Text:
        
        return "credit_risk_1"

    def encoder(self, inputData):
        scaler= pickle.load(open("actions/MLModels/scaler.sav", 'rb'))
        return scaler.transform(inputData)
    
    def get_prediction(self, inputData):
        model = pickle.load(open("actions/MLModels/finalized_model.sav", 'rb'))
        scaledData = self.encoder(inputData)
        return model.predict(scaledData)[0]


class ActionTellID(Action):
    """Informs the user about the conversation ID."""

    def name(self) -> Text:
        return "action_tell_id"

    def run(
        self, dispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:

        conversation_id = tracker.sender_id

        dispatcher.utter_message(f"{conversation_id}")

        return []
