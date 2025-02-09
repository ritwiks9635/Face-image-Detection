# Use an official Python runtime as a parent image  
FROM python:3.9  

# Set the working directory  
WORKDIR /app  

# Copy the requirements file and install dependencies  
COPY requirements.txt /app/  
RUN pip install --no-cache-dir -r requirements.txt  

# Copy the entire project  
COPY . /app/  

# Expose port for Gradio or Streamlit  
EXPOSE 7860  

# Run the application  
CMD ["python", "frontend/app.py"]
