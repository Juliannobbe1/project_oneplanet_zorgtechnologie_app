import 'dart:convert';
import 'package:http/http.dart';

import '../models/products.dart';

class ApiCall {
  String uri = 'http://192.168.123.41:5001/products';
  Future<List<Product>> getProducts() async {
    Response response = await get(Uri.parse(uri));
    if (response.statusCode == 200) {
      final List result = jsonDecode(response.body);
      return result.map(((e) => Product.fromJson(e))).toList();
    } else {
      throw Exception(response.reasonPhrase);
    }
  }
}
