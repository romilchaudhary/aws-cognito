a = 10
b = 2

def add(x, y):
	return x+y

def max(x, y):
	if x > y:
		return str(x) + " is greater than " + str(y)
	else:
		return str(y) + " is greater thant " + str(x)

def fact(n):
	if n == 0:
		return 1
	elif n == 1:
		return 1
	else:
		return n * fact(n-1)

def max_array(a):
	max = 0
	for i in a: 
		if i > max:
			max = i
	return f"max is: {max}"

def interchange(a):
	last = a[-1]
	first = a[0]
	a[0] = last
	a[len(a)-1] = first
	return f"interchange : {a}"

def swap(a=[23, 65, 19, 90], pos1=1, pos2=3):
	temp = a[pos1]
	a[pos1] = a[pos2]
	a[pos2] = temp
	return f"swapped array is: {a}"
 	 

if __name__ == '__main__':
	print("adding")
	adding = add(a, b)
	print(adding)
	print(max(a,b))
	print(fact(4))
	print(max_array([11,2,3]))
	print(interchange([12, 35, 9, 56, 24]))
	print(swap(a = [23, 65, 19, 90], pos1 = 1, pos2 = 3))
	a = [1, 2, 2]
	a *= 0
	print(f"clear array is: {a}")
	a = [12, 15, 3, 10]
	print(f"sum is: {sum(a)}")
	summ = 0
	for i in a:
		summ += i
	print(f"summ is: {summ}")

	ll = [1, 2, 3, 4]
	from functools import reduce
	print(f"mul is: {reduce(lambda x,y:x*y, ll)}")

	list1 = [10, 20, 1, 4]
	print(f"min is: {min(list1)}")

	minn = list1[0]
	for i in list1:
		if i<minn:
			minn = i
		else:
			minn = minn
	print(f"minn is: {minn}")
	list1.sort(reverse=True)
	print(f"max is: {list1[1]}")
