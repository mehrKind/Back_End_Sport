# import nltk
# from nltk.stem.porter import PorterStemmer
# import numpy as np
# import torch.nn as nn

# # Ensure that the NLTK data is downloaded
# # nltk.download('punkt')
# nltk.download('punkt_tab')
# # Create a stemmer object
# stemmer = PorterStemmer()


# def tokenize(sentence):
#     return nltk.word_tokenize(sentence)


# def stem(word):
#     return stemmer.stem(word.lower())


# def bag_of_words(tokenized_sentence, all_words):
#     """
#     **sentence**: [hello, how, are, you] \n
#     **words** = [Hi, hello, I, you, by, thank, cool]\n
#     **bag** = [0, 1, 0, 1, 0, 0, 0]
#     """
#     tokenized_sentence = [stem(w) for w in tokenized_sentence]
#     bag = np.zeros(len(all_words), dtype=np.float32)
    
#     for idx, w in enumerate(all_words):
#         if w in tokenized_sentence:
#             bag[idx] = 1.0
            
#     return bag


# class NeuralNet(nn.Module):
#     def __init__(self, input_size, hidden_size, num_classes):
#         super(NeuralNet, self).__init__()
#         self.l1 = nn.Linear(input_size, hidden_size)
#         self.l2 = nn.Linear(hidden_size, hidden_size)
#         self.l3 = nn.Linear(hidden_size, num_classes)
#         self.relu = nn.ReLU()
        
#     def forward(self, x):
#         out = self.l1(x)
#         out = self.relu(out)
#         out = self.l2(out)
#         out = self.relu(out)
#         out = self.l3(out)
#         # no activation and no soft max
#         return out
