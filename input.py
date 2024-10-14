import json
import random

ring_art = """                                                                                 
                 ...                              
              .::::::::..                         
             ::.       ..:::.                     
            .::          ..:-:.                   
            :-:            ..--:                  
           ..-:              .:::                 
           ..:-:              .:::                
            ..::               .::.               
             ..::.             .:::               
              ..--:             .::               
               ..:::.           .-:               
                 ..::..        .::                
                   ...::::::.:::.                 
                      .........                   
                                                  
###   ###   #  #   ##          ##   ####  ###   #  #  ###   
#  #   #    ## #  #  #        #  #  #      #    #  #  #  #  
#  #   #    ## #  #            #    ###    #    #  #  #  #  
###    #    # ##  # ##          #   #      #    #  #  ###   
# #    #    # ##  #  #        #  #  #      #    #  #  #     
#  #  ###   #  #   ###         ##   ####   #     ##   #     
                                                  
"""

# Define colors
RED = "\033[0;31m"
GREEN = "\033[0;32m"
BLUE = "\033[0;34m"
NC = "\033[0m"  # No Color

# Display a beautiful prompt
print(ring_art)

is_lead = input(f"{BLUE}Will you be the leading this ring round (y/N)?{NC}")

members = []
if is_lead.lower() == "y":
    leader = input(f"{BLUE}Add your email as a ring member: {NC}")
    members.append(leader)
    while True:
        member = input(
            f"{BLUE}Add new a ring member (Leave empty to stop adding peers): {NC}"
        )
        if not member:
            break
        members.append(member)

    members.append(leader)

# secret_number = input(f"{BLUE}Secret Number: {NC}")
secret_list = input(
    f"{BLUE}Provide a list of integers (eg: [1,2,3,4,5], leave it empty to generate a new one):  {NC}"
)
if secret_list:
    secret_list = json.loads(secret_list)
else:
    secret_list = [random.randint(0, 100) for _ in range(100)]

bound_min = input(f"{BLUE}Min Bound: {NC}")

bound_max = input(f"{BLUE}Max Bound: {NC}")

epsilon = input(f"{BLUE}Epsilon: {NC}")

# Write the secret number to a file
with open("secret.json", "w") as file:
    file.write(
        json.dumps(
            {
                "data": secret_list,
                "epsilon": epsilon,
                "bound_min": bound_min,
                "bound_max": bound_max,
            }
        )
    )

with open("data.json", "w") as file:
    file.write(json.dumps({"ring": members, "data": 0, "current_index": 0}))

# Confirm the action
print(f"\n\n{GREEN}Everything has been set! Have good fun!{NC}\n\n")
