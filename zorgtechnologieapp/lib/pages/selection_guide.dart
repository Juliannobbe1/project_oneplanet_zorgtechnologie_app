import 'package:flutter/material.dart';
import 'package:zorgtechnologieapp/models/toepassing.dart';

import '../handlers/data_api_handler.dart';
import '../handlers/responsive_layout_handler.dart';
import '../models/products.dart';
import 'package:selectable_list/selectable_list.dart';

class SelectionGuidePage extends StatelessWidget {
  const SelectionGuidePage({super.key});

  @override
  Widget build(BuildContext context) {
    final deviceType = ResponsiveLayout.getDeviceType(context);
    double screenWidth = MediaQuery.of(context).size.width;
    double screenHeight = MediaQuery.of(context).size.height;

    return Scaffold(
      backgroundColor: Colors.indigo[50],
      appBar: AppBar(
        // leading: const Icon(Icons.menu),
        title: Text(
          "$deviceType",
        ),
      ),
      body: Column(
        children: [
          if (deviceType == DeviceType.tablet ||
              deviceType == DeviceType.desktop) ...[
            TabletSelectionScreen(
              screenWidth: screenWidth,
              screenHeight: screenHeight,
            )
          ] else ...[
            PhoneSelectionScreen(
              screenWidth: screenWidth,
              screenHeight: screenHeight,
            )
          ]
        ],
      ),
    );
  }
}

class TabletSelectionScreen extends StatefulWidget {
  final double screenWidth;
  final double screenHeight;
  const TabletSelectionScreen(
      {super.key, required this.screenWidth, required this.screenHeight});

  @override
  State<TabletSelectionScreen> createState() => _TabletSelectionScreenState();
}

class _TabletSelectionScreenState extends State<TabletSelectionScreen> {
  String? selectedToepassing;

  @override
  Widget build(BuildContext context) {
    final screenWidth = widget.screenWidth;
    final screenHeight = widget.screenHeight;
    return Padding(
      padding: EdgeInsets.fromLTRB(screenWidth * 0.02, screenHeight * 0.025,
          screenWidth * 0.02, screenHeight * 0.05),
      child: Column(
        children: [
          Padding(
            padding: const EdgeInsets.fromLTRB(20.0, 5.0, 15.0, 15.0),
            child: Text(
              "Welkom bij de keuze gids. De gids zal u enkele vragen stellen om u te helpen bij het vinden van de juiste zorgtechnologie om uw cliënt bij te staan in hun zorgvraag. Selecteer een van de opties hieronder om te beginnen.",
              style: SizeScaler.getResponsiveTextStyle(
                  context, 15, FontWeight.normal, Colors.black),
            ),
          ),
          Row(
            children: [
              Expanded(
                flex: 1,
                child: Container(
                  height: screenHeight * 0.75,
                  color: Colors.transparent,
                  child: Padding(
                    padding: const EdgeInsets.all(10.0),
                    child: Card(
                      elevation: 5,
                      shape: RoundedRectangleBorder(
                          borderRadius: BorderRadius.circular(10)),
                      color: Colors.blue[200],
                      child: Column(
                        children: [
                          SizedBox(
                            height: screenHeight * 0.05,
                          ),
                          Padding(
                            padding:
                                const EdgeInsets.only(left: 10.0, right: 10),
                            child: Text(
                              "Selecteer de zorgbehoeften van uw cliënt",
                              style: SizeScaler.getResponsiveTextStyle(
                                  context, 15, FontWeight.bold, Colors.black),
                            ),
                          ),
                          FutureBuilder<List<Toepassing>>(
                            future: DataAPI().distinctToepassing(),
                            builder: (context, snapshot) {
                              if (snapshot.hasData) {
                                final toepassingen = snapshot.data!;
                                final limitedToepassingen = toepassingen
                                    .take(5)
                                    .toList(); // Limit to 5 items
                                return SelectableList<Toepassing, String?>(
                                  items: limitedToepassingen,
                                  itemBuilder:
                                      (context, toepassing, selected, onTap) =>
                                          ListTile(
                                    title: Text(toepassing.toepassing),
                                    selected: selected,
                                    onTap: onTap,
                                  ),
                                  valueSelector: (toepassing) =>
                                      toepassing.toepassing,
                                  selectedValue: selectedToepassing,
                                  onItemSelected: (toepassing) {
                                    setState(() {
                                      selectedToepassing = toepassing
                                          .toepassing; // Assign selected item
                                    });
                                  },
                                  onItemDeselected: (toepassing) {
                                    setState(() {
                                      selectedToepassing =
                                          null; // Deselect the item
                                    });
                                  },
                                );
                              } else if (snapshot.hasError) {
                                return Center(child: Text("${snapshot.error}"));
                              } else {
                                return const Center(
                                    child: CircularProgressIndicator());
                              }
                            },
                          ),
                        ],
                      ),
                    ),
                  ),
                ),
              ),
              Expanded(
                flex: 2,
                child: Container(
                  height: screenHeight * 0.75,
                  color: Colors.transparent,
                  child: Padding(
                    padding: const EdgeInsets.all(10.0),
                    child: Card(
                      elevation: 5,
                      shape: RoundedRectangleBorder(
                          borderRadius: BorderRadius.circular(10)),
                      color: Colors.blue[200],
                      child: Column(
                        children: [
                          SizedBox(
                            height: screenHeight * 0.05,
                          ),
                          Text(
                            "Results",
                            style: SizeScaler.getResponsiveTextStyle(
                                context, 20, FontWeight.bold, Colors.black),
                          ),
                          SizedBox(
                            height: screenHeight * 0.05,
                          ),
                          // ! Replace with algorithme function
                          FutureBuilder<List<Product>>(
                            future: DataAPI().getProducts(),
                            builder: (context, snapshot) {
                              if (snapshot.hasData) {
                                final products = snapshot.data!;

                                //? edit point
                                final filteredProducts = selectedToepassing !=
                                        null
                                    ? products
                                        .where((product) =>
                                            product.iD ==
                                            selectedToepassing) // Filter products based on selected item
                                        .toList()
                                    : products;

                                return SizedBox(
                                  height: 450,
                                  child: ListView.builder(
                                    itemCount: products.length,
                                    itemBuilder: (context, index) {
                                      final product = products[index];
                                      return Padding(
                                        padding: const EdgeInsets.fromLTRB(
                                            15.0, 10.0, 15.0, 10.0),
                                        child: Material(
                                          elevation: 5,
                                          borderRadius: const BorderRadius.all(
                                              Radius.circular(10)),
                                          child: Container(
                                            decoration: BoxDecoration(
                                              borderRadius:
                                                  const BorderRadius.all(
                                                Radius.circular(10),
                                              ),
                                              color: Colors.blue[500],
                                            ),
                                            child: Padding(
                                              padding: EdgeInsets.only(
                                                  top: screenHeight * 0.02,
                                                  bottom: screenHeight * 0.02,
                                                  left: screenWidth * 0.01,
                                                  right: screenWidth * 0.01),
                                              child: ListTile(
                                                title: Text(
                                                  product.naam,
                                                  style: SizeScaler
                                                      .getResponsiveTextStyle(
                                                          context,
                                                          18,
                                                          FontWeight.bold,
                                                          Colors.white),
                                                ),
                                                subtitle: Text(
                                                  product.beschrijving,
                                                  style: SizeScaler
                                                      .getResponsiveTextStyle(
                                                          context,
                                                          17,
                                                          FontWeight.normal,
                                                          Colors.white),
                                                ),
                                                // trailing: SingleProductView(
                                                //   product: product,
                                                // ),
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
                                return const Center(
                                    child: CircularProgressIndicator());
                              }
                            },
                          ),
                        ],
                      ),
                    ),
                  ),
                ),
              ),
            ],
          ),
        ],
      ),
    );
  }
}

class PhoneSelectionScreen extends StatelessWidget {
  final double screenWidth;
  final double screenHeight;
  const PhoneSelectionScreen(
      {super.key, required this.screenWidth, required this.screenHeight});

  @override
  Widget build(BuildContext context) {
    return SizedBox(
      height: screenHeight * 0.85,
      child: SingleChildScrollView(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Container(
              height: 200,
              width: double.infinity,
              color: Colors.red,
            ),
            Container(
              height: 200,
              width: double.infinity,
              color: Colors.amber,
            ),
            Container(
              height: 200,
              width: double.infinity,
              color: Colors.blue,
            ),
            Container(
              height: 200,
              width: double.infinity,
              color: Colors.red,
            ),
            Container(
              height: 200,
              width: double.infinity,
              color: Colors.amber,
            ),
            Container(
              height: 200,
              width: double.infinity,
              color: Colors.blue,
            )
          ],
        ),
      ),
    );
  }
}
