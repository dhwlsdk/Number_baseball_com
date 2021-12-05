import random
from itertools import permutations


class strategy():
    def __init__(self):
        #do something
        self.tries = 0
        self.record = {}
        self.current_val = ""
        self.current_res = ""

        self.investigate_mode = False
        self.investigate_candid = []
        self.investigate_res = []
        self.investigate_res_max = 0

        self.additional_mode = False
        self.additional_candid = []
        self.additional_target_strike = 0

        self.pool = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        self.trash_pool = []
        self.answer = [-1, -1, -1, -1]
        self.answer_count = 0

        pass

    def random_gen(self):
        # Use self.answer and random number to generate random number
        print(self.pool)
        candid = random.sample(self.pool, 4)
        res = ""
        cnt = 0
        for i in range(4):
            if self.answer[i] != -1:
                res += str(self.answer[i])
            else:
                while True:
                    if candid[cnt] not in self.answer:
                        res += str(candid[cnt])
                        cnt += 1
                        break
                    else:
                        cnt += 1

        print(f"Random gen, Pool: {self.pool}, Answer: {self.answer}, Res: {res}")
        return res

    def evict_useless(self):
        # Use self.current_val to evict useless number in self.pool
        # evict useless ones
        candid_idx_list = []
        useless_list = [int(self.current_val[0]), int(self.current_val[1]), int(self.current_val[2]),
                        int(self.current_val[3])]
        for idx, i in enumerate(self.pool):
            if i not in useless_list:
                candid_idx_list.append(idx)

        temp_pool = []
        for i in candid_idx_list:
            temp_pool.append(self.pool[i])
        for i in self.answer:
            if i != -1:
                temp_pool.append(i)
        self.pool = temp_pool[:]

        self.trash_pool = []
        for i in range(10):
            if i not in self.pool:
                self.trash_pool.append(i)

        print(f"Updated pool: {self.pool}")

    def investigate_gen(self):
        # Use self.current_val and self.answer to generate self.investigate_candid
        # Use permutation!
        candid_list = []
        for i in self.current_val:
            int_i = int(i)
            if int_i not in self.answer:
                candid_list.append(int_i)

        print(f"Investigate target num: {candid_list}, Answer count: {self.answer_count}")

        candid_permute_list = permutations(candid_list, 4 - self.answer_count)
        self.investigate_candid = []
        for candid in candid_permute_list:
            cnt = 0
            tmp = ""
            for a in self.answer:
                if a == -1:
                    tmp += str(candid[cnt])
                    cnt += 1
                else:
                    tmp += str(a)
            self.investigate_candid.append(tmp)

        print(f"Investigate candid: {self.investigate_candid}")

    def check_answer(self):
        # Compare numbers in self.investigate_res to find out answers!
        print(self.investigate_res)
        if len(self.investigate_res) == 1: # need to compare with trash value
            if self.answer_count == 3:
                first_elem = self.investigate_res[0]
                for idx, i in enumerate(self.answer):
                    if i == -1:
                        self.answer[idx] = int(first_elem[idx])
                        self.answer_count += 1
                        break
                print(f"Updated answer: {self.answer}, Finally End!")
                return True
            else:
                print("Additional check required")
                return False
        else:
            first_elem = self.investigate_res[0]
            answer_idx_in_elem = []
            # 1st elem
            elem = self.investigate_res[1]
            for idx, i in enumerate(elem):
                if int(i) in self.answer:
                    continue
                elif first_elem[idx] == i:
                    answer_idx_in_elem.append(idx)
                else:
                    continue
            # others
            if len(self.investigate_res) > 2:
                for elem in self.investigate_res[2:]:
                    temp_idx = []
                    for idx, i in enumerate(elem):
                        if i in self.answer:
                            continue
                        elif idx in answer_idx_in_elem:
                            if first_elem[idx] == i:
                                temp_idx.append(idx)
                    answer_idx_in_elem = temp_idx

            # fix answers
            for idx in range(4):
                if idx in answer_idx_in_elem:
                    self.answer[idx] = int(first_elem[idx])
                    self.answer_count += 1
                elif int(first_elem[idx]) not in self.trash_pool:
                    self.pool.remove(int(first_elem[idx]))
                    self.trash_pool.append(int(first_elem[idx]))

            print(f"Updated answer: {self.answer}")

            return True

    def additional_candid_gen(self):
        trash_val = self.trash_pool[0]
        first_elem = self.investigate_res[0]
        target_idx = []

        for idx, i in enumerate(first_elem):
            if int(i) not in self.answer:
                target_idx.append(idx)

        self.additional_candid = []
        for idx in target_idx:
            tmp = ""
            for i in range(4):
                if i == idx:
                    tmp += str(trash_val)
                else:
                    tmp += first_elem[i]
            self.additional_candid.append(tmp)

        print(f"Additional candid gen, first_elem: {first_elem}, target_idx: {target_idx}, candid: {self.additional_candid}")

        return

    def additional_answer_fix(self):
        elem = self.current_val
        for idx, i in enumerate(elem):
            if int(i) in self.answer:
                continue
            elif int(i) in self.trash_pool:
                continue
            else:
                self.answer[idx] = int(i)
                self.answer_count += 1

    def give_an_answer(self):

        if self.tries == 0:
            res = self.random_gen()
            self.tries += 1
        elif self.answer_count == 4:
            res = ""
            for i in self.answer:
                res += str(i)
        elif not self.investigate_mode and not self.additional_mode:
            self.current_val, self.current_res = list(self.record.items())[0]
            self.record.pop(self.current_val, None)

            how_many_strike = int(self.current_res[0])
            how_many_ball = int(self.current_res[2])

            print(f"Strike: {how_many_strike}, Ball: {how_many_ball}, Known: {self.answer_count}")

            if how_many_strike + how_many_ball == self.answer_count:
                print("111")
                self.evict_useless()
                res = self.random_gen()
            elif how_many_strike + how_many_ball - self.answer_count == 3:
                print("It's actually very lucky, but ironically, not good for us")
                res = self.random_gen()
            else:
                print("222")
                print("Enter investigate mode")
                self.investigate_mode = True
                self.investigate_candid = []
                self.investigate_res = []
                self.investigate_res_max = 0
                self.investigate_gen()
                res = self.investigate_candid.pop(0)
        elif self.investigate_mode and self.investigate_candid:
            print("Currently, investigate mode")
            print("333")
            self.current_val, self.current_res = list(self.record.items())[0]
            self.record.pop(self.current_val, None)

            current_strike = int(self.current_res[0])
            if current_strike > self.investigate_res_max:
                self.investigate_res_max = current_strike
                self.investigate_res = []
                self.investigate_res.append(self.current_val)
            elif current_strike == self.investigate_res_max:
                self.investigate_res.append(self.current_val)

            res = self.investigate_candid.pop(0)

        elif self.investigate_mode and not self.investigate_candid:
            print("Last investigate mode")
            self.current_val, self.current_res = list(self.record.items())[0]
            self.record.pop(self.current_val, None)

            current_strike = int(self.current_res[0])
            if current_strike > self.investigate_res_max:
                self.investigate_res_max = current_strike
                self.investigate_res = []
                self.investigate_res.append(self.current_val)
            elif current_strike == self.investigate_res_max:
                self.investigate_res.append(self.current_val)

            self.investigate_mode = False
            if self.check_answer(): # Succesfully find answers
                print("444")
                res = self.random_gen()
            else:
                print("555")
                self.additional_candid_gen()
                self.additional_mode = True
                self.additional_target_strike = self.investigate_res_max
                print(f"Target strike: {self.additional_target_strike}")
                res = self.additional_candid.pop(0)
        elif self.additional_mode:
            self.current_val, self.current_res = list(self.record.items())[0]
            self.record.pop(self.current_val, None)

            current_strike = int(self.current_res[0])
            if current_strike == self.additional_target_strike:
                print("666")
                self.additional_answer_fix()
                self.additional_mode = False
                res = self.random_gen()
            elif self.additional_candid:
                print("777")
                res = self.additional_candid.pop(0)
            else:
                print("888")
                res = self.random_gen()

        else:
            print("ERROR, not allowed case")
            exit(1)

        print(f"Return {res}")
        return res




        # pool = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        # answer = '9876'
        # # print(f"Tries: {self.tries}")
        # if self.tries == 0:
        #     answer = '0123'
        # elif self.tries == 1:
        #     answer = '3456'
        # elif self.tries == 2:
        #     answer = '6789'
        # else:
        #     answer = "1234"

        # if '0S0B' in self.record:
        #     for i in answer:
        #         pool.remove(i)
        #         answer = random.sample(pool, 4)

        # if '0S0B' in self.record:
        #     for i in answer:
        #         pool.remove(i)
        #         answer = random.sample(pool, 4)


        # print(self.record)
        # do something
        # print(f"Answer: {answer}, Tries: {self.tries}")
        # return answer