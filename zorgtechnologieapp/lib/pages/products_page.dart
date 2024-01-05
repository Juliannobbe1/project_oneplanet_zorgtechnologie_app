import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:logger/logger.dart';
import 'package:zorgtechnologieapp/providers/logging_provider/logging_provider.dart';

import '../handlers/data_api_handler.dart';
import '../handlers/responsive_layout_handler.dart';
import '../models/products.dart';
import '../widgets/futurebuilder.dart';

class ProductPage extends ConsumerWidget {
  const ProductPage({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final logger = ref.watch(loggingProvider);

    return Scaffold(
      backgroundColor: Colors.indigo[50],
      appBar: AppBar(
        title: Text(
          "Technologie Overzicht", // App bar title
          style: SizeScaler.getResponsiveTextStyle(
              context,
              16,
              FontWeight.bold,
              Colors
                  .white), // Define the text style using SizeScaler for responsive text sizing
        ),
      ),
      body: Column(
        children: [
          FutureDataWidget(
              fetchData: DataAPI(logger: logger)
                  .getProducts(), // Fetch product data using DataAPI
              countRow: 2, // Specify the number of rows for the grid view
              widgetType:
                  FutureWidgetType.gridView, // Display the data in a grid view
              dataType:
                  FutureDataType.product), // Specify the data type as product
        ],
      ),
    );
  }
}

class SingleProductView extends ConsumerWidget {
  final String productId;

  const SingleProductView({super.key, required this.productId});

  Future<Product> fetchProduct(Logger logger) async {
    List<Product> products = await DataAPI(logger: logger)
        .getProducts(); // Fetch all products using DataAPI
    return products.firstWhere((product) =>
        product.iD == productId); // Find the product with matching ID
  }

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    Logger logger = ref.watch(loggingProvider);

    return FutureBuilder<Product>(
      future: fetchProduct(
          logger), // Fetch the product data using fetchProduct() method
      builder: (context, snapshot) {
        if (snapshot.hasData) {
          logger.t("Successfully retrieved product data: '${snapshot.data}'");
          // If product data is available
          Product product = snapshot.data!; // Get the product object
          return IconButton(
            key: ValueKey("SingleProductViewButton | ${product.iD}"),
            icon: const Icon(
              Icons.info,
              color: Colors.black,
            ),
            onPressed: () {
              showDialog(
                context: context,
                builder: (context) => Dialog(
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(10),
                  ),
                  child: Container(
                    padding: const EdgeInsets.all(16),
                    constraints: const BoxConstraints(maxHeight: 600),
                    child: SingleChildScrollView(
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text(
                            product.naam, // Display the product name
                            style: SizeScaler.getResponsiveTextStyle(
                                context, 20, FontWeight.bold, Colors.black),
                          ),
                          const SizedBox(height: 10),
                          Text(
                            product
                                .beschrijving, // Display the product description
                            style: SizeScaler.getResponsiveTextStyle(
                                context, 20, FontWeight.normal, Colors.black),
                          ),
                          const SizedBox(height: 5),
                          Text(
                            'Prijs: ${product.prijs}', // Display the product price
                            style: SizeScaler.getResponsiveTextStyle(
                                context, 20, FontWeight.normal, Colors.black),
                          ),
                          const SizedBox(height: 5),
                          Text(
                            'Link: ${product.link}', // Display the product link
                            style: SizeScaler.getResponsiveTextStyle(
                                context, 20, FontWeight.normal, Colors.black),
                          ),
                          Row(
                            mainAxisAlignment: MainAxisAlignment.end,
                            children: [
                              TextButton(
                                child: const Text('Close'), // Close button text
                                onPressed: () =>
                                    Navigator.pop(context), // Close the dialog
                              ),
                            ],
                          ),
                        ],
                      ),
                    ),
                  ),
                ),
              );
            },
          );
        } else if (snapshot.hasError) {
          logger.e(
              "An error occurred while fetching product data: '${snapshot.error}'");
          // If there's an error fetching product data
          return IconButton(
            icon: const Icon(
              Icons.info,
              color: Colors.black,
            ),
            onPressed: () {
              showDialog(
                context: context,
                builder: (context) => AlertDialog(
                  title: const Text('Error'),
                  content: const Text(
                      'Failed to fetch product details.'), // Display error message
                  actions: [
                    TextButton(
                      child: const Text('Close'), // Close button text
                      onPressed: () =>
                          Navigator.pop(context), // Close the dialog
                    ),
                  ],
                ),
              );
            },
          );
        } else {
          // If product data is still loading
          return IconButton(
            icon: const Icon(
              Icons.info,
              color: Colors.black,
            ),
            onPressed: () {
              showDialog(
                context: context,
                builder: (context) => const Center(
                  child:
                      CircularProgressIndicator(), // Display a loading indicator
                ),
              );
            },
          );
        }
      },
    );
  }
}
