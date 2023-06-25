import pandas as pd

# Stap 1: Lees de dataset in
dataset = pd.read_csv('/Users/juliannobbe/Projects/flutter projects/project_oneplanet_zorgtechnologie_app/mockdata/Producten v2.csv')  # Vervang 'jouw_dataset.csv' met de daadwerkelijke bestandsnaam

# Step 2: Delete the 'categorie' column
dataset = dataset.drop('categorie', axis=1)

# Step 3: Save the modified dataset
dataset.to_csv('Producten v2.csv', index=False)  # Replace 'dataset_without_categorie.csv' with the desired file name


# Stap 2: Maak een nieuwe dataset 'toepassing'
# toepassing_dataset = pd.DataFrame(columns=['toepassingID','toepassing','productID'])

# # Stap 3 en 4: Itereer over de producten en voeg de categorieën toe aan de 'toepassing' dataset
# for index, row in dataset.iterrows():
#     product = row['productID']
#     categorie = row['categorie']
#     # toepassing_dataset = toepassing_dataset.({'toepassingID': index, 'toepassing': categorie,'productID': product}),
#     toepassing_dataset = pd.concat([toepassing_dataset, pd.DataFrame([[index+1, categorie, product]], columns=['toepassingID', 'toepassing', 'productID'])])

# # Stap 5: Sla de resulterende dataset op
# toepassing_dataset.to_csv('toepassing_dataset.csv', index=False)  # Vervang 'toepassing_dataset.csv' met de gewenste bestandsnaam
