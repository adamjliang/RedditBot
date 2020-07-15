from creative_ai.utils.print_helpers import ppGramJson


class BigramModel():

    def __init__(self):
        """
        Requires: nothing
        Modifies: self (this instance of the NGramModel object)
        Effects:  This is the NGramModel constructor. It sets up an empty
                  dictionary as a member variable.

        This function is done for you.
        """
        self.nGramCounts = {}

    def __str__(self):
        """
        Requires: nothing
        Modifies: nothing
        Effects:  Returns the string to print when you call print on an
                  NGramModel object. This string will be formatted in JSON
                  and display the currently trained dataset.

        This function is done for you.
        """

        return ppGramJson(self.nGramCounts)

    ###############################################################################
    # Begin Core >> FOR CORE IMPLEMENTION, DO NOT EDIT ABOVE OF THIS SECTION <<
    ###############################################################################

    def trainModel(self, text):
        """
        Requires: text is a list of lists of strings
        Modifies: self.nGramCounts, a two-dimensional dictionary. For examples
                  and pictures of the BigramModel's version of
                  self.nGramCounts, see the spec.
        Effects:  this function populates the self.nGramCounts dictionary,
                  which has strings as keys and dictionaries of
                  {string: integer} pairs as values.
        """
        for sentences in text:
            for i in range(len(sentences) - 1):
                if (sentences[i] not in self.nGramCounts):
                    self.nGramCounts[sentences[i]] = {}
                if (sentences[i + 1] not in self.nGramCounts[sentences[i]]):
                    self.nGramCounts[sentences[i]][sentences[i + 1]] = 1
                elif (sentences[i + 1] in self.nGramCounts[sentences[i]]):
                    self.nGramCounts[sentences[i]][sentences[i + 1]] += 1

    def trainingDataHasNGram(self, sentence):
        """
        Requires: sentence is a list of strings
        Modifies: nothing
        Effects:  returns True if this n-gram model can be used to choose
                  the next token for the sentence. For explanations of how this
                  is determined for the BigramModel, see the spec.
        """
        return sentence[-1] in self.nGramCounts

    def getCandidateDictionary(self, sentence):
        """
        Requires: sentence is a list of strings, and trainingDataHasNGram
                  has returned True for this particular language model
        Modifies: nothing
        Effects:  returns the dictionary of candidate next words to be added
                  to the current sentence. For details on which words the
                  BigramModel sees as candidates, see the spec.
        """
        return self.nGramCounts[sentence[-1]]


###############################################################################
# End Core
###############################################################################

###############################################################################
# Main
###############################################################################

if __name__ == '__main__':
    uni = BigramModel()

    text = [['the', 'brown', 'fox'], ['the', 'lazy', 'dog']]
    uni.trainModel(text)
    print(uni)