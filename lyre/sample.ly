def function divisible
	type : [int a] [int b] -> boolean
	info : "Returns true if b evenly divides a (i.e., a % b equals 0) and false otherwise"
	return [not [mod a b]]
