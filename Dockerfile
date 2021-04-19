FROM python:3

RUN apt update && apt install -y graphviz nano

RUN pip install tensorflow pydot pygame clipboard

CMD [ "python", "chessApp/engine/train_model.py" ]
