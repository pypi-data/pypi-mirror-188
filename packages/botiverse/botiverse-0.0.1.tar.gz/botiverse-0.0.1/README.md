# Botiverse
A library that imports chatbots from other galaxies

### Installation
```
pip install botiverse
```

### Get started
Try to import and playaround with the Basic Chat Bot:

```Python
from Botiverse import BasicChatBot

# Make a new chatbot and give it a name
Max = BasicChatBot("Max")
# Train the chatbot
Max.train("abcdefgh")
# Ask the chatbot a question
response = Max.infer("Can you tell me a joke?")
print(response)
```
