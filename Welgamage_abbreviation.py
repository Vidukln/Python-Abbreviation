#Reference: https://my.dundee.ac.uk/ultra/courses/_81072_1/outline
#Reference: Python documentation https://docs.python.org/3/
#Function 01 - This function will handles the process of reading letter scores
def read_letter_scores(file_path):
    #This line will create a dictionary to store key valuyes pairs
    #In this case it will store letters and their respective scores
    letter_scores = {}

    #Open Value.txt file and read values for each letter
    #Then strip each line into two parts assigning letter to letter variable and value to score variable
    #Finally convert score to integer values so that we can use it in our calculations
    #Originally score is considered as a string
    with open(file_path, 'r') as file:
        for line in file:
            letter, score = line.strip().split()
            letter_scores[letter] = int(score)
    print(letter_scores)
    return letter_scores

#Function 02 - This function will calculate score of each letter considering its position
def calculate_score(word, letter, letter_scores):
    #Letter Values rule implementation
    #First need to get the dictionary created for letter scores
    #position variable will handle the position of each letter
    if letter in letter_scores:
        score = letter_scores[letter]
        position = word.find(letter)

        #Rule states that firts letter always gets 0 score
        if position == 0:
            return 0
        #Part 2 of the rule states that last letter will always score 5 unless the letter is E
        elif position == len(word) - 1:
            #If last letter is E score will be 20
            if letter == 'E':
                return 20
            return 5
        #If the letter is neither the first nor last letter of the word
        else:
            #Calculate the score based on position in the word
            if position == 1:
                return 1 + score
            elif position == 2:
                return 2 + score
            else:
                return 3 + score
    else:
        return 0

#Function 03 - First need to process available words to form abbreviations
#Reference for set : https://docs.python.org/3/library/stdtypes.html#set-types-set-frozenset
def generate_abbreviations(name, letter_scores, used_abbreviations):
    #Removing apostropes and converting to Upper case
    name = name.upper().replace("'", "")
    #This step will split the given input into separete words
    words = name.split()
    #Empty set will be created to store the abbreviations and scores of them
    abbreviations = set()

    #This code part will handle creating the abbreviations and calculating the respective scores
    #Empty set created above will be used to store the abbreviations and scores of them
    #for loop will iterate through all the words available in the words array
    for word in words:
        first_letter = word[0]

        #Iterate through all possible pairs of letters in the word
        #Program will start from index 1 as 0th position will be always the starting letter for abbreviation
        for i in range(1, len(word) - 1):
            for j in range(i + 1, len(word)):
                abbreviation = first_letter + word[i] + word[j]

                #To match the condition this part will check whether the abbreviation is only consist of letter
                #Secondly it will calculate the score for the abbreviation created
                #Finally cretaed abbreviation , score, name will be stored in the abbreviations set
                if abbreviation.isalpha():
                    #Calculate the score for the abbreviation
                    score = calculate_score(word, word[i], letter_scores) + calculate_score(word, word[j], letter_scores)
                    #This line will store the values for abbreviation, score, and name to the set
                    abbreviations.add((abbreviation, score, name))

    #Return the set of abbreviations
    return abbreviations

#Function 04 - This function will identify best abbreviations for each word
def find_best_abbreviation(name, letter_scores, used_abbreviations):
    #First generate abbreviations function will be called inside this function to form all abbreviations for each word
    abbreviations = generate_abbreviations(name, letter_scores, used_abbreviations)
    #valid_abbtreviations list will store all conditions matched and lowest score abbreviation for each word
    valid_abbreviations = []

    #for loop will iterate through each abbreviation, score, and current name
    for abbr, score, current_name in abbreviations:
        #Check if the abbreviation is not in the set of used abbreviations for the current name
        if abbr not in used_abbreviations.get(current_name, set()):
            #if the condition satisfy, add the abbreviation and score to the list of valid abbreviations
            valid_abbreviations.append((abbr, score))

    #If there are multiple valid abbreviations this if else condition will handle it
    if valid_abbreviations:
        #This line will find the minimum score among valid abbreviations
        min_score = min(score for _, score in valid_abbreviations)
        #This line will get abbreviations with the minimum score
        best_abbreviations = [abbr for abbr, score in valid_abbreviations if score == min_score]
        #This will update the set of used abbreviations for the current name
        used_abbreviations.setdefault(name, set()).update(best_abbreviations)
        #Finally it will return the list of best abbreviations
        return best_abbreviations
    else:
        #If no valid abbreviation need return an empty list as given by rules
        return []

#Main function
def main(input_file, output_file, letter_scores_file):
    #Reading letter scores from the values.txt file
    letter_scores = read_letter_scores(letter_scores_file)
    #Create a dictionary to store used abbreviations for each name
    #This will help to keep uniquness of abbreviations created
    used_abbreviations = {}

    #Open the input file and read names into a list
    with open(input_file, 'r') as f:
        names = [line.strip() for line in f.readlines()]

    #Create an empty list to store results
    results = []

    #Iterate through each name of the file
    for name in names:
        #Find the best abbreviations for the current name
        best_abbreviations = find_best_abbreviation(name, letter_scores, used_abbreviations)

        #If there are valid abbreviations
        if best_abbreviations:
            #Write the original name to the results list
            results.append(name)

            #Write each chosen abbreviation to the results list on a new line
            for abbreviation in best_abbreviations:
                results.append(abbreviation)

        else:
            #If no valid abbreviation, write the original name to the results list
            results.append(name)

    #Open the output file and write results
    with open(output_file, 'w') as f:
        f.write('\n'.join(results))

if __name__ == "__main__":
    input_file = "trees.txt"
    output_file = "welgamage_trees_abbrevs.txt"
    letter_scores_file = "values.txt"

    main(input_file, output_file, letter_scores_file)
