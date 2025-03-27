import tensorflow as tf #need tenserflow to stress CPU/GPU
#import time
import os #trying to use os to clean up the warnings

# clean up some warnings
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

#making a function to put stress on the computer CPU/GPU to simulate a cryptominer running
def gpu_workload():

    #print("Actaully running")
    # increase matrix size to increase load on computer, 6000 gets CPU to ~90-95% 
    matrix_size = 6000  # Adjust size for more/less stress
    a = tf.random.uniform((matrix_size, matrix_size), dtype=tf.float32) #make big matrix
    b = tf.random.uniform((matrix_size, matrix_size), dtype=tf.float32) #make another big matrix

    # More iterations for longer stress test
    iterations = 100 #takes about 26 seconds to run, scales lineraly, eg 100 is 2.6 seconds 
    #start_time = time.time() #was using to check active time
    while True: #runs for each iteration
        tf.linalg.matmul(a, b) # this is multiplying two large matrices to consume CPU/GPU resources
           # print(f"Took {time.time() - start_time:.2f} seconds")

if __name__ == "__main__": #runs the code 
    gpu_workload() #call the function to consume the resources   
