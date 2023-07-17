# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions

# dispatcher.utter_message(text='The info of: ' + str(condition))
# dispatcher.utter_message("Here is the address of the {}".format(condition))
# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
import pandas as pd
from rasa_sdk.events import SlotSet
from rasa_sdk.events import UserUtteranceReverted


class ActionInfo(Action):

    def name(self) -> Text:
        return "action_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        condition = tracker.get_slot('condition')
        infotype = tracker.get_slot('infotype')
        df = pd.read_csv('Data_Mayo.csv', sep=',')
        data = df[df['Condition'] == condition]
        result2 = data[infotype].values[0]
        dispatcher.utter_message(text="Here you go!")
        dispatcher.utter_message(text=result2)
        dispatcher.utter_message(response="utter_next")
        return [SlotSet('condition', None), SlotSet('infotype', None)]


class ValidateInfoForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_info_form"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # dispatcher.utter_message(response='utter_next')
        return []

    def validate_condition(
            self,
            slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `condition` value."""

        # Checking if slot_value i.e Condition name is in first column of database
        print("Inside validate condition")
        df = pd.read_csv('Data_Mayo.csv', sep=',')
        first_column = df['Condition'].values
        if slot_value not in first_column:
            dispatcher.utter_message(text="Sorry, I don't have information regarding that.")
            return {"condition": None}
        return {"condition": slot_value}

    def validate_infotype(
            self,
            slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict,
    ) -> Dict[Text, Any]:

        df = pd.read_csv('Data_Mayo.csv', sep=',')
        print("Inside validate infotype")
        headers = df.columns.values[1:]
        if slot_value not in headers:
            dispatcher.utter_message(text="Sorry, I don't have information regarding that.")
            return {"infotype": None}
        return {"infotype": slot_value}

    def submit(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict]:

        # dispatcher.utter_message(response='utter_next')

        return [SlotSet('condition', None), SlotSet('infotype', None)]


class ActionDefaultFallback(Action):
    """Executes the fallback action and goes back to the previous state
    of the dialogue"""

    def name(self) -> Text:
        return "action_default_fallback"

    async def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(response="utter_default")

        # Revert user message which led to fallback.
        return []

class ActionDefaultFallback(Action):
    """Executes the fallback action and goes back to the previous state
    of the dialogue"""

    def name(self) -> Text:
        return "action_default_fallback"

    async def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(response="utter_default")

        # Revert user message which led to fallback.
        return []
