
import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score

# 1. Membaca dataset Bahasa Indonesia
data = pd.read_csv("data/train.csv")

# 2. Mengambil kolom yang dibutuhkan
data = data[["text", "label"]].dropna()

data["text"] = data["text"].astype(str).str.strip()
data = data[data["text"] != ""]

# Label 0 = manusia, label 1 = AI
data["label"] = data["label"].astype(int)
data["label"] = data["label"].map({
    0: "human",
    1: "ai"
})

data = data.dropna(subset=["label"])

print("Jumlah data:", len(data))
print("\nJumlah setiap label:")
print(data["label"].value_counts())

# 3. Membagi data untuk latihan dan pengujian
X_train, X_test, y_train, y_test = train_test_split(
    data["text"],
    data["label"],
    test_size=0.20,
    random_state=42,
    stratify=data["label"]
)

print("\nData latihan:", len(X_train))
print("Data pengujian:", len(X_test))

# 4. Membuat model
model = Pipeline([
    ("tfidf", TfidfVectorizer(
        ngram_range=(1, 2),
        sublinear_tf=True
    )),
    ("classifier", LogisticRegression(max_iter=1000))
])

# 5. Melatih model
print("\nSedang melatih model Detectra...")
model.fit(X_train, y_train)

# 6. Menguji model
predictions = model.predict(X_test)

print("\nAkurasi pengujian:",
      round(accuracy_score(y_test, predictions) * 100, 2), "%")

print("\nLaporan evaluasi:")
print(classification_report(
    y_test,
    predictions,
    labels=["human", "ai"],
    target_names=["Manusia", "AI"],
    zero_division=0
))

# 7. Menyimpan model
joblib.dump(model, "text_model.pkl")

print("\nModel baru berhasil disimpan sebagai text_model.pkl")
