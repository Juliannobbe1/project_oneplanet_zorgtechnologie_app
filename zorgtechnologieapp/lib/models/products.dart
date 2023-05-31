class Product {
  int iD;
  String naam;
  double? prijs;
  String beschrijving;
  String? link;
  int? leverancierID;

  Product(
      {required this.iD,
      required this.naam,
      this.prijs,
      required this.beschrijving,
      this.link,
      this.leverancierID});

  factory Product.fromJson(Map<String, dynamic> json) {
    return Product(
        iD: json['ID'],
        naam: json['naam'],
        prijs: json['prijs'],
        beschrijving: json['beschrijving'],
        link: json['link'],
        leverancierID: json['leverancierID']);
  }

  Map<String, dynamic> toJson() {
    final Map<String, dynamic> data = <String, dynamic>{};
    data['product'] = {
      'beschrijving': beschrijving,
      'ID': iD,
      'leverancierID': leverancierID,
      'link': link,
      'naam': naam,
      'prijs': prijs,
    };
    return data;
  }
}
