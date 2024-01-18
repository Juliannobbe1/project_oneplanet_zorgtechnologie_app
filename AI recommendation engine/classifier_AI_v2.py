from surprise import Dataset, Reader, KNNBasic, accuracy
from surprise.model_selection import train_test_split
import pandas as pd

# Lees de dataset
data = pd.read_csv('AI recommendation engine/ExploritoryData.csv')

# Creëer een Surprise Reader-object
reader = Reader(rating_scale=(1, 5))

# Laad de dataset in Surprise formaat
dataset = Dataset.load_from_df(data[['naam', 'probleem', 'rating']], reader)

# Kies een Collaborative Filtering algoritme
sim_options = {'name': 'cosine', 'user_based': False}
algo = KNNBasic(sim_options=sim_options)

# Split de dataset in trainings- en testsets
trainset, testset = train_test_split(dataset, test_size=0.2)

# Train het model op de trainingsset
algo.fit(trainset)

# Maak voorspellingen op de testset
predictions = algo.test(testset)

# Bereken en print evaluatiemetrics
rmse = accuracy.rmse(predictions)
mae = accuracy.mae(predictions)

# Geef een probleem op waarvoor aanbevelingen gegeven moeten worden
gebruiker_probleem = "Veiligheid en toezicht"

# Vind gebruikers die vergelijkbare problemen hebben
gebruiker_probleem_ratings = data[data['probleem'] == gebruiker_probleem]
gebruiker_ids = gebruiker_probleem_ratings['naam'].tolist()

# Maak aanbevelingen voor de gebruiker op basis van vergelijkbare problemen
aanbevelingen = {}
for gebruiker_id in gebruiker_ids:
    pred = algo.predict(gebruiker_id, gebruiker_probleem)
    aanbevelingen[gebruiker_id] = pred.est

# Identificeer de gebruiker met de hoogste aanbeveling
hoogste_gebruiker = max(aanbevelingen, key=aanbevelingen.get)
hoogste_score = aanbevelingen[hoogste_gebruiker]

print(f"product met hoogste aanbeveling: {hoogste_gebruiker}, Score: {hoogste_score}")
