# Import 2 levels up for speck
import os
import sys

from speck import ChatConfig, Message, Prompt, Response, Speck, Stream

client = Speck()

# client.chat.log(
#     messages=Prompt(
#         messages=[
#             Message(role="system", content="You respond with 1 word answers."),
#             Message(
#                 role="user",
#                 content="Respond with YES or NO. Do you understand? Then, recite the A B Cs",
#             ),
#         ],
#     ),
#     config=ChatConfig(
#         model="anthropic:claude-2",
#         temperature=0.0,
#         stream=True,
#         _log=True,
#     ),
#     response=Response(content="hi")
# )
