#!/usr/bin/env nu

for i in 1..100000 {
		if (2..($i | math sqrt) | all? $i mod $it != 0) {
				echo $i
		}
} | save primes.txt
