class Clients {
  String probleem;
  String? iD;

  Clients({required this.probleem, this.iD});

  @override
  bool operator ==(Object other) =>
      identical(this, other) ||
      other is Clients &&
          runtimeType == other.runtimeType &&
          probleem == other.probleem;

  @override
  int get hashCode => probleem.hashCode;

  factory Clients.fromJson(Map<String, dynamic> json) {
    return Clients(
      probleem: json['probleem'],
      iD: json['ID'],
    );
  }

  Map<String, dynamic> toJson() {
    final Map<String, dynamic> data = <String, dynamic>{};
    data['probleem'] = probleem;
    data['ID'] = iD;
    return data;
  }
}
