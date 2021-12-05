import random
from algorithm import Algorithm

tries = 0
# If you are going to propose an algorithm, you can use:
my_algorithm = Algorithm.strategy()
target_number = ''

def function_for_initializing_target_number():
    test = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    a = random.sample(test, 4)
    num = ''

    for i in a:
        num += str(i)

    return num


def function_for_checking_answer(answer):
    availability = True
    if len(answer) != 4:
        # print("4자리 숫자가 아닙니다.")
        availability = False
    for i in range(3):
        for j in range(i + 1, len(player_answer)):
            if player_answer[i] == player_answer[j]:
                # print("중복되는 숫자가 있습니다.")
                availability = False
    return availability


def function_for_scoring(answer):
    strike = 0
    ball = 0

    while True:
        for i in range(4):
            if target_number[i] == answer[i]:
                strike += 1
            elif target_number[i] in answer and target_number[i] != answer[i]:
                ball += 1
        else:
            break

    return '{}S{}B'.format(strike, ball)


if __name__ == '__main__':
    # random.seed(10)
    target_number = function_for_initializing_target_number()
    print('컴퓨터가 숫자를 정했습니다.')
    # print('숫자를 맞출 차례입니다. 숫자를 입력해주세요.')
    print('숫자를 맞출 차례입니다.')
    while True:
        tries += 1
        player_answer = ''
        # player_answer = input("네자리 숫자를 입력해주세요: ")       # 일반 버전 input
        player_answer = my_algorithm.give_an_answer()          # 알고리즘 버전
        # you can assign 'player_answer' as follows:
        #               = input('네자리 숫자를 입력해주세요')
        #               = my_algorithm.give_an_answer()
        # e.g., player_answer variable can be '0123', '2034, or '9802 ans so on.

        if tries >= 1:
            while function_for_checking_answer(player_answer) == False:
                if len(player_answer) != 4:
                    print("4자리 숫자가 아닙니다.")
                for i in range(3):
                    for j in range(i+1, len(player_answer)):
                        if player_answer[i] == player_answer[j]:
                            print("중복되는 숫자가 있습니다.")
                # player_answer = str(input("다시 네자리 숫자를 입력해주세요: "))
                player_answer = my_algorithm.give_an_answer()

            # do something
            # if there is an error, ask for another answer.
            # player_answer = ''

        if target_number != player_answer:
            message = function_for_scoring(player_answer) # e.g., message variable can be 'OUT', '4B', '4S', or '1S2B'
            # If you are going to propose an algorithm, you can use:
            my_algorithm.tries = tries      # 알고리즘 버전
            my_algorithm.record[player_answer] = message        # 알고리즘 버전
            print(message)
        else:
            print("축하합니다! 정답을 {}번의 시도만에 맞추셨습니다".format(tries))
            break