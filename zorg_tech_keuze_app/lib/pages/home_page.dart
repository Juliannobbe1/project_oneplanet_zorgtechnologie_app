import 'package:flutter/material.dart';
import 'package:zorg_tech_keuze_app/handlers/get_products.dart';
import 'package:zorg_tech_keuze_app/handlers/responsive_layout_handler.dart';
import 'package:zorg_tech_keuze_app/models/products.dart';
import 'package:zorg_tech_keuze_app/pages/products_page.dart';

class HomePage extends StatelessWidget {
  const HomePage({super.key});

  @override
  Widget build(BuildContext context) {
    final TextStyle standardTextSize = SizeScaler.getResponsiveTextStyle(
        context, 20, FontWeight.bold, Colors.white);
    final TextStyle titleTextSize = SizeScaler.getResponsiveTextStyle(
        context, 25, FontWeight.bold, Colors.white);
    final deviceType = ResponsiveLayout.getDeviceType(context);
    double screenWidth = MediaQuery.of(context).size.width;

    return Scaffold(
      backgroundColor: const Color.fromRGBO(231, 235, 244, 1),
      appBar: AppBar(
        leading: const Icon(Icons.menu),
        title: Text(
          "Welkom terug $deviceType",
          style: titleTextSize,
        ),
      ),
      body: Column(
        children: [
          if (deviceType == DeviceType.tablet ||
              deviceType == DeviceType.desktop ||
              screenWidth >= 500) ...[
            TabletScreen(
              standardTextSize: standardTextSize,
              titleTextSize: titleTextSize,
              screenWidth: screenWidth,
            )
          ] else ...[
            PhoneScreen(
                standardTextSize: standardTextSize,
                titleTextSize: titleTextSize,
                screenWidth: screenWidth)
          ]
        ],
      ),
    );
  }
}

class TabletScreen extends StatelessWidget {
  final TextStyle standardTextSize;
  final TextStyle titleTextSize;
  final double screenWidth;

  const TabletScreen({
    Key? key,
    required this.standardTextSize,
    required this.titleTextSize,
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
                              builder: (context) => const ProductPage(),
                            ));
                          },
                          child: Text(
                            "Keuzegids",
                            style: standardTextSize,
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
                            style: standardTextSize,
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
            padding: EdgeInsets.only(left: screenWidth * 0.03, top: 75),
            child: Text(
              "Nieuwste producten:",
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
                    height: 400, // Specify the desired height for the ListView
                    child: GridView.builder(
                      gridDelegate:
                          const SliverGridDelegateWithFixedCrossAxisCount(
                        crossAxisCount: 2, // Number of columns in the grid
                        childAspectRatio:
                            4, // Width to height ratio of each grid item
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

class PhoneScreen extends StatelessWidget {
  final TextStyle standardTextSize;
  final TextStyle titleTextSize;
  final double screenWidth;
  const PhoneScreen(
      {super.key,
      required this.standardTextSize,
      required this.titleTextSize,
      required this.screenWidth});

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
                      style: TextButton.styleFrom(
                          // fixedSize: const Size(300, 100),
                          ),
                      onPressed: () {
                        Navigator.of(context).push(MaterialPageRoute(
                            builder: (context) => const ProductPage()));
                      },
                      child: Text("Keuzegids", style: standardTextSize),
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
                          style: standardTextSize),
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
                  context, 21, FontWeight.bold, Colors.black),
            ),
          ),

          // comment section & recommended videos
          FutureBuilder<List<Product>>(
            future: ApiCall().newestProducts(),
            builder: (context, snapshot) {
              if (snapshot.hasData) {
                final products = snapshot.data!;
                return SizedBox(
                  height: 325, // Specify the desired height for the ListView
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
                                    context, 20, FontWeight.bold, Colors.white),
                              ),
                              subtitle: Text(
                                'Categorie: ${product.categorie}',
                                style: SizeScaler.getResponsiveTextStyle(
                                    context,
                                    18,
                                    FontWeight.normal,
                                    Colors.white),
                              ),
                            ),
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
