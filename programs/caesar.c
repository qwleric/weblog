#include <stdio.h>
#include <stdlib.h>

void caesar(const char* msg, int shift)
{
	char c;
	while((c = *msg++))
	{
		char start;
		if(c >= 65 && c <= 90) start = 'A';
		else if(c >= 97 && c <= 122) start = 'a';
		else start = '\0';

		if(start)
			c = start + (c - start + shift) % 26;
		printf("%c", c);
	}
	printf("\n");
}

int main(int argc, char **argv)
{
	if(argc < 2 || argc > 3)
	{
		printf("Usage: %s message shift\n", argv[0]);
		return 1;
	}

	int shift = 1; /* default shift range */
	if(argc == 3) shift = atoi(argv[2]);
	caesar(argv[1], shift);
	return 0;
}
