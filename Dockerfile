FROM public.ecr.aws/lambda/python:3.8

# requestsをインストール
RUN pip install requests

COPY app.py ${LAMBDA_TASK_ROOT}

CMD [ "app.lambda_handler" ]

