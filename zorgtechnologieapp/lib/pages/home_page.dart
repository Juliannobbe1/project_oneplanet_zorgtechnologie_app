import 'package:flutter/material.dart';
import 'package:zorgtechnologieapp/pages/client_overview_page.dart';

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
              //button to keuzegids
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
                              builder: (context) =>
                                  const ClientOverview(), //const SelectionGuidePage(),
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

              //button to catalogus
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
                            // Navigator.of(context).push(MaterialPageRoute(
                            //   builder: (context) => const ProductPage(),
                            // ));
                            // DataAPI().createClient(61, 'Test 8');
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

          //newest products
          Padding(
            padding: EdgeInsets.only(
                left: screenWidth * 0.025, top: screenWidth * 0.05),
            child: Text(
              "Nieuwste producten: $screenHeight",
              style: SizeScaler.getResponsiveTextStyle(
                  context, 21, FontWeight.bold, Colors.black),
            ),
          ),
          FutureDataWidget(
              fetchData: DataAPI().newestProducts(),
              countRow: 2,
              widgetType: FutureWidgetType.gridView,
              dataType: FutureDataType.product),
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
          // DataAPI().buildListFutureBuilder(DataAPI().newestProducts()),
          FutureBuilder<List<Product>>(
            future: DataAPI().newestProducts(),
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
                                product.naam,
                                style: SizeScaler.getResponsiveTextStyle(
                                    context, 18, FontWeight.bold, Colors.white),
                              ),
                              // subtitle: Text(
                              //   'Beschrijving: ${product.beschrijving}',
                              //   style: SizeScaler.getResponsiveTextStyle(
                              //       context,
                              //       17,
                              //       FontWeight.normal,
                              //       Colors.white),
                              // ),
                              trailing: SingleProductView(
                                productId: product.iD,
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
