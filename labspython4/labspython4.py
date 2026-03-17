import io, sys
def printi(f):
    def wrap(*args, **kwargs):
        sys.stdout = io.StringIO()
        result = f(*args, **kwargs)
        sys.stdout = sys.__stdout__
        return result
    return wrap
# @printi
def hero():
    hp = 100
    def heal(n):
        nonlocal hp 
        hp = min(100, hp + n )
    def damage(n):
        nonlocal hp
        hp = max(0, hp - n)
    def get_hp():
        return hp
    print(hp)
    return get_hp, heal, damage
get_hp, heal, damage = hero()
damage(30)  
heal(20)     
damage(80)  
print(get_hp())  