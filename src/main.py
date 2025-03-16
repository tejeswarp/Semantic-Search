import time
import vectorizerhfcustomer

if __name__ == "__main__":
    initial_time = time.time()
    vectorizerhfcustomer.main()
    finish_time = time.time()
    print('Embeddings created & indexed in {:f} seconds\n'.format(finish_time-initial_time))
