# 📘 Danger Categories Labeling Tool

## 📝 Overview
The **Danger Categories Labeling Tool** provides a curated list of **30 predefined danger classes**. By uploading an Excel file (`.xlsx` or `.csv`), users can quickly view descriptions, metadata, and other reference information for each danger category.

This tool is designed to **simplify and accelerate data labeling**, ensuring consistent, high-quality annotations for **training machine learning models**.

Link to the tool: [Danger Labeling Streamlit](https://dangerlabeling.streamlit.app/)

---

## 🚀 Features
- **30 predefined danger categories** with clear descriptions and metadata  
- **Excel file upload support** (`.xlsx` and `.csv`)  
- **User-friendly interface** for fast browsing and labeling  
- **Standardized outputs** suitable for ML datasets  
- **Speeds up annotation and reduces human error**

---

## 📂 How It Works
1. Prepare your dataset as an Excel file (`.xlsx` or `.csv`).  
2. Upload the file through the interface.  
3. The tool automatically displays metadata, descriptions, and danger category definitions.  
4. Use the provided information to label your data quickly and accurately.  
5. Export or integrate the labeled data into your ML training pipeline.

---

## 📁 Input Format
Your uploaded file should contain:
- **Text or items to classify**
- Optional metadata
- One row per data instance

**Example (`.csv`):**

```csv
Record No., Description
00001,"Chemical spill detected near storage area."
00002,"Unauthorized access attempt at server room."
```

--- 

## 🗂️ Danger Categories

The tool includes 30 predefined danger categories, such as:

- Facteurs humains

- Chutes de plain pieds

- Incendie/Explosion

- Vibrations

- Rayonnments

(…and more — all included inside the tool.)

--- 

## 📊 Example Workflow

1. Prepare dataset

2. Upload to tool

3. Label using built-in danger descriptions

4. Export dataset

5. Train ML model

6. Iterate as needed
