import 'dart:convert';
import 'package:http/http.dart' as http;
import '../models/products.dart';
import '../models/toepassing.dart';
import '../models/clients.dart';

class DataAPI {
  String baseUrl = 'http://192.168.123.41:5001';

  Future<List<dynamic>> fetchData(String endpoint) async {
    String url = '$baseUrl$endpoint';
    http.Response response = await http.get(Uri.parse(url));
    if (response.statusCode == 200) {
      final List<dynamic> result = jsonDecode(response.body);
      return result;
    } else {
      throw Exception(response.reasonPhrase);
    }
  }

  Future<void> postData(String endpoint, payload) async {
    final url = '$baseUrl$endpoint';

    final response = await http.post(Uri.parse(url),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode(payload));

    if (response.statusCode == 200) {
      final responseBody = jsonDecode(response.body);
      print(responseBody[
          'message']); // Replace 'message' with the appropriate key in the response
    } else {
      throw Exception(response.reasonPhrase);
    }
  }

  Future<void> putData(String endpoint) async {
    final url = '$baseUrl$endpoint';

    final response = await http.put(Uri.parse(url));

    if (response.statusCode == 200) {
      final responseBody = jsonDecode(response.body);
      print(
          responseBody); // Replace 'message' with the appropriate key in the response
    } else {
      throw Exception(response.reasonPhrase);
    }
  }

  Future<void> createClientRelationship(int clientID, int zorgprofID) async {
    await putData('/client/relationship/$clientID/$zorgprofID');
  }

  Future<void> createClient(int id, String probleem) async {
    final payload = {"ID": id, "probleem": probleem};
    await postData('/client/', payload);
  }

  Future<List<Clients>> latestClient() async {
    List<dynamic> result = await fetchData('/client/latest');
    return result
        .map((e) => Clients.fromJson(e as Map<String, dynamic>))
        .toList();
  }

  Future<List<Product>> getProducts() async {
    List<dynamic> result = await fetchData('/product');
    return result
        .map((e) => Product.fromJson(e as Map<String, dynamic>))
        .toList();
  }

  Future<List<Product>> getOneProducts(int id) async {
    List<dynamic> result = await fetchData('/product/$id');
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

  Future<List<Product>> getProductsForClient(int clientID) async {
    List<dynamic> result = await fetchData('/product/client/$clientID');
    return result
        .map((e) => Product.fromJson(e as Map<String, dynamic>))
        .toList();
  }

  Future<List<Product>> recommendedProducts(
      int zorgprofID, int clientID) async {
    List<dynamic> result =
        await fetchData('/product/aanbeveling/$zorgprofID/$clientID');
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

  Future<List<Clients>> providedClient(int zorgprofID) async {
    List<dynamic> result = await fetchData('/client/wordtverzorgd/$zorgprofID');
    return result
        .map((e) => Clients.fromJson(e as Map<String, dynamic>))
        .toList();
  }
}
