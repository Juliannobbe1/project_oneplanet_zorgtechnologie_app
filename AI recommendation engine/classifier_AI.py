import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.metrics import f1_score

df = pd.read_csv("AI recommendation engine/ExploritoryData.csv")

# Feature engineering: combineer relevante informatie
df['kenmerken'] = df['naam'] + ' ' + df['categorie'] + ' ' + df['probleem']

# Definieer features en labels
X = df['kenmerken']
y = df['naam']  # Verander dit van 'probleem' naar 'naam'

# Split de data in trainings- en testsets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.35, random_state=42)

# Gebruik TF-IDF Vectorizer om tekst om te zetten naar numerieke waarden
vectorizer = TfidfVectorizer()
X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)

# Bouw een classificatiemodel (Random Forest in dit geval)
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train_tfidf, y_train)

# Voorspel de labels voor de testset
y_pred = model.predict(X_test_tfidf)

# Evaluatie van het model
print("Accuracy:", accuracy_score(y_test, y_pred))
print("\nClassification Report:\n", classification_report(y_test, y_pred))

# Assuming y_test and y_pred are your true labels and predicted labels
f1 = f1_score(y_test, y_pred, average='weighted')  # or 'micro', 'macro', or None
print("F1-score:", f1)

# Vraag om een lijst van beschikbare problemen
beschikbare_problemen = df['probleem'].unique()
print("Beschikbare oplossing:")
for i, probleem in enumerate(beschikbare_problemen, start=1):
    print(f"{i}. {probleem}")

# Laat de gebruiker een probleem kiezen
keuze = int(input("Kies een nummer voor het gewenste probleem: "))
gekozen_probleem = beschikbare_problemen[keuze - 1]

# Vraag om een prijsrange
min_prijs = float(input("Voer de minimum prijs in: "))
max_prijs = float(input("Voer de maximum prijs in: "))

# Geef aanbevelingen op basis van het gekozen probleem en prijsrange
aanbevelingen = model.classes_  # Alle beschikbare producten

# Bereken de gewogen score op basis van prijs en classificatiekans
gewogen_scores = []
for aanbeveling in aanbevelingen:
    product_info = df[df['naam'] == aanbeveling].iloc[0]
    if min_prijs <= product_info['prijs'] <= max_prijs:
        prijs_score = 1 / (1 + product_info['prijs'])  # Hoe lager de prijs, hoe hoger de score
        classificatiekans = model.predict_proba(vectorizer.transform([gekozen_probleem]))[0, model.classes_ == aanbeveling][0]
        gewogen_score = prijs_score * classificatiekans
        gewogen_scores.append((aanbeveling, gewogen_score, product_info['prijs']))

# Sorteer op gewogen score en geef de top N aanbevelingen
top_aanbevelingen = sorted(gewogen_scores, key=lambda x: x[1], reverse=True)[:3]

# Print de top aanbevelingen met prijzen
print(f"\nTop 3 Aanbevelingen voor probleem '{gekozen_probleem}' binnen de opgegeven prijsrange:")
for aanbeveling, score, prijs in top_aanbevelingen:
    print(f"- Product: {aanbeveling}, Prijs: {prijs:.2f} euro")
