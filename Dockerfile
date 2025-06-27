FROM public.ecr.aws/lambda/python:3.12

# requestsライブラリをインストール
RUN pip install requests

# Lambda実行用コードをコピー
COPY lambda_function.py .

# Lambdaのエントリポイントを指定
CMD ["lambda_function.lambda_handler"]
