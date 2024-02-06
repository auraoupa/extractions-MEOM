#! /usr/bin/env python
import sys

def check(item, list_items, message):
    """
    Check if the given item is in the list. If not, exit the script with the provided error message.

    Parameters:
    - item: The item to check in the list.
    - list_items: The list to check for the item.
    - message: The error message to display if the item is not in the list.

    Returns:
    None
    """
    if item not in list_items:
        sys.exit(message)

def concatenate_all_names_in_list(listnames):
    """
    Concatenate names in the given list into a single string separated by '-'.

    Parameters:
    - listnames: A list of names to concatenate.

    Returns:
    str: The concatenated string of names.
    """
    if len(listnames)==1:
        allnames=listnames[0]
    elif len(listnames)==2:
        allnames=listnames[0]+'-'+listnames[1]
    elif len(listnames)>2:
        allnames=''
        lv=len(listnames)
        ll=0
        for var in listnames:
            ll+=1
            allnames=allnames+var
            if ll < lv:
                allnames=allnames+'-'
    return allnames
