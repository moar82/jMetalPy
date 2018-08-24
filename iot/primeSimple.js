//RMA count primes below 100,000  .
function isPrime(num) {
  for(var i = 2; i < num; i++)
    if(num % i === 0) return false;
  return num !== 1;
}

function forTest() {
	count =0
    for (var i = 1; i < 10000; i++) {
      if (isPrime(i) && (i % 10000) == 9999) {
	         count++; 
	     }

	} 
	//print (count);
}
//forTest();