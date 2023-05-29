import 'package:flutter/material.dart';

import '../handlers/get_products.dart';
import '../handlers/responsive_layout_handler.dart';
import '../models/products.dart';
import 'products_page.dart';
import 'selection_guide.dart';

class HomePage extends StatelessWidget {
  const HomePage({super.key});

  @override
  Widget build(BuildContext context) {
    final deviceType = ResponsiveLayout.getDeviceType(context);
    double screenWidth = MediaQuery.of(context).size.width;
    double screenHeight = MediaQuery.of(context).size.height;

    return Scaffold(
      backgroundColor: Colors.indigo[50],
      appBar: AppBar(
        leading: const Icon(Icons.menu),
        title: Text(
          "$deviceType",
        ),
      ),
      body: Column(
        children: [
          if (deviceType == DeviceType.tablet ||
              deviceType == DeviceType.desktop) ...[
            TabletHomeScreen(
              screenHeight: screenHeight,
              screenWidth: screenWidth,
            )
          ] else ...[
            PhoneHomeScreen(screenWidth: screenWidth)
          ]
        ],
      ),
    );
  }
}

class TabletHomeScreen extends StatelessWidget {
  final double screenWidth;
  final double screenHeight;

  const TabletHomeScreen({
    Key? key,
    required this.screenHeight,
    required this.screenWidth,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Expanded(
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
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
                        color: Colors.blue[900],
                      ),
                      child: Center(
                        child: TextButton(
                          style: TextButton.styleFrom(
                            fixedSize: const Size(300, 150),
                          ),
                          onPressed: () {
                            Navigator.of(context).push(MaterialPageRoute(
                              builder: (context) => const SelectionGuidePage(),
                            ));
                          },
                          child: Text(
                            "Keuzegids",
                            style: SizeScaler.getResponsiveTextStyle(
                                context, 20, FontWeight.normal, Colors.white),
                          ),
                        ),
                      ),
                    ),
                  ),
                ),
              ),
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
                            "Technologie-catalogus",
                            style: SizeScaler.getResponsiveTextStyle(
                                context, 20, FontWeight.normal, Colors.white),
                          ),
                        ),
                      ),
                    ),
                  ),
                ),
              ),
            ],
          ),
          Padding(
            padding: EdgeInsets.only(
                left: screenWidth * 0.025, top: screenWidth * 0.05),
            child: Text(
              "Nieuwste producten: $screenHeight",
              style: SizeScaler.getResponsiveTextStyle(
                  context, 21, FontWeight.bold, Colors.black),
            ),
          ),
          FutureBuilder<List<Product>>(
            future: ApiCall().newestProducts(),
            builder: (context, snapshot) {
              if (snapshot.hasData) {
                final products = snapshot.data!;
                return Padding(
                  padding: const EdgeInsets.fromLTRB(10, 0, 10, 10.0),
                  child: SizedBox(
                    height: screenHeight > 900
                        ? screenHeight * 0.65
                        : screenHeight *
                            0.50, // Specify the desired height for the ListView
                    child: GridView.builder(
                      gridDelegate: SliverGridDelegateWithFixedCrossAxisCount(
                        crossAxisCount: 2, // Number of columns in the grid
                        childAspectRatio: screenHeight > 900
                            ? 3.5
                            : 4.5, // Width to height ratio of each grid item
                      ),
                      itemCount: products.length,
                      itemBuilder: (context, index) {
                        final product = products[index];
                        return Padding(
                          padding: const EdgeInsets.fromLTRB(20, 25, 20, 5),
                          child: Material(
                            elevation: 10,
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
                                  product.productNaam,
                                  style: SizeScaler.getResponsiveTextStyle(
                                      context,
                                      18,
                                      FontWeight.bold,
                                      Colors.white),
                                ),
                                subtitle: Text(
                                  'Categorie: ${product.categorie}',
                                  style: SizeScaler.getResponsiveTextStyle(
                                      context,
                                      16,
                                      FontWeight.normal,
                                      Colors.white),
                                ),
                              ),
                            ),
                          ),
                        );
                      },
                    ),
                  ),
                );
              } else if (snapshot.hasError) {
                return Center(child: Text("${snapshot.error}"));
              } else {
                return const Center(child: CircularProgressIndicator());
              }
            },
          ),
        ],
      ),
    );
  }
}

class PhoneHomeScreen extends StatelessWidget {
  final double screenWidth;
  const PhoneHomeScreen({super.key, required this.screenWidth});

  @override
  Widget build(BuildContext context) {
    return Expanded(
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
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
                      child: Text("Keuzegids",
                          style: SizeScaler.getResponsiveTextStyle(
                              context, 20, FontWeight.bold, Colors.white)),
                    ),
                  ),
                ),
              ),
            ),
          ),
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
                      child: Text("Technologie-catalogus",
                          style: SizeScaler.getResponsiveTextStyle(
                              context, 20, FontWeight.bold, Colors.white)),
                    ),
                  ),
                ),
              ),
            ),
          ),
          Padding(
            padding: EdgeInsets.only(left: screenWidth * 0.03, top: 15),
            child: Text(
              "Nieuwste producten:",
              style: SizeScaler.getResponsiveTextStyle(
                  context, 22, FontWeight.bold, Colors.black),
            ),
          ),
          FutureBuilder<List<Product>>(
            future: ApiCall().newestProducts(),
            builder: (context, snapshot) {
              if (snapshot.hasData) {
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
                                  product.productNaam,
                                  style: SizeScaler.getResponsiveTextStyle(
                                      context,
                                      18,
                                      FontWeight.bold,
                                      Colors.white),
                                ),
                                subtitle: Text(
                                  'Categorie: ${product.categorie}',
                                  style: SizeScaler.getResponsiveTextStyle(
                                      context,
                                      17,
                                      FontWeight.normal,
                                      Colors.white),
                                ),
                                trailing: SingleProductView(
                                  product: product,
                                )),
                          ),
                        ),
                      );
                    },
                  ),
                );
              } else if (snapshot.hasError) {
                return Center(child: Text("${snapshot.error}"));
              } else {
                return const Center(child: CircularProgressIndicator());
              }
            },
          ),
        ],
      ),
    );
  }
}
