from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import APIView
from rest_framework.permissions import AllowAny
from step import serializer, models
from step.nlpFunc import bag_of_words, tokenize, NeuralNet
import torch
import json
import os
from random import choice
import nltk


# ai model
bot_name = "Vanila"
jsonFile_path = os.path.join(os.path.dirname(__file__), './data/intents.json')
FILE_path = os.path.join(os.path.dirname(__file__), './data/data.pth')

class SupportView(APIView):
    # permission_classes = [AllowAny]
    
    def post(self, request, format=None):
        # user message
        message = request.data.get("message")
        user = request.user
        
        # Determine the device
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

        # Load intents
        with open(jsonFile_path, 'r') as f:
            intents = json.load(f)

        # Load model data with map_location to handle CPU-only environments
        data = torch.load(FILE_path, map_location=torch.device('cpu'))

        input_size = data["input_size"]
        hidden_size = data["hidden_size"]
        output_size = data["output_size"]
        all_words = data["all_words"]
        tags = data["tags"]
        model_state = data["model_state"]

        # Initialize the model
        model = NeuralNet(input_size, hidden_size, output_size).to(device)
        model.load_state_dict(model_state)
        model.eval()
    
        # ? main ai 
        # Tokenize and create bag of words
        tokenized_message = tokenize(message)
        X = bag_of_words(tokenized_message, all_words)
        X = X.reshape(1, X.shape[0])  # Reshape for the model input
        X = torch.from_numpy(X).to(device)  # Convert to tensor and move to the same device as the model

        # Get model output
        output = model(X)
        _, predicted = torch.max(output, dim=1)  # Get the index of the max log-probability
        tag = tags[predicted.item()]  # Get the corresponding tag

        # Calculate probabilities
        probs = torch.softmax(output, dim=1)
        prob = probs[0][predicted.item()]

        # Check if the probability is above a threshold
        for intent in intents["intents"]:
            if tag == intent["tag"]:
                bot_response = choice(intent["responses"])
                break
            
        
        # save data
        if bot_response:
            step_instance = models.StepSupport(
                sender = user,
                sender_message = message,
                receiver_message = bot_response
            )
            step_instance.save()
            
            context = {
                "status": 200,
                "data": bot_response,
                "error": "null"
            }
        else:
            context = {
                "status": 404,
                "data": "null",
                "error": "we couldn't found any answer"
            }
            
        
            
        
        return Response(context,status.HTTP_200_OK)