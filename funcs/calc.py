def calc_simple(w=int, h=int):
    result = [w+24, h+45]
    return result

def calc_skf(w=int, h=int):
    result = [w-45, h-47]
    return result

def calc_hooks(w=int, h=int):
    result = [w+40, h+30]
    return result

def calc_net(width=int, height=int, net_type=str):

    if net_type == 'skf':      return calc_skf(width, height)
    elif net_type == 'simple': return calc_simple(width, height)
    elif net_type == 'hooks':  return calc_hooks(width, height)
    else: 
        print(f"Incorrect type - {net_type}")
        return None
    
    
def net_storage():
    """function for holding net sizes

    Returns:
        add: func
        store: list
    """
    store=[]

    def add(new_size):
        # nonlocal store

        store.append(new_size)
        # print(f"store: {store}")
        return store
    def get_store():
        for s in store:
            print(f"store item: {s}")
        return  store

    return add, get_store




