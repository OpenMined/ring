import json

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

# print(f"{BLUE}Please, fill the fields in order to setup your peer for the ring app:{NC}\n")
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

secret_number = input(f"{BLUE}Secret Number: {NC}")


# Write the secret number to a file
with open("secret.txt", "w") as file:
    file.write(secret_number)

with open("data.json", "w") as file:
    file.write(json.dumps({"ring": members, "data": 0, "current_index": 0}))

# Confirm the action
print(f"\n\n{GREEN}Everything has been set! Have good fun!{NC}\n\n")
