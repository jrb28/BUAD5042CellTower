# -*- coding: utf-8 -*-
"""
Spyder Editor
"""

import mysql.connector as mySQL

""" global MySQL settings """
mysql_user_name = 'xx'
mysql_password = 'xx'
mysql_ip = '127.0.0.1'
mysql_db = 'cell_tower'

def checkBudget(towers,budget):
    """ contents is expected as a dictionary of the form {tower_id:(cost,calls), ...} """
    """ This function returns True if the cell tower construction plan is within budget; False otherwise """
    load = 0
    if isinstance(towers,dict):
        for this_key in towers.keys():
            load = load + towers[this_key][0]
        if load <= budget:
            return True
        else:
            return False
    else:
        print("function checkBudget() requires a dictionary")

def compute_added_calls(towers):
    value = 0.0
    if isinstance(towers,dict):
        for this_key in towers.keys():
            value = value + towers[this_key][1]
        return(value)
    else:
        print("function compute_added_calls() requires a dictionary")

def cell_algo(towers,budget):
    """ You write your heuristic cell tower algorithm in this function using the argument values that are passed
             towers: a dictionary of the possible cell towers
             budget: budget for adding cell towers, whcih total cost cannot exceed
    
        Your algorithm must return two values as indicated in the return statement:
            my_username: you WM username
            towers_to_pick: list containing keys (integers) of the towers you want to construct
                            The integers refer to keys in the towers dictionary. 
   """
        
    my_user_name = "no_name"   # replace string with your username
    my_nickname = 'nickname'   # if you chose, enter a nickname to appear instead of your username
    towers_to_pick = []        # use this list for the indices of the towers you select
    investment = 0.0           # use this variable, if you wish, to keep track of how much of the budget is already used
    tot_calls_added = 0.0      # use this variable, if you wish, to accumulate total calls added given towers that are selected
        
    ''' Start your code below this comment '''
    
    
    ''' Finish coding before this comment '''
    
    return my_user_name, towers_to_pick, my_nickname    

def getDBDataList():
    cnx = db_connect()
    cursor = cnx.cursor()
    #cursor.execute(commandString)
    cursor.callproc('spGetProblemIds')
    items = []
    for result in cursor.stored_results(): #list(cursor):
        for item in result.fetchall():
            items.append(item[0])
        break
    cursor.close()
    cnx.close()
    return items
   
""" db_get_data connects with the database and returns a dictionary with the problem data """
def db_get_data(problem_id):
    cnx = db_connect()
                        
    cursor = cnx.cursor()
    cursor.callproc("spGetBudget", args=[problem_id])
    for result in cursor.stored_results():
        knap_cap = result.fetchall()[0][0]
        break
    cursor.close()
    cnx.close()
    cnx = db_connect()
    cursor = cnx.cursor()
    cursor.callproc('spGetData',args=[problem_id])
    items = {}
    for result in cursor.stored_results():
        blank = result.fetchall()
        break
    for row in blank:
        items[row[0]] = (row[1],row[2])
    cursor.close()
    cnx.close()
    return knap_cap, items
    
def db_connect():
    cnx = mySQL.connect(user=mysql_user_name, passwd=mysql_password,
                        host=mysql_ip, db=mysql_db)
    return cnx
    
""" Error Messages """
error_bad_list_key = """ 
A list was received from cell_algo() for the cell numbers to be constructed.  However, that list contained an element that was not a key in the dictionary of the towers that were not yet selected.   This could be either because the element was non-numeric, it was a key that was already selected, or it was a numeric value that didn't match with any of the dictionary keys. Please check the list that your cell_algo function is returning. 
"""
error_response_not_list = """
cell_algo() returned a response for towers to be built that was not a list of possible locations.  Scoring will be terminated   """

""" Get solutions bassed on sbmission """
problems = getDBDataList() 
silent_mode = False    # use this variable to turn on/off appropriate messaging depending on student or instructor use

print('Cell Tower Problems to Solve:',problems)
for problem_id in problems:
    towers_selected = {}
    budget, towers = db_get_data(problem_id)
    #finished = False
    errors = False
    response = None
    
    #print('function')
    team_num, response, nicname = cell_algo(towers,budget)
    if isinstance(response,list):
        for this_key in response:
            if this_key in towers.keys():
                towers_selected[this_key] = towers[this_key]
                del towers[this_key]
            else:
                errors = True
                if silent_mode:
                    status = "bad_list_key"
                else:
                    print("P"+str(problem_id)+"bad_key_")
                #finished = True
    else:
        if silent_mode:
            status = "P"+str(problem_id)+"_not_list_"
        else:
            print(error_response_not_list)
                
    if errors == False:
        if silent_mode:
            status = "P"+str(problem_id)+"budget"
        else:
            print("Cell Tower Problem ", str(problem_id)," ....")
        budget_ok = checkBudget(towers_selected,budget)
        towers_result = compute_added_calls(towers_selected)
        if silent_mode:
            print(status+"; cell towers added within capacity: "+ budget_ok)
        else:
            print('Is Solution Feasible?: ', budget_ok, '   Total Calls Added : ', towers_result)