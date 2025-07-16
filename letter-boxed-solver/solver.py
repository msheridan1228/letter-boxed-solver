from english_words import get_english_words_set
import pandas as pd
from itertools import permutations


class LetterBoxedSolver:
    def __init__(self, letter_box):
        self.letter_box = letter_box
        self.unique_letters = set(letter for side in letter_box for letter in side)
        self.valid_words = self.get_valid_word_list()
        self.web2lowerset = get_english_words_set(['web2'], lower=True)

    def solve(self):
        valid_words = self.get_valid_word_list()
        print(f"Found {len(valid_words)} valid words.")
        single_word_solution = self.find_single_word_solutions(valid_words, self.unique_letters)
        best_single_word_solution = self.return_best_solution(single_word_solution)
        if best_single_word_solution:
            print(f"Best single word solution: {best_single_word_solution}")
            return best_single_word_solution
        else:
            print("No single word solution found.")
            two_word_solutions = self.find_multi_word_solutions(valid_words, self.letter_box, max_words=2)
            if two_word_solutions:
                print(f"Found {len(two_word_solutions)} two-word solutions.")
                best_two_word_solution = self.return_best_solution(two_word_solutions)
                print(f"Best two word solution: {best_two_word_solution}")
                return best_two_word_solution
            else:
                print("No two-word solutions found. Breaking for now until multi words is fixed!")

    def get_valid_word_list(self):
        valid_words = set()
        for word in self.web2lowerset:
            if self.is_valid_word(word):
                valid_words.add(word)
        return valid_words

    def is_valid_word(self, word):
        ## must be in the word list
        if word not in self.web2lowerset:
            return False
        ## must be more than 2 letters
        if len(word) < 3:
            return False
        ## must contain only letters from the letter box
        if any(letter not in self.unique_letters for letter in word):
            return False
        ## must not contain two letters from the same side in a row
        for i in range(len(word) - 1):
            if (word[i] in self.letter_box[0] and word[i + 1] in self.letter_box[0]) or \
               (word[i] in self.letter_box[1] and word[i + 1] in self.letter_box[1]) or \
               (word[i] in self.letter_box[2] and word[i + 1] in self.letter_box[2]) or \
               (word[i] in self.letter_box[3] and word[i + 1] in self.letter_box[3]):
                return False
            ## must not contain the same letter more than once in a row
            if word[i] == word[i + 1]:
                return False
        return True

    def is_valid_word(self, word):
        ## must be in the word list
        if word not in self.web2lowerset:
            return False
        ## must be more than 2 letters
        if len(word) < 3:
            return False
        ## must contain only letters from the letter box
        if any(letter not in self.unique_letters for letter in word):
            return False
        ## must not contain two letters from the same side in a row
        for i in range(len(word) - 1):
            if (word[i] in self.letter_box[0] and word[i + 1] in self.letter_box[0]) or \
            (word[i] in self.letter_box[1] and word[i + 1] in self.letter_box[1]) or \
            (word[i] in self.letter_box[2] and word[i + 1] in self.letter_box[2]) or \
            (word[i] in self.letter_box[3] and word[i + 1] in self.letter_box[3]):
                return False
            ## must not contain the same letter more than once in a row
            if word[i] == word[i + 1]:
                return False
        return True

    def get_valid_word_list(self):
        valid_words = set()
        for word in self.web2lowerset:
            if self.is_valid_word(word):
                valid_words.add(word)
        return valid_words

    ## want to find words tha use the most letters from the letter box
    def score_words(self, word_list, unique_letters):
        return len(set(letter for word in word_list for letter in word if letter in unique_letters))

    def is_single_word_solution(self, word, unique_letters):
        if self.is_valid_word(word):
            if self.score_words([word], unique_letters) == len(unique_letters):
                return True
        return False

    def find_single_word_solutions(valid_words, unique_letters):
        single_word_solutions = set()
        for word in valid_words:
            if is_single_word_solution(word, unique_letters):
                single_word_solutions.add(word)
        print(f"Found {len(single_word_solutions)} single word solutions.")
        return single_word_solutions

    def is_valid_solution(solution, unique_letters):
        ## check if the solution is valid
        for word in solution:
            if not is_valid_word(word):
                return False
        ## check if the solution uses all letters from the letter box
        if score_words(solution, unique_letters) != len(unique_letters):
            return False
        ## check if last letter of each word matches first letter of next word
        for i in range(len(solution) - 1):
            if solution[i][-1] != solution[i + 1][0]:
                return False
        return True

    def find_two_word_solutions(valid_words, letter_box):
        two_word_solutions = set()
        for word1 in valid_words:
            for word2 in valid_words:
                if is_valid_solution([word1, word2], letter_box):
                    two_word_solutions.add((word1, word2))
        print(f"Found {len(two_word_solutions)} two word solutions.")
        return two_word_solutions

    ## OOM - need to adjust this -
    def find_multi_word_solutions(valid_words, unique_letters, max_words=3):
        multi_word_solutions = []
        # while len(multi_word_solutions) < 50:
        for word in valid_words:
            if is_valid_solution([word]):
                multi_word_solutions.append([word])
                
            valid_next_words = [w for w in valid_words if w[-1] == word[0] and w != word]
            for word2 in valid_next_words:
                if is_valid_solution([word1, word2], unique_letters):
                    multi_word_solutions.append(perm)
                if len(multi_word_solutions) >= 50:
                    break
        multi_word_solutions = list(set(multi_word_solutions))  # Remove duplicates
        print(f"Found {len(multi_word_solutions)} multi-word solutions.")
        return multi_word_solutions

    def sort_solutions(solutions):
        ## take in solutions, which is a list of sets
        ## sort by length first then number of letters total
        if not solutions:
            return []
        if len(solutions) == 0:
            return []
        if len(solutions) == 1:
            return solutions
        solutions_df = pd.DataFrame({'solutions': solutions, 'num_words': [len(x) for x in solutions], 'total_length': [sum(len(word) for word in x) for x in solutions]})
        sorted_solutions = solutions_df.sort_values(by=['total_length', 'num_words'], ascending=[True, True])

        return sorted_solutions['solutions'].tolist()


    def return_best_solution(solutions):
        sorted_solutions = sort_solutions(solutions)
        if not sorted_solutions:
            return None
        return sorted_solutions[0]
