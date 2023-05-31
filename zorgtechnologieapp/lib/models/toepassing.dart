class HeeftToepassing {
  String toepassing;
  String productnaam;
  int productID;

  HeeftToepassing({
    required this.toepassing,
    required this.productnaam,
    required this.productID,
  });

  factory HeeftToepassing.fromJson(Map<String, dynamic> json) {
    return HeeftToepassing(
      toepassing: json['toepassing'],
      productnaam: json['productnaam'],
      productID: json['productID'],
    );
  }

  Map<String, dynamic> toJson() {
    final Map<String, dynamic> data = <String, dynamic>{};
    data['toepassing'] = toepassing;
    data['productnaam'] = productnaam;
    data['productID'] = productID;
    return data;
  }
}

class Toepassing {
  String toepassing;
  int? iD;
  int? productID;

  Toepassing({required this.toepassing, this.iD, this.productID});

  @override
  bool operator ==(Object other) =>
      identical(this, other) ||
      other is Toepassing &&
          runtimeType == other.runtimeType &&
          toepassing == other.toepassing;

  @override
  int get hashCode => toepassing.hashCode;

  factory Toepassing.fromJson(Map<String, dynamic> json) {
    return Toepassing(
      toepassing: json['toepassing'],
      iD: json['ID'],
      productID: json['productID'],
    );
  }

  Map<String, dynamic> toJson() {
    final Map<String, dynamic> data = <String, dynamic>{};
    data['toepassing'] = toepassing;
    data['ID'] = iD;
    data['productID'] = productID;
    return data;
  }
}
