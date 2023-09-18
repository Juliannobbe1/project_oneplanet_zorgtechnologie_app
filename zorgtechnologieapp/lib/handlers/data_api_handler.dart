import 'dart:convert';
import 'dart:developer';
import 'package:http/http.dart' as http;
import '../models/products.dart';
import '../models/toepassing.dart';
import '../models/clients.dart';

class DataAPI {
  String baseUrl = 'http://192.168.72.182:5001';

  /// Fetches data from the specified [endpoint] using a GET request.
  /// Returns a [Future] that resolves to a list of dynamic objects.
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

  /// Sends data to the specified [endpoint] using a POST request.
  /// The [payload] is the data to be sent in the request body.
  Future<void> postData(String endpoint, payload) async {
    final url = '$baseUrl$endpoint';

    final response = await http.post(Uri.parse(url),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode(payload));
    if (response.statusCode == 200) {
      // Handle successful response if needed
    } else {
      throw Exception(response.reasonPhrase);
    }
  }

  /// Sends a PUT request to the specified [endpoint].
  Future<void> putData(String endpoint) async {
    final url = '$baseUrl$endpoint';

    final response = await http.put(Uri.parse(url));

    if (response.statusCode == 200) {
      final responseBody = jsonDecode(response.body);
      log('$responseBody'); // Replace 'message' with the appropriate key in the response
    } else {
      throw Exception(response.reasonPhrase);
    }
  }

  /// Deletes a client with the specified [id].
  Future<void> deleteClient(String id) async {
    String url = '$baseUrl/client/$id';
    http.Response response = await http.delete(Uri.parse(url));
    if (response.statusCode != 200) {
      throw Exception(response.reasonPhrase);
    }
  }

  /// Creates a relationship between a client and a caregiver.
  Future<void> createClientRelationship(
      String clientID, String zorgprofID) async {
    await putData('/client/relationship/$clientID/$zorgprofID');
  }

  /// Creates a relationship between a client, a caregiver, and a product.
  Future<void> createRecommendationRelationship(
      String clientID, String zorgprofessionalID, String productID) async {
    await putData('/aanbeveling/$zorgprofessionalID/$productID/$clientID');
  }

  /// Creates a new client with the specified [id] and [probleem].
  Future<void> createClient(String id, String probleem) async {
    final payload = {"ID": id, "probleem": probleem};
    await postData('/client/', payload);
  }

  /// Retrieves the latest client(s) from the API.
  Future<List<Clients>> latestClient() async {
    List<dynamic> result = await fetchData('/client/latest');
    return result
        .map((e) => Clients.fromJson(e as Map<String, dynamic>))
        .toList();
  }

  /// Retrieves a list of products from the API.
  Future<List<Product>> getProducts() async {
    List<dynamic> result = await fetchData('/product');
    return result
        .map((e) => Product.fromJson(e as Map<String, dynamic>))
        .toList();
  }

  /// Retrieves a single product with the specified [id] from the API.
  Future<List<Product>> getOneProducts(int id) async {
    List<dynamic> result = await fetchData('/product/$id');
    return result
        .map((e) => Product.fromJson(e as Map<String, dynamic>))
        .toList();
  }

  /// Retrieves the newest products from the API.
  Future<List<Product>> newestProducts() async {
    List<dynamic> result = await fetchData('/product/newest');
    return result
        .map((e) => Product.fromJson(e as Map<String, dynamic>))
        .toList();
  }

  /// Retrieves the products associated with a specific [clientID] from the API.
  Future<List<Product>> getProductsForClient(String clientID) async {
    List<dynamic> result = await fetchData('/product/client/$clientID');
    return result
        .map((e) => Product.fromJson(e as Map<String, dynamic>))
        .toList();
  }

  /// Retrieves the recommended products based on a [zorgprofID] and [probleem] from the API.
  Future<List<Product>> recommendedProducts(
      String zorgprofID, String probleem) async {
    List<dynamic> result =
        await fetchData('/product/aanbeveling/$zorgprofID/$probleem');
    return result
        .map((e) => Product.fromJson(e as Map<String, dynamic>))
        .toList();
  }

  /// Retrieves a list of products with their applications from the API.
  Future<List<HeeftToepassing>> toepassingProducts() async {
    List<dynamic> result = await fetchData('/toepassing/HEEFT_TOEPASSING');
    return result
        .map((e) => HeeftToepassing.fromJson(e as Map<String, dynamic>))
        .toList();
  }

  /// Retrieves distinct applications from the API.
  Future<List<Toepassing>> distinctToepassing() async {
    List<dynamic> result = await fetchData('/toepassing/distinct');
    return result
        .map((toepassing) => Toepassing(toepassing: toepassing))
        .toList();
  }

  /// Retrieves distinct client problems from the API.
  Future<List<Clients>> distinctProbleem() async {
    List<dynamic> result = await fetchData('/client/distinct-problem');
    return result.map((probleem) => Clients(probleem: probleem)).toList();
  }

  /// Retrieves clients associated with a specific [zorgprofID] from the API.
  Future<List<Clients>> providedClient(String zorgprofID) async {
    List<dynamic> result = await fetchData('/client/wordtverzorgd/$zorgprofID');
    return result
        .map((e) => Clients.fromJson(e as Map<String, dynamic>))
        .toList();
  }
}
