def add(nums, target):
    seen = {}
    i = 0
    while i < len(nums):
        num = nums[i]
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
        i = i + 1
    return []


print(add([2, 7, 11, 15], 9))
print(add([3, 2, 4], 6))
print(add([3, 3], 6))
