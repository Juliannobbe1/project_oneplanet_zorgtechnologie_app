import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:logger/logger.dart';
import 'package:zorgtechnologieapp/pages/client_overview_page.dart';
import 'package:zorgtechnologieapp/providers/logging_provider/logging_provider.dart';

import '../handlers/data_api_handler.dart';
import '../handlers/responsive_layout_handler.dart';
import '../models/products.dart';
import '../widgets/futurebuilder.dart';
import 'products_page.dart';
import 'selection_guide.dart';

class HomePage extends StatelessWidget {
  const HomePage({super.key});

  @override
  Widget build(BuildContext context) {
    final deviceType = ResponsiveLayout.getDeviceType(
        context); // Determine the type of device (e.g., phone, tablet, desktop)
    double screenWidth =
        MediaQuery.of(context).size.width; // Get the width of the screen
    double screenHeight =
        MediaQuery.of(context).size.height; // Get the height of the screen

    return Scaffold(
      backgroundColor:
          Colors.indigo[50], // Set the background color of the scaffold
      appBar: AppBar(
        leading:
            const Icon(Icons.menu), // Display a menu icon as the leading widget
        title: const Text(
          "Welcome", // Set the title of the app bar
        ),
      ),
      body: Column(
        children: [
          if (deviceType == DeviceType.tablet ||
              deviceType == DeviceType.desktop) ...[
            TabletHomeScreen(
              screenHeight: screenHeight,
              screenWidth: screenWidth,
            ) // Display a tablet-specific or desktop-specific home screen
          ] else ...[
            PhoneHomeScreen(
                screenWidth:
                    screenWidth) // Display a phone-specific home screen
          ]
        ],
      ),
    );
  }
}

class TabletHomeScreen extends ConsumerWidget {
  final double screenWidth;
  final double screenHeight;

  const TabletHomeScreen({
    Key? key,
    required this.screenHeight,
    required this.screenWidth,
  }) : super(key: key);

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final logger = ref.watch(loggingProvider);

    return Expanded(
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              // Button to Keuzegids
              Expanded(
                flex: 1,
                child: Padding(
                  padding: const EdgeInsets.fromLTRB(30, 45, 20, 20),
                  child: Material(
                    elevation: 10,
                    borderRadius: const BorderRadius.all(Radius.circular(10)),
                    child: Container(
                      decoration: BoxDecoration(
                        borderRadius: const BorderRadius.all(
                          Radius.circular(10),
                        ),
                        color: Colors.blue[800],
                      ),
                      child: Center(
                        child: TextButton(
                          style: TextButton.styleFrom(
                            fixedSize: const Size(300, 150),
                          ),
                          onPressed: () {
                            Navigator.of(context).push(MaterialPageRoute(
                              builder: (context) => const ClientOverview(),
                            ));
                          },
                          child: Text(
                            "Keuzegids", // Button text
                            style: SizeScaler.getResponsiveTextStyle(
                                context,
                                20,
                                FontWeight.normal,
                                Colors
                                    .white), // Define the text style using SizeScaler for responsive text sizing
                          ),
                        ),
                      ),
                    ),
                  ),
                ),
              ),

              // Button to Catalogus
              Expanded(
                flex: 1,
                child: Padding(
                  padding: const EdgeInsets.fromLTRB(20, 45, 30, 20),
                  child: Material(
                    elevation: 10,
                    borderRadius: const BorderRadius.all(Radius.circular(10)),
                    child: Container(
                      decoration: BoxDecoration(
                        borderRadius: const BorderRadius.all(
                          Radius.circular(10),
                        ),
                        color: Colors.blue[800],
                      ),
                      child: Center(
                        child: TextButton(
                          style: TextButton.styleFrom(
                            fixedSize: const Size(300, 150),
                          ),
                          onPressed: () {
                            Navigator.of(context).push(MaterialPageRoute(
                              builder: (context) => const ProductPage(),
                            ));
                          },
                          child: Text(
                            "Technologie-catalogus", // Button text
                            style: SizeScaler.getResponsiveTextStyle(
                                context,
                                20,
                                FontWeight.normal,
                                Colors
                                    .white), // Define the text style using SizeScaler for responsive text sizing
                          ),
                        ),
                      ),
                    ),
                  ),
                ),
              ),
            ],
          ),

          // Newest Products
          Padding(
            padding: EdgeInsets.only(
                left: screenWidth * 0.025, top: screenWidth * 0.05),
            child: Text(
              "Nieuwste producten: ", // Heading text
              style: SizeScaler.getResponsiveTextStyle(
                  context,
                  21,
                  FontWeight.bold,
                  Colors
                      .black), // Define the text style using SizeScaler for responsive text sizing
            ),
          ),
          FutureDataWidget(
              fetchData: DataAPI(logger: logger)
                  .newestProducts(), // Fetch the newest products data using DataAPI
              countRow: 2, // Display two products per row
              widgetType: FutureWidgetType
                  .gridView, // Use gridView as the widget type for displaying the products
              dataType: FutureDataType
                  .product), // Specify that the data type is a product
        ],
      ),
    );
  }
}

class PhoneHomeScreen extends ConsumerWidget {
  final double screenWidth;

  const PhoneHomeScreen({super.key, required this.screenWidth});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    Logger logger = ref.watch(loggingProvider);

    return Expanded(
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          // Button to Keuzegids
          Padding(
            padding: const EdgeInsets.fromLTRB(15.0, 20.0, 15.0, 5.0),
            child: AspectRatio(
              aspectRatio: 16 / 5,
              child: Material(
                elevation: 5,
                borderRadius: const BorderRadius.all(Radius.circular(10)),
                child: Container(
                  decoration: BoxDecoration(
                    borderRadius: const BorderRadius.all(
                      Radius.circular(10),
                    ),
                    color: Colors.blue[900],
                  ),
                  child: Center(
                    child: TextButton(
                      onPressed: () {
                        Navigator.of(context).push(MaterialPageRoute(
                            builder: (context) => const SelectionGuidePage()));
                      },
                      child: Text(
                        "Keuzegids", // Button text
                        style: SizeScaler.getResponsiveTextStyle(
                            context,
                            20,
                            FontWeight.bold,
                            Colors
                                .white), // Define the text style using SizeScaler for responsive text sizing
                      ),
                    ),
                  ),
                ),
              ),
            ),
          ),

          // Button to Technologie-catalogus
          Padding(
            padding: const EdgeInsets.all(15.0),
            child: AspectRatio(
              aspectRatio: 16 / 5,
              child: Material(
                elevation: 5,
                borderRadius: const BorderRadius.all(Radius.circular(10)),
                child: Container(
                  decoration: BoxDecoration(
                    borderRadius: const BorderRadius.all(
                      Radius.circular(10),
                    ),
                    color: Colors.blue[800],
                  ),
                  child: Center(
                    child: TextButton(
                      onPressed: () {
                        Navigator.of(context).push(MaterialPageRoute(
                            builder: (context) => const ProductPage()));
                      },
                      child: Text(
                        "Technologie-catalogus", // Button text
                        style: SizeScaler.getResponsiveTextStyle(
                            context,
                            20,
                            FontWeight.bold,
                            Colors
                                .white), // Define the text style using SizeScaler for responsive text sizing
                      ),
                    ),
                  ),
                ),
              ),
            ),
          ),

          // Heading for Newest Products
          Padding(
            padding: EdgeInsets.only(left: screenWidth * 0.03, top: 15),
            child: Text(
              "Nieuwste producten:", // Heading text
              style: SizeScaler.getResponsiveTextStyle(
                  context,
                  22,
                  FontWeight.bold,
                  Colors
                      .black), // Define the text style using SizeScaler for responsive text sizing
            ),
          ),

          // FutureBuilder for displaying Newest Products
          FutureBuilder<List<Product>>(
            future: DataAPI(logger: logger)
                .newestProducts(), // Fetch the newest products data using DataAPI
            builder: (context, snapshot) {
              if (snapshot.hasData) {
                logger.t(
                    "Successfully retrieved '${snapshot.data}' newest products.");
                final products = snapshot.data!;
                return SizedBox(
                  height: 325,
                  child: ListView.builder(
                    itemCount: products.length,
                    itemBuilder: (context, index) {
                      final product = products[index];
                      return Padding(
                        padding:
                            const EdgeInsets.fromLTRB(15.0, 10.0, 15.0, 10.0),
                        child: Material(
                          elevation: 5,
                          borderRadius:
                              const BorderRadius.all(Radius.circular(10)),
                          child: Container(
                            decoration: BoxDecoration(
                              borderRadius: const BorderRadius.all(
                                Radius.circular(10),
                              ),
                              color: Colors.blue[500],
                            ),
                            child: ListTile(
                              title: Text(
                                product.naam, // Product name
                                style: SizeScaler.getResponsiveTextStyle(
                                    context,
                                    18,
                                    FontWeight.bold,
                                    Colors
                                        .white), // Define the text style using SizeScaler for responsive text sizing
                              ),
                              trailing: SingleProductView(
                                productId: product
                                    .iD, // Pass the product ID to SingleProductView widget
                              ),
                            ),
                          ),
                        ),
                      );
                    },
                  ),
                );
              } else if (snapshot.hasError) {
                logger.e(
                    "An error occurred while retrieving the newest products: '${snapshot.error}'");
                return Center(
                    child: Text(
                        "${snapshot.error}")); // Display an error message if there's an error in fetching the data
              } else {
                return const Center(
                    child:
                        CircularProgressIndicator()); // Display a progress indicator while data is being fetched
              }
            },
          ),
        ],
      ),
    );
  }
}
