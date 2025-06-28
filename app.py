import streamlit as st
from ultralytics import YOLO
from PIL import Image

st.title("Mask Detection with YOLOv8")
model = YOLO(r"C:\CDAC\DNN_programs_Assignments\Mask_detection\runs\detect\train\weights\best.pt")  # Drop best.pt in same folder or specify path

uploaded = st.file_uploader("Upload an image", type=["jpg", "png"])
if uploaded:
    img = Image.open(uploaded).convert("RGB")
    results = model.predict(source=img, imgsz=640, conf=0.25, verbose=False)[0]
    annotated = results.plot()
    st.image(annotated, caption="Detected Masks", use_column_width=True)
    st.write("### Detections:")
    for *box, conf, cls in results.boxes.data.tolist():
        x1,y1,x2,y2 = map(int, box)
        cls_name = model.names[int(cls)]
        st.write(f"{cls_name}: {conf:.2f} at [{x1},{y1},{x2},{y2}]")
