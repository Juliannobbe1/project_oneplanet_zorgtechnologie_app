import 'dart:convert';
import 'package:http/http.dart' as http;

import 'products.dart';

Future<List<Product>> getProducts() async {
  var url = Uri.parse('http://localhost:5000/products');
  var response = await http.get(url);
  if (response.statusCode == 200) {
    List<dynamic> data = json.decode(response.body);
    List<Product> products =
        data.map((item) => Product.fromJson(item)).toList();
    return products;
  } else {
    throw Exception('Failed to load products');
  }
}
