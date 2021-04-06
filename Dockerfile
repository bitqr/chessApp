FROM python:3

RUN pip install tensorflow

CMD [ "python", "./engine/train_model.py" ]
