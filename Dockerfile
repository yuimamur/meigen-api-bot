FROM public.ecr.aws/lambda/python:3.8

# requestsライブラリをインストール
RUN pip install requests

# アプリケーションファイルをコピー
COPY app.py ${LAMBDA_TASK_ROOT}
