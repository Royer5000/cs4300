
num = 0
if num > 0:
    print("num is greater than 0")
elif num < 0:
    print("num is less than 0")
elif num == 0:
    print("num is equal to  0")

isPrime = True
prime_num_iter = 2
prime_nums = []
for i in range(10):
    while len(prime_nums) <= i:
        for j in range(len(prime_nums)):
            if prime_num_iter % prime_nums[j] == 0:
                isPrime = False

        if isPrime:
            print(prime_num_iter)
            prime_nums.append(prime_num_iter)
        prime_num_iter += 1
        isPrime = True


count = 1
sum = 0
while count <= 100:
    sum += count
    count += 1

print("The sum of all numbers from 1 to 100 is: " + str(sum))
