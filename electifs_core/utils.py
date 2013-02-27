def to_int_list (input):
    """
    Tries to convert the input to a list of integers.
    
    If input is None, returns an empty list.
    If input is a list or tuple, tries to convert each item (unless it is None)
    to an integer and return the list of converted items.
    In all other cases, tries to convert input to integer and returns it as a
    single-item list.
    
    Upon failure to convert input or an item of input, a ValueError is raised
    """
    
    try:
        
        if input is None:
            return []
        
        elif (type(input) is list) or (type(input) is tuple):
            result = []
            for i in input:
                if i is not None:
                    result.append(int(i))
            return result
        
        else:
            return [int(input)]
    
    except (TypeError, ValueError): # ValueError or TypeError are legitimate
        raise
    
    except Exception as e:
        # unexpected situation - log something...
        raise

################################################################################


