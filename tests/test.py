score=[(100,100),(95,90),(65,20),(60,90),(100,60)]

def password_check(func):
    def wrapper(*args,**kwargs):
        password="1234"
        check = input()
        if password==check:
            result = func(*args, **kwargs)
        else:
            result = "잘못된비번"
        return result
    return wrapper

@password_check
def get_avg(score:list):
    for index,point in enumerate(score):
        print(f'{index+1}번, 평균 : {sum(point)/len(point)}')


print(get_avg(score))

