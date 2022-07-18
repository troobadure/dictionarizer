def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

def count(lst, n):
    """Return number of n-sized chunks in a lst"""
    return (len(lst) - 1) // n + 1