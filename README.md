# Zorgtechnologie-applicatie
## Inleiding

Dit project omvat de ontwikkeling van een zorgtechnologie-applicatie voor Oneplanet. Het doel van de applicatie is om zorgprofessionals te ondersteunen bij het selecteren en toepassen van geschikte zorgtechnologieën. Dit README-bestand biedt een overzicht van het project, de installatie-instructies en enkele belangrijke informatie.
Projectstructuur

    project_oneplant_zorgtechnologie_app/zorgtechnologieapp/

### Flutter en Dart code:

    lib/handlers: Deze map bevat de code voor het verwerken van verschillende gebeurtenissen in de app.

    lib/models: Hier worden de modellen gedefinieerd die worden gebruikt in de app.

    lib/pages: Deze map bevat de verschillende schermen en pagina's van de app.

    lib/widgets: Hier vind je herbruikbare widgets die in de app worden gebruikt.

    lib/main.dart: Dit is het hoofdbestand van de Flutter-applicatie. Het initialiseert de app en bevat de hoofdstructuur van de UI.

### Python code:

    python/database: In deze map bevinden zich alle bestanden en code die verband houden met de databasefunctionaliteit van de backend.

    python/etl_pipeline: Hier vind je de integratie- en dataprocessingspipeline. Dit deel van de code is verantwoordelijk voor het verwerken van de gegevens.

    python/models: Deze map bevat de modellen die worden gebruikt in het Python-gedeelte van de code. Ze definiëren de structuur en het gedrag van de gegevensobjecten.

    python/api_initialtion.py: Dit bestand is verantwoordelijk voor het opzetten van de API. Hier worden de benodigde configuraties en verbindingen geïnitialiseerd.

    python/database_api.py: Dit bestand fungeert als de API die de verbinding tussen de database en de Flutter-applicatie mogelijk maakt. Het biedt methoden en functionaliteit voor het ophalen en bijwerken van gegevens.


## Installatie

    Zorg ervoor dat Python 3.x op je systeem is geïnstalleerd.
    Zorg ervoor dat flutter 3.7 geinstaleerd is. 
    Installeer docker op je syteem
    Installeer de database: `docker run -e NEO4J_AUTH="neo4j/iVOG0qvVg9iYYGz6WVf8BW19Xv4zmmHbDIkH0ur9PCU" --publish=7474:7474 --publish=7687:7687 --volume=$HOME/neo4j/data:/data neo4j`

    Clone de repository naar je lokale machine.
    Navigeer naar de projectmap: cd zorgtechnologie-applicatie.
    Installeer de vereiste afhankelijkheden van python met pip: pip install flask-restx flask neo4j pandas loguru
    Navigeer naar de flutter deel van de applicatie: cd project_oneplant_zorgtechnologie_app/zorgtechnologieapp/
    Installeer de vereiste van flutter met pub: pub get
    run python programma vanuit de repo root om database te vullen: `python python/database/cvs_to_database.py`

## Gebruik

    navigeer naar: cd project_oneplant_zorgtechnologie_app/python
    Start api server: python database_api.py
    (Nieuwe terminal) navigeer naar: project_oneplant_zorgtechnologie_app/zorgtechnologieapp/lib/
    Start applicatie: flutter run
    select device

## Beschikbare aparaten

### Beschikbare schermen:
    
    Ipad
    Android tablet

### coming soon: 

    Android telefoon
    Iphone
    Computer
    

De lijst met ondersteunde apparaten kan in de toekomst worden uitgebreid met nieuwe functionaliteiten en integraties.
