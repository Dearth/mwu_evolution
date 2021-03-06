#include <stdlib.h>
#include <stdio.h>
#include <pthread.h>

pthread_mutex_t sync_mutex;
int count = 0;
int totals[10];

void* increment_count() {
	FILE* fout = NULL;
	fout = fopen("inc_out.txt", "w");
	if(NULL == fout) {
		printf("Error opening inc file\n");
		exit(1);
	}

	for(int i = 0; i < 10; ++i) {
		++count;
		
		if(i > 0) {
			totals[i] = totals[i-1] + count;
		} else {
			totals[0] = count;
		}
	}

	for(int i = 0; i < 10; ++i) {
		if(i > 0) {
			fprintf(fout, "%d %d\n", totals[i], (totals[i] > totals[i-1]));
		} else {
			fprintf(fout, "%d 1\n", totals[i]);
		}
	}

	fclose(fout);

	pthread_mutex_unlock(&sync_mutex);
	pthread_exit(NULL);
}

void* increment_count2() {
	FILE* fout = NULL;
	fout = fopen("inc2_out.txt", "w");
	if(NULL == fout) {
		printf("Error opening inc file\n");
		exit(1);
	}
	
	for(int i = 0; i < 10; ++i) {
		++count;
		
		if(i > 0) {
			totals[i] = totals[i-1] + count;
		} else {
			totals[0] = count;
		}
	}
	
	for(int i = 0; i < 10; ++i) {
		if(i > 0) {
			fprintf(fout, "%d %d\n", totals[i], (totals[i] > totals[i-1]));
		} else {
			fprintf(fout, "%d 1\n", totals[i]);
		}
	}

	fclose(fout);

	pthread_exit(NULL);
}

int main(int argc, char** argv) {
	pthread_t threads[2];
	int err;
	FILE* fout = NULL;

	if(argc < 2) {
		printf("Please supply input\n");
		exit(1);
	}

	count = atoi(argv[1]);

	pthread_mutex_init(&sync_mutex, NULL);

	fout = fopen("output.txt", "w");
	if(NULL == fout) {
		printf("Error opening output file\n");
		exit(1);
	}
	
	pthread_mutex_lock(&sync_mutex);
	err = pthread_create(&threads[0], NULL, &increment_count, NULL);
	if(err) {
		printf("ERROR: return code for pthread_create() is %d\n", err);
		exit(1);
	}
	
	err = pthread_create(&threads[1], NULL, &increment_count2, NULL);
	if(err) {
		printf("ERROR: return code for pthread_create() is %d\n", err);
		exit(1);
	}

	pthread_mutex_lock(&sync_mutex);
	for(int i = 0; i < 10; ++i) {
		printf("%d\n", totals[i]);
		fprintf(fout, "%d\n", totals[i]);
	}
	pthread_mutex_unlock(&sync_mutex);
	
	fclose(fout);

	pthread_exit(NULL);
	return 0;
}
