import 'dart:convert';
import 'package:flutter/foundation.dart';
import 'package:http/http.dart' as http;
import 'package:logger/logger.dart';
import '../models/products.dart';
import '../models/toepassing.dart';
import '../models/clients.dart';

const kDebugApiBaseUrl = "http://10.0.2.2:5001";
const kProdApiBaseUrl = "http://10.0.2.2:5001";
const kApiBaseUrl = kDebugMode ? kDebugApiBaseUrl : kProdApiBaseUrl;

class DataAPI {
  Logger logger;

  DataAPI({required this.logger});

  /// Fetches data from the specified [endpoint] using a GET request.
  /// Returns a [Future] that resolves to a list of dynamic objects.
  Future<List<dynamic>> fetchData(String endpoint) async {
    String url = '$kApiBaseUrl$endpoint';
    logger.t("Retrieving data from '$url'");
    http.Response response = await http.get(Uri.parse(url));
    if (response.statusCode == 200) {
      final List<dynamic> result = jsonDecode(response.body);
      logger.t("Retrieved data '$result'");
      return result;
    } else {
      logger.e("Error occurred retrieving data: '${response.reasonPhrase}'");
      throw Exception(response.reasonPhrase);
    }
  }

  /// Sends data to the specified [endpoint] using a POST request.
  /// The [payload] is the data to be sent in the request body.
  Future<void> postData(String endpoint, payload) async {
    final url = '$kApiBaseUrl$endpoint';

    logger.t("Sending POST request to '$url' with payload '$payload'");

    final response = await http.post(Uri.parse(url),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode(payload));
    if (response.statusCode == 200) {
      logger.t("POST request was handled successfully");
      // Handle successful response if needed
    } else {
      logger.e("Error occurred POSTing data: '${response.reasonPhrase}'");
      throw Exception(response.reasonPhrase);
    }
  }

  /// Sends a PUT request to the specified [endpoint].
  Future<void> putData(String endpoint) async {
    final url = '$kApiBaseUrl$endpoint';

    logger.t("Sending PUT request to '$url'");

    final response = await http.put(Uri.parse(url));

    if (response.statusCode == 200) {
      final responseBody = jsonDecode(response.body);
      logger
          .t("PUT request was handled successfully with body '$responseBody'");
    } else {
      logger.e("Error occurred PUTing data: '${response.reasonPhrase}'");
      throw Exception(response.reasonPhrase);
    }
  }

  /// Deletes a client with the specified [id].
  Future<void> deleteClient(String id) async {
    String url = '$kApiBaseUrl/client/$id';
    logger.i("Attempting to delete client '$id'");

    http.Response response = await http.delete(Uri.parse(url));
    if (response.statusCode != 200) {
      logger.e("Failed to delete client '$id': '${response.reasonPhrase}'");
      throw Exception(response.reasonPhrase);
    }
    logger.i("Successfully deleted client '$id'");
  }

  /// Creates a relationship between a client and a caregiver.
  Future<void> createClientRelationship(
      String clientID, String zorgprofID) async {
    logger.i(
        "Attempting to create client relationship between client '$clientID' and caregiver '$zorgprofID'");
    await putData('/client/relationship/$clientID/$zorgprofID');
  }

  /// Creates a relationship between a client, a caregiver, and a product.
  Future<void> createRecommendationRelationship(
      String clientID, String zorgprofessionalID, String productID) async {
    logger.i(
        "Attempting to create recommendation relationship between client '$clientID' and caregiver '$zorgprofessionalID' for product '$productID'");
    await putData('/aanbeveling/$zorgprofessionalID/$productID/$clientID');
  }

  /// Creates a new client with the specified [id] and [probleem].
  Future<void> createClient(String id, String probleem) async {
    logger.i("Attempting to create client '$id' with probleem '$probleem'");
    final payload = {"ID": id, "probleem": probleem};
    await postData('/client/', payload);
  }

  /// Retrieves the latest client(s) from the API.
  Future<List<Clients>> latestClient() async {
    logger.i("Attempting to retrieve the latest clients");
    List<dynamic> result = await fetchData('/client/latest');
    List<Clients> clients =
        result.map((e) => Clients.fromJson(e as Map<String, dynamic>)).toList();
    logger.i("Retrieved '${clients.length}' latest clients");
    return clients;
  }

  /// Retrieves a list of products from the API.
  Future<List<Product>> getProducts() async {
    logger.i("Attempting to retrieve products");
    List<dynamic> result = await fetchData('/product');
    List<Product> products =
        result.map((e) => Product.fromJson(e as Map<String, dynamic>)).toList();
    logger.i("Retrieved '${products.length}' products");
    return products;
  }

  /// Retrieves a single product with the specified [id] from the API.
  Future<List<Product>> getOneProducts(int id) async {
    logger.i("Attempting to retrieve product '$id'");
    List<dynamic> result = await fetchData('/product/$id');
    List<Product> products =
        result.map((e) => Product.fromJson(e as Map<String, dynamic>)).toList();
    logger.i("Retrieved product '${products[0]}'");
    return products;
  }

  /// Retrieves the newest products from the API.
  Future<List<Product>> newestProducts() async {
    logger.i("Attempting to retrieve the latest products");
    List<dynamic> result = await fetchData('/product/newest');
    List<Product> products =
        result.map((e) => Product.fromJson(e as Map<String, dynamic>)).toList();
    logger.i("Retrieved '${products.length}' latest products");
    return products;
  }

  /// Retrieves the products associated with a specific [clientID] from the API.
  Future<List<Product>> getProductsForClient(String clientID) async {
    logger.i("Attempting to retrieve products for client '$clientID'");
    List<dynamic> result = await fetchData('/product/client/$clientID');
    List<Product> products =
        result.map((e) => Product.fromJson(e as Map<String, dynamic>)).toList();
    logger.i("Retrieved '${products.length}' products for client $clientID");
    return products;
  }

  /// Retrieves the recommended products based on a [zorgprofID] and [probleem] from the API.
  Future<List<Product>> recommendedProducts(
      String zorgprofID, String probleem) async {
    logger.i(
        "Attempting to retrieve recommended products for caregiver '$zorgprofID' and probleem '$probleem'");
    List<dynamic> result =
        await fetchData('/product/aanbeveling/$zorgprofID/$probleem');
    List<Product> products =
        result.map((e) => Product.fromJson(e as Map<String, dynamic>)).toList();
    logger.i(
        "Retrieved '${products.length}' recommended products for caregiver '$zorgprofID' and probleem '$probleem'");
    return products;
  }

  /// Retrieves a list of products with their applications from the API.
  Future<List<HeeftToepassing>> toepassingProducts() async {
    logger.i("Attempting to retrieve products with toepassingen");
    List<dynamic> result = await fetchData('/toepassing/HEEFT_TOEPASSING');
    List<HeeftToepassing> products = result
        .map((e) => HeeftToepassing.fromJson(e as Map<String, dynamic>))
        .toList();
    logger.i("Retrieved '${products.length}' products with toepassingen");
    return products;
  }

  /// Retrieves distinct applications from the API.
  Future<List<Toepassing>> distinctToepassing() async {
    logger.i("Attempting to retrieve distinct toepassingen");
    List<dynamic> result = await fetchData('/toepassing/distinct');
    List<Toepassing> toepassingen =
        result.map((toepassing) => Toepassing(toepassing: toepassing)).toList();
    logger.i("Retrieved '${toepassingen.length}' distinct toepassingen");
    return toepassingen;
  }

  /// Retrieves distinct client problems from the API.
  Future<List<Clients>> distinctProbleem() async {
    logger.i("Attempting to retrieve distinct client problems");
    List<dynamic> result = await fetchData('/client/distinct-problem');
    List<Clients> clientProblems =
        result.map((probleem) => Clients(probleem: probleem)).toList();
    logger.i("Retrieved '${clientProblems.length}' distinct client problems");
    return clientProblems;
  }

  /// Retrieves clients associated with a specific [zorgprofID] from the API.
  Future<List<Clients>> providedClient(String zorgprofID) async {
    logger.i("Attempting to retrieve clients for caregiver '$zorgprofID'");
    List<dynamic> result = await fetchData('/client/wordtverzorgd/$zorgprofID');
    List<Clients> clients =
        result.map((e) => Clients.fromJson(e as Map<String, dynamic>)).toList();
    logger
        .i("Retrieved '${clients.length}' clients for caregiver '$zorgprofID'");
    return clients;
  }
}
