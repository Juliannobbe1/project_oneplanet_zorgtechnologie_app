import 'dart:convert';
import 'package:http/http.dart';

import '../models/products.dart';

class ApiCall {
  String uri = 'http://172.16.1.149:5001/product';
  Future<List<Product>> getProducts() async {
    Response response = await get(Uri.parse(uri));
    if (response.statusCode == 200) {
      final List result = jsonDecode(response.body);
      return result.map(((e) => Product.fromJson(e))).toList();
    } else {
      throw Exception(response.reasonPhrase);
    }
  }

  String newestProductsUri = 'http://172.16.1.149:5001/product/newest';
  Future<List<Product>> newestProducts() async {
    Response response = await get(Uri.parse(newestProductsUri));
    if (response.statusCode == 200) {
      final List result = jsonDecode(response.body);
      return result.map(((e) => Product.fromJson(e))).toList();
    } else {
      throw Exception(response.reasonPhrase);
    }
  }
}
