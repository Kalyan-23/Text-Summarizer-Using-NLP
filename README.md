⚡ Text Summarizer Using NLP

A powerful **Natural Language Processing (NLP)** application that generates concise summaries from long text using multiple extractive summarization techniques — built with **pure Python and Streamlit**.

---

## 🚀 Project Overview

This project implements an **intelligent text summarization system** capable of reducing lengthy articles into meaningful summaries while preserving key information.

It supports multiple NLP algorithms such as:

* Frequency-Based Summarization
* TF-IDF
* TextRank
* LexRank

Additionally, it provides advanced features like:

* 📌 Top Keywords Extraction
* 😊 Sentiment Analysis
* 🧠 Named Entity Recognition (NER)
* ⏱ Reading Time Estimation

---

## 🧠 Features

* 🔹 Multi-algorithm summarization (Frequency, TF-IDF, TextRank, LexRank)
* 🔹 Interactive UI using Streamlit
* 🔹 Dataset explorer for real-world news data
* 🔹 Keyword extraction using TF-IDF
* 🔹 Sentiment analysis (positive / negative / neutral)
* 🔹 Named entity detection (Person, Organization, Location)
* 🔹 Reading time comparison (original vs summary)
* 🔹 Algorithm comparison dashboard

---

## 📂 Project Structure

```
├── app.py                 # Main Streamlit application
├── requirements.txt       # Required libraries
├── dataset/
│   └── news_summary.csv   # Dataset file
└── README.md
```

---

## 📊 Dataset

This project uses a **news summarization dataset**.

### 🔗 Dataset Link

* Kaggle Dataset: https://www.kaggle.com/datasets/sunnysai12345/news-summary

### 📁 Your Dataset File

* Included dataset: 

The dataset typically contains:

* `article` / `ctext` → Full news article
* `highlights` / `text` → Summary

---

## ⚙️ Installation

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/your-username/text-summarizer-nlp.git
cd text-summarizer-nlp
```

### 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Run the Application

```bash
streamlit run app.py
```

---

## 📦 Requirements

Your project uses the following libraries:

```
streamlit
pandas
numpy
nltk
scikit-learn
```

(From your file: )

---

## 🧪 Algorithms Used

| Algorithm | Description                                |
| --------- | ------------------------------------------ |
| Frequency | Scores sentences based on word frequency   |
| TF-IDF    | Highlights important words across document |
| TextRank  | Graph-based ranking (like PageRank)        |
| LexRank   | Probabilistic graph-based summarization    |

---

## 📸 Screenshots

<img width="1911" height="915" alt="Screenshot 2026-04-16 225006" src="https://github.com/user-attachments/assets/76e29b31-56cc-4e8e-a566-2af97100fc54" />
<img width="1919" height="907" alt="Screenshot 2026-04-16 225033" src="https://github.com/user-attachments/assets/c72d59c8-c00d-487c-9e7a-43d3487c1543" />
<img width="1364" height="885" alt="Screenshot 2026-04-16 225116" src="https://github.com/user-attachments/assets/9eaf6170-6dda-46a1-821e-451d7d728335" />

---

## 💡 Use Cases

* News summarization
* Academic content summarization
* Blog/article compression
* Content analysis tools

---

## 🔮 Future Improvements

* 🔹 Add abstractive summarization (Transformers / BERT)
* 🔹 Improve NER using spaCy
* 🔹 Deploy on cloud (Streamlit Cloud / AWS)
* 🔹 Add multilingual support













