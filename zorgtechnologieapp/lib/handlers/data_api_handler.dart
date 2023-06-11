import 'dart:convert';
import 'package:http/http.dart';
import '../models/products.dart';
import '../models/toepassing.dart';
import '../models/clients.dart';

class DataAPI {
  String baseUrl = 'http://172.16.1.149:5001';

  Future<List<dynamic>> fetchData(String endpoint) async {
    String url = '$baseUrl$endpoint';
    Response response = await get(Uri.parse(url));
    if (response.statusCode == 200) {
      final List<dynamic> result = jsonDecode(response.body);
      return result;
    } else {
      throw Exception(response.reasonPhrase);
    }
  }

  Future<List<Product>> getProducts() async {
    List<dynamic> result = await fetchData('/product');
    return result
        .map((e) => Product.fromJson(e as Map<String, dynamic>))
        .toList();
  }

  Future<List<Product>> newestProducts() async {
    List<dynamic> result = await fetchData('/product/newest');
    return result
        .map((e) => Product.fromJson(e as Map<String, dynamic>))
        .toList();
  }

  Future<List<HeeftToepassing>> toepassingProducts() async {
    List<dynamic> result = await fetchData('/toepassing/HEEFT_TOEPASSING');
    return result
        .map((e) => HeeftToepassing.fromJson(e as Map<String, dynamic>))
        .toList();
  }

  Future<List<Toepassing>> distinctToepassing() async {
    List<dynamic> result = await fetchData('/toepassing/distinct');
    return result
        .map((toepassing) => Toepassing(toepassing: toepassing))
        .toList();
  }

  Future<List<Clients>> distinctProbleem() async {
    List<dynamic> result = await fetchData('/client/distinct-problem');
    return result.map((probleem) => Clients(probleem: probleem)).toList();
  }
}
