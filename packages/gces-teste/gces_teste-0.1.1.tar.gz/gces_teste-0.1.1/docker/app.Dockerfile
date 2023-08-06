FROM python:3.9

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

ENV PYTHONPATH "${PYTHON}:."

CMD ["python", "src/main.py"]