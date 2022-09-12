[println "test"]
[println 42]
[println [+ 5 2]]

[set x 22]
[println [get x]]
[println x]

[println [** 5 3]]

[def cube x [** x 3]]

[
	quote
	for-x
	[range 0 10]
	[println x]
]

[def function divisible
	type : [int a] [int b] -> boolean
	info : "Returns true if b evenly divides a (i.e., a % b equals 0) and false otherwise"
	return [not [mod a b]]
]
