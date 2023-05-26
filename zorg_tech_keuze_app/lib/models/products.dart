class Product {
  int? productID;
  String productNaam;
  double? prijs;
  String beschrijving;
  String? categorie;
  String? link;
  int? leverancierID;

  Product(
      {this.productID,
      required this.productNaam,
      this.prijs,
      required this.beschrijving,
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
    data['product'] = {
      'beschrijving': beschrijving,
      'categorie': categorie,
      'productID': productID,
      'leverancierID': leverancierID,
      'link': link,
      'productNaam': productNaam,
      'prijs': prijs,
    };
    return data;
  }
}
