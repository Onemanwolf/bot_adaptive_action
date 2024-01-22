# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from botbuilder.core import ActivityHandler, TurnContext, CardFactory

from botbuilder.schema import ChannelAccount, Attachment, Activity, ActivityTypes
import json
import os

ADAPTIVECARDTEMPLATEAVAYA = "resources/adaptiveCardAnswer.json"
class MyBot(ActivityHandler):
    # See https://aka.ms/about-bot-activity-message to learn more about the message and other activity types.

    async def on_message_activity(self, turn_context: TurnContext):
        if turn_context.activity.text != None:
            await self._create_adaptive_card_attachment(turn_context)
        else:
            action =  turn_context.activity.value
            print(action["OverallRating"])
            await turn_context.send_activity(f"You said your answer was: '{ turn_context.activity.value['OverallRating'] }'")
            return
            #await turn_context.send_activity(f"You said '{ turn_context.activity.text }'")

    async def on_members_added_activity(
        self,
        members_added: ChannelAccount,
        turn_context: TurnContext
    ):
        for member_added in members_added:
            if member_added.id != turn_context.activity.recipient.id:
                await turn_context.send_activity("Hello and welcome!")

    async def _create_adaptive_card_attachment(self, turn_context) -> Attachment:
         """
         Load a random adaptive card attachment from file.
         :return:
         """
         card_path = os.path.join(os.getcwd(), ADAPTIVECARDTEMPLATEAVAYA )
         with open(card_path, "rb") as in_file:
            template_json = json.load(in_file)
            data = turn_context.activity.text
            # promptData = json.loads(data)
            # data = promptData["choices"][0]['message']
            # dataIn = data["content"]

            d = template_json["body"]
            i = d[2]['items']
            d = i[1]
            r = d
            r["text"] = r["text"].replace("${data}", str(data))



         adaptive_card_attachment = Activity(
                 attachments=[CardFactory.adaptive_card(template_json)]
            )

         await turn_context.send_activity(adaptive_card_attachment)
