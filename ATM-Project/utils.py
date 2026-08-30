import hashlib 

def hash_pin(raw_pin: str) -> str:
    '''take raw str pin "6578" and covert into raw hash'''
    return hashlib.sha256(str(raw_pin).encode("utf-8")).hexdigest()
