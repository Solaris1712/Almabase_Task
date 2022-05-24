My solution to Backend Developer Task - Find Duplicate Profiles

OS - Windows x64
Python version - 3.10.4
Requirements.txt provided in the repo

I have provided two scripts that implement the logic slightly differently. In both the solutions, I have made some assumptions that alleviate some tedium of implenting utility logic or any confusion regarding the wording of the question. These are the assumptions that are common to both scripts,

    1. Input profiles are a list of JSON objects holding the data, instead of having a list of Profile objects. We can implement JSON serializers in the models themselves depending on the ORM used in the project/company.

    2. I have assumed that the baseline criteria for flagging two profiles as duplicates is the combined string of "email first_name last_name", and any score change are applied to these profiles only. I am not checking for field matches for profiles that don't have 80% match for the baseline itself. Might be obvious, but stating my assumptions for clarity.
    
    3. There were no instructions regarding this, but I have assumed that two profiles with final scores less than one are not duplicates anyore. I have a function that removes such pairs, but I have not called it in the script.




