# Use the AWS Lambda Python 3.12 base image
FROM public.ecr.aws/lambda/python:3.12

# Set working directory
WORKDIR ${LAMBDA_TASK_ROOT}

# Copy app files
COPY . .

RUN pip install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"

# Set the Lambda handler — points to handler = Mangum(app) in main.py
CMD ["main.handler"]