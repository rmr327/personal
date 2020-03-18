class Solution:
    @ staticmethod
    def two_sum(nums, target):
        ind = dict()
        for i, num in enumerate(nums):
            tar = target - nums[i]
            if tar not in ind:
                ind[num] = i
            else:
                return [ind[tar], i]

    @staticmethod
    def add_two_numbers(self, l1, l2):
        res = 0
        count = 0
        forward = l1
        forward_1 = l2

        while forward or forward_1:
            try:
                val = forward.val
                forward = forward.next
                res += val * 10 ** count
            except  AttributeError:
                pass

            try:
                val = forward_1.val
                forward_1 = forward_1.next
                res += val * 10 ** count
            except AttributeError:
                pass

            count += 1

        res = str(res)[::-1]
        res_list = [ListNode(int(res[0]))]
        count = 0

        for element in res[1:]:
            node = ListNode(int(element))
            res_list[count].next = node
            res_list.append(node)
            count += 1

        return res_list[0]


class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None


if __name__ == '__main__':
    import numpy as np
    np.linalg.inv()

    c = Solution()
    print(c.two_sum([1, 3, 5, 7, 9], 10))

    list_1 = ListNode

    print(c.add_two_numbers())
