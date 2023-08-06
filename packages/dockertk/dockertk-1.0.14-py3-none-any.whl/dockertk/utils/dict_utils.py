def __safe_merge(__lhs:dict,__rhs:dict):
    result = __lhs.copy()
    for key,value in __rhs.items():
        if key in __lhs:
            lvalue = __lhs.get(key)
            if lvalue != value:
                raise Exception(f"ERROR: CONFLICT OF DICT KEYS:: {str(key)} : {lvalue} : {value}")
        result[key] = value
    return result


def safe_merge(__lhs:dict,__rhs:dict):
    return __safe_merge(__lhs,__rhs)
