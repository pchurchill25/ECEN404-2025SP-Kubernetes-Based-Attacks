#Use TensorFlow for adding stress
FROM tensorflow/tensorflow:latest-gpu

# Clean up some error messages
ENV TF_CPP_MIN_LOG_LEVEL=3

# Copy the stress test  script into the container
COPY gpu_workload.py /gpu_workload.py

# Run the script
CMD ["python", "/gpu_workload.py"]
