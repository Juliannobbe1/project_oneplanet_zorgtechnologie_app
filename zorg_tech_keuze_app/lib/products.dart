class Product {
  int? productID;
  String? productNaam;
  double? prijs;
  String? beschrijving;
  String? categorie;
  String? link;
  int? leverancierID;

  Product(
      {this.productID,
      this.productNaam,
      this.prijs,
      this.beschrijving,
      this.categorie,
      this.link,
      this.leverancierID});

  factory Product.fromJson(Map<String, dynamic> json) {
    return Product(
        productID: json['productID'],
        productNaam: json['productNaam'],
        prijs: json['prijs'],
        beschrijving: json['beschrijving'],
        categorie: json['categorie'],
        link: json['link'],
        leverancierID: json['leverancierID']);
  }

  Map<String, dynamic> toJson() {
    final Map<String, dynamic> data = <String, dynamic>{};
    data['productID'] = productID;
    data['productNaam'] = productNaam;
    data['prijs'] = prijs;
    data['beschrijving'] = beschrijving;
    data['categorie'] = categorie;
    data['link'] = link;
    data['leverancierID'] = leverancierID;
    return data;
  }
}
