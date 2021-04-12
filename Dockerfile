FROM python:3

RUN apt update && apt install -y graphviz nano

RUN pip install tensorflow pydot

CMD [ "python", "./engine/train_model.py" ]
