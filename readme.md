# Receipt Processor API  

A FastAPI service that processes receipts and calculates points based on specific rules.



## Instructions to build and run the application

Step 1:
  Clone the Repository
  
    git clone https://github.com/sky2134/receipt-processor.git

  Step 2:
  Navigate to project directory
  
    cd receipt-processor

Step 3:
 Building and Running with Docker

Build the Docker image:

    docker build -t receipt-processor .

Run the container:

    docker run -p 8000:8000 receipt-processor

Step 4:
API Documentation

1. Open your browser and navigate to http://localhost:8000
2. You'll see the API documentation with two endpoints:

       POST /receipts/process
       GET /receipts/{id}/points

Step 5:

1. Click on POST /receipts/process endpoint
2. Click the "Try it out" button
3. In the Request body, paste your receipt JSON
4. Click "Execute"
5. You'll receive a response with an ID
6. IMPORTANT: Copy this ID for the next step!


Step 6:

1. Click on GET /receipts/{id}/points endpoint
2. Click the "Try it out" button
3. Paste the ID you received from step 5 into the 'id' field
4. Click "Execute"
5. You'll see the points calculated for your receipt
