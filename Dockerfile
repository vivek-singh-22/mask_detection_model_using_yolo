FROM tensorflow/tensorflow:2.13.0

WORKDIR /Mask_detection

COPY . .

# Install missing packages (streamlit, opencv, etc.)
RUN pip install --no-cache-dir -r requirements_d.txt

EXPOSE 8501

CMD ["streamlit", "run", "app.py"]
