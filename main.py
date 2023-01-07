from generator import Generator

if __name__ == '__main__':
    pseudocode = '''x <- 1;
if (x = 1){
	y<-2;
} else {
	y<-3;
}

my_print(x){
	for i <- 1…x{
		print i;
	}
	return true;
}

my_print(5);

arr <- [1,2,3];
z <- arr[2];
'''
    generator = Generator(pseudocode)
    generator.generate()
