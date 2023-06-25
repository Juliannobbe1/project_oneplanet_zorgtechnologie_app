class Product {
  String iD;
  String naam;
  double? prijs;
  String beschrijving;
  String? link;
  int? leverancierID;
  String? imageBase64;

  Product(
      {required this.iD,
      required this.naam,
      this.prijs,
      required this.beschrijving,
      this.link,
      this.leverancierID,
      this.imageBase64});

  // @override
  // bool operator ==(Object other) =>
  //     identical(this, other) ||
  //     other is Product &&
  //         runtimeType == other.runtimeType &&
  //         naam == other.naam;

  // @override
  // int get hashCode => naam.hashCode;

  factory Product.fromJson(Map<String, dynamic> json) {
    return Product(
        iD: json['ID'],
        naam: json['naam'],
        prijs: json['prijs'],
        beschrijving: json['beschrijving'],
        link: json['link'],
        // leverancierID: json['leverancierID'],
        imageBase64: json['imageBase64']);
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
