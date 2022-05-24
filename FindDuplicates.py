from typing import List
from thefuzz import fuzz
from thefuzz import process
from pprint import pprint


#Note
#emfnln --- shorthand for "email first_name last_name"




# checks for duplicates of the passed emfnln string in the array of previously encountered emfnln strings.
# cutoff decides the cutoff score for the duplicates.
# returns a list of profile indexes.
def check_emfnln(single,choices,cutoff=80):

    if len(choices) <=0:
        return -1   
    result = process.extractBests(single,choices,scorer =fuzz.token_sort_ratio,score_cutoff=cutoff)
    duplicates_index = [choices.index(ele[0]) for ele in result]
    return duplicates_index


# A helper function to remove pairs with final scores less than 1. Although not stated in the question, I have gone ahead and implemented this,
# although not called it in the script.
def purge_negatives(duplicates_dict:dict):
    for pair in duplicates_dict.copy():
        if duplicates_dict[pair]['match_score'] <=0:
            duplicates_dict.pop(pair)




# Prints out the duplicates dictionary as per the questions format. Nothing fancy here.
def print_output(duplicates_dict):
    for pair in duplicates_dict.values():
        print(f"Profile ID {pair['id_1']} and Profile ID {pair['id_2']}.\nTotal Match Score : {pair['match_score']}.\nMatching Attributes : {pair['matching_attributes']}.\nNon Matching Attributes : {pair['non_matching_attributes']}\nIgnored Attributes : {pair['ignored_attributes']}")
        print("=================================================================================")




# the piece de resistance! 
# Essentially a single loop to go through the profiles and a dictionary to cache details. Also a dictionary to store duplicate pairs and relevant details.
# First I get some baseline duplicates (based on emfnln matching) and assign them a score of 1. Then I go through the the fields and update the score automatically.
# Then I print the outputs as detailed in the question.
def find_duplicates(profiles:List,profile_fields:List[str]):
    
    # I prepare the list by removing the 3 separate entries and making them a single one. Useful in the later stages to avoid multiple If statements.
    # Also makes sense to have one instead of 3 seperate ones, based on the needs.
    profile_fields.remove('email')
    profile_fields.remove('first_name')
    profile_fields.remove('last_name')
    profile_fields.append('email first_name last_name')

    # Initialize the storage variables needed for the logic.
    profile_names_list = []
    duplicates_table = {}
    
    # I go through each profile and compare them to profiles encountered before it. One Fuzzy string match later, we have a list of duplicates for the profile!
    # With the list of duplicates in hand, I go through the list and create entries in the duplicates_table with relevant details.
    for ele in profiles:
        cur_index = profiles.index(ele)

        emfnln = " ".join([ele[temp] for temp in ["email","first_name","last_name"]])
        duplicates = check_emfnln(emfnln,profile_names_list)

        if duplicates != -1:
            for index in duplicates:
                duplicates_table[(cur_index,index)] = { 'id_1': ele['id'],
                                                        'id_2': profiles[index]['id'],
                                                        'match_score':1, 
                                                        'matching_attributes':["email","first_name","last_name"],
                                                        'non_matching_attributes':[],
                                                        'ignored_attributes':[]}
                
        profile_names_list.append(emfnln)
    
    # This is where both scripts differ, this script again iterates through the duplicates_table and compares the fields.
    # This is a bit cleaner imo, and should be equivalent in performance to V2.
    for field in profile_fields:
        if field != 'email first_name last_name':
            for pair in duplicates_table.keys():
                first = profiles[pair[0]].get(field,None)
                second = profiles[pair[1]].get(field,None)
                if first and second:
                    if first == second:
                        duplicates_table[pair]['match_score'] += 1
                        duplicates_table[pair]['matching_attributes'].append(field)
                    else:
                        duplicates_table[pair] -= 1
                        duplicates_table[pair]['non_matching_attributes'].append(field)
                else:
                    duplicates_table[pair]['ignored_attributes'].append(field)
        else:
            continue
    

    # purging negatives and printing output. Uncomment next line to purge pairs with negative scores.
    #purge_negatives(duplicates_table)
    print_output(duplicates_table)

    return duplicates_table




if __name__ == "__main__":

   profile_1 = { 'id': 1, 
   'email': 'knowkanhai@gmail.com', 
   'first_name': 'Kanhai', 
   'last_name': 'Shah', 
   'class_year': 2012, 
   'date_of_birth': '1990-10-11'}

   profile_2 = { 'id': 2, 
   'email': 'knowkanhai@gmail.com', 
   'first_name': 'Kanhai1', 
   'last_name': 'Shah',
   'class_year': 2012,
   'date_of_birth': '1990-10-11'}


   profile_3 = { 'id': 3, 
   'email': 'knowkanhai+donotcompare@gmail.com', 
   'first_name': 'Kanhai1', 
   'last_name': 'Shah', 
   'class_year': 2012, 
   'date_of_birth':'1990-10-11' }

   profile_4 = { 'id': 4, 
   'email': 'knowkanhai@gmail.com', 
   'first_name': 'Kanhai', 
   'last_name': 'Shah', 
   'class_year': None, 
   'date_of_birth': None}

   profile_5 = { 'id': 5, 
   'email': 'rajalalluhai@gmail.com', 
   'first_name': 'raja', 
   'last_name': 'lallu', 
   'class_year': None, 
   'date_of_birth': None}

   profile_6 = { 'id': 6, 
   'email': 'rajalal@gmail.com', 
   'first_name': 'Lal', 
   'last_name': 'Raja', 
   'class_year': None, 
   'date_of_birth': None}

   find_duplicates([profile_1,profile_2,profile_3,profile_4,profile_5,profile_6],
    ['email','first_name', 'last_name', 'class_year', 'date_of_birth'])


