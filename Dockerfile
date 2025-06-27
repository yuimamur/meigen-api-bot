FROM public.ecr.aws/lambda/python:3.10

# 依存パッケージをインストール
COPY requirements.txt ./
RUN pip3 install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"

# Lambdaのハンドラを追加
COPY app/* ${LAMBDA_TASK_ROOT}/

# ハンドラの名前を指定（ファイル名.関数名）
CMD ["lambda_function.lambda_handler"]
