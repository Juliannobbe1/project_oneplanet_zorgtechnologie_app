import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Gegevens inlezen
data = pd.read_csv('mockdata/Producten v2.csv')

# Toon de eerste paar rijen van de dataset
print("Eerste 5 rijen van de dataset:")
print(data.head())

# Bekijk de algemene informatie over de dataset
print("\nAlgemene informatie over de dataset:")
print(data.info())

# Statistische samenvatting van numerieke kolommen
print("\nStatistische samenvatting van numerieke kolommen:")
print(data.describe())

# Unieke waarden in de 'categorie' kolom
print("\nUnieke waarden in de 'categorie' kolom:")
print(data['categorie'].unique())

# Aantal producten per categorie
print("\nAantal producten per categorie:")
print(data['categorie'].value_counts())

# Gemiddelde prijs van producten
gemiddelde_prijs = data['prijs'].mean()
print(f"\nGemiddelde prijs van producten: {gemiddelde_prijs:.2f} Euro")

# Aantal unieke leveranciers
aantal_leveranciers = data['leverancierID'].nunique()
print(f"\nAantal unieke leveranciers: {aantal_leveranciers}")

# Bekijk enkele voorbeelden van beschrijvingen
print("\nVoorbeelden van productbeschrijvingen:")
print(data['beschrijving'].sample(5))

# Palet voor kleuren
color_palette = 'viridis'

# Countplot van categorieën
plt.figure(figsize=(12, 6))
sns.countplot(x='categorie', data=data, palette=color_palette)
plt.title('Aantal producten per categorie')
plt.xlabel('Categorie')
plt.ylabel('Aantal producten')
plt.xticks(rotation=45)
plt.show()


# Line plot van verkopen per maand
data['datum'] = pd.to_datetime(data['datum'])
data['maand'] = data['datum'].dt.month
monthly_sales = data.groupby('maand')['verkocht'].sum().reset_index()
plt.figure(figsize=(10, 6))
sns.lineplot(x='maand', y='verkocht', data=monthly_sales, marker='o', color='orange')
plt.title('Verkopen per maand')
plt.xlabel('Maand')
plt.ylabel('Aantal verkochte producten')
plt.show()

# Swarm plot van beoordelingen per categorie
plt.figure(figsize=(12, 8))
sns.swarmplot(x='categorie', y='beoordeling', data=data, palette='Set2')
plt.title('Beoordelingen per categorie')
plt.xlabel('Categorie')
plt.ylabel('Beoordeling')
plt.xticks(rotation=45)
plt.show()

# Pairplot van numerieke variabelen
sns.pairplot(data[['prijs', 'voorraad', 'verkocht', 'beoordeling']], height=2.5)
plt.suptitle('Pairplot van numerieke variabelen', y=1.02)
plt.show()

