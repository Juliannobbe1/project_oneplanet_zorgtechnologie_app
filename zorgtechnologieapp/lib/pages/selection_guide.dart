import 'package:auto_size_text/auto_size_text.dart';
import 'package:flutter/material.dart';
import 'package:zorgtechnologieapp/widgets/futurebuilder.dart';

import '../handlers/data_api_handler.dart';
import '../handlers/responsive_layout_handler.dart';
import '../models/products.dart';

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
  String? selectedProbleem;

  void handleItemSelected(String? item) {
    setState(() {
      selectedProbleem = item;
    });
  }

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
                        mainAxisAlignment: MainAxisAlignment.start,
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
                          Expanded(
                            child: FutureDataWidget(
                              fetchData: DataAPI().distinctProbleem,
                              widgetType: FutureWidgetType.selectableList,
                            ),
                          ),
                        ],
                      ),
                    ),
                  ),
                ),
              ),

              //results container
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
                                // final filteredProducts = selectedProbleem !=
                                //         null
                                //     ? products
                                //         .where((product) =>
                                //             product.iD ==
                                //             selectedProbleem) // Filter products based on selected item
                                //         .toList()
                                //     : products;

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

  //local method
  // FutureBuilder<List<Toepassing>> listToepassing() {
  //   return FutureBuilder<List<Toepassing>>(
  //     future: DataAPI().distinctToepassing(),
  //     builder: (context, snapshot) {
  //       if (snapshot.hasData) {
  //         final toepassingen = snapshot.data!;
  //         final limitedToepassingen =
  //             toepassingen.take(5).toList(); // Limit to 5 items
  //         return SelectableList<Toepassing, String?>(
  //           items: limitedToepassingen,
  //           itemBuilder: (context, toepassing, selected, onTap) => Card(
  //             elevation: 2.0,
  //             shape: RoundedRectangleBorder(
  //               borderRadius: BorderRadius.circular(
  //                   10.0), // Set the border radius to make the edges round
  //             ),
  //             color: Colors.blue[100],
  //             child: ListTile(
  //               title: Text(toepassing.toepassing),
  //               selected: selected,
  //               onTap: onTap,
  //             ),
  //           ),
  //           valueSelector: (toepassing) => toepassing.toepassing,
  //           selectedValue: selectedToepassing,
  //           onItemSelected: (toepassing) {
  //             setState(() {
  //               selectedToepassing =
  //                   toepassing.toepassing; // Assign selected item
  //             });
  //           },
  //           onItemDeselected: (toepassing) {
  //             setState(() {
  //               selectedToepassing = null; // Deselect the item
  //             });
  //           },
  //         );
  //       } else if (snapshot.hasError) {
  //         return Center(child: Text("${snapshot.error}"));
  //       } else {
  //         return const Center(child: CircularProgressIndicator());
  //       }
  //     },
  //   );
  // }

  // FutureBuilder<List<Product>> listProducts() {
  //   return FutureBuilder<List<Product>>(
  //     future: DataAPI().newestProducts(),
  //     builder: (context, snapshot) {
  //       if (snapshot.hasData) {
  //         final product = snapshot.data!;
  //         final limitedProduct = product.take(5).toList(); // Limit to 5 items
  //         return SelectableList<Product, String?>(
  //           items: limitedProduct,
  //           itemBuilder: (context, product, selected, onTap) => Card(
  //             elevation: 2.0,
  //             shape: RoundedRectangleBorder(
  //               borderRadius: BorderRadius.circular(
  //                   10.0), // Set the border radius to make the edges round
  //             ),
  //             color: Colors.white70,
  //             child: ListTile(
  //               title: Text(product.naam),
  //               selected: selected,
  //               onTap: onTap,
  //             ),
  //           ),
  //           valueSelector: (product) => product.naam,
  //           selectedValue: selectedProduct,
  //           onItemSelected: (product) {
  //             setState(() {
  //               selectedProduct = product.naam; // Assign selected item
  //             });
  //           },
  //           onItemDeselected: (product) {
  //             setState(() {
  //               selectedProduct = null; // Deselect the item
  //             });
  //           },
  //         );
  //       } else if (snapshot.hasError) {
  //         return Center(child: Text("${snapshot.error}"));
  //       } else {
  //         return const Center(child: CircularProgressIndicator());
  //       }
  //     },
  //   );
  // }

  // FutureBuilder<List<Toepassing>> toepassingList() {
  //   return FutureBuilder<List<Toepassing>>(
  //     future: DataAPI().distinctToepassing(),
  //     builder: (context, snapshot) {
  //       if (snapshot.hasData) {
  //         final toepassingen = snapshot.data!;
  //         final limitedToepassingen =
  //             toepassingen.take(5).toList(); // Limit to 5 items
  //         return SelectableList<Toepassing, String?>(
  //           items: limitedToepassingen,
  //           itemBuilder: (context, toepassing, selected, onTap) => ListTile(
  //             title: Text(toepassing.toepassing),
  //             selected: selected,
  //             onTap: onTap,
  //           ),
  //           valueSelector: (toepassing) => toepassing.toepassing,
  //           selectedValue: selectedToepassing,
  //           onItemSelected: (toepassing) {
  //             setState(() {
  //               selectedToepassing =
  //                   toepassing.toepassing; // Assign selected item
  //             });
  //           },
  //           onItemDeselected: (toepassing) {
  //             setState(() {
  //               selectedToepassing = null; // Deselect the item
  //             });
  //           },
  //         );
  //       } else if (snapshot.hasError) {
  //         return Center(child: Text("${snapshot.error}"));
  //       } else {
  //         return const Center(child: CircularProgressIndicator());
  //       }
  //     },
  //   );
  // }
}

class PhoneSelectionScreen extends StatefulWidget {
  final double screenWidth;
  final double screenHeight;
  const PhoneSelectionScreen(
      {super.key, required this.screenWidth, required this.screenHeight});

  @override
  State<PhoneSelectionScreen> createState() => _PhoneSelectionScreenState();
}

class _PhoneSelectionScreenState extends State<PhoneSelectionScreen> {
  String? selectedToepassing;

  @override
  Widget build(BuildContext context) {
    final screenWidth = widget.screenWidth;
    final screenHeight = widget.screenHeight;
    return Expanded(
      flex: 1,
      child: Padding(
        padding: EdgeInsets.fromLTRB(screenWidth * 0.05, screenHeight * 0.025,
            screenWidth * 0.05, screenHeight * 0.025),
        child: Card(
          elevation: 5,
          shape:
              RoundedRectangleBorder(borderRadius: BorderRadius.circular(10)),
          color: Colors.blue[200],
          child: Column(
            children: [
              SizedBox(
                height: screenHeight * 0.05,
              ),
              const Padding(
                padding: EdgeInsets.only(left: 10.0, right: 10),
                child: AutoSizeText(
                  "Selecteer de zorgbehoeften van uw cliënt",
                  maxFontSize: 25,
                  minFontSize: 17,
                  style: TextStyle(fontWeight: FontWeight.bold),
                  // style: SizeScaler.getResponsiveTextStyle(
                  //     context, 15, FontWeight.bold, Colors.black),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}





// class PhoneSelectionScreenold extends StatelessWidget {
//   final double screenWidth;
//   final double screenHeight;
//   const PhoneSelectionScreenold(
//       {super.key, required this.screenWidth, required this.screenHeight});

//   @override
//   Widget build(BuildContext context) {
//     return Padding(
//       padding: const EdgeInsets.all(20.0),
//       child: SizedBox(
//         height: screenHeight * 0.85,
//         child: Expanded(
//           flex: 1,
//           child: Container(
//             height: screenHeight * 0.75,
//             color: Colors.transparent,
//             child: Padding(
//               padding: const EdgeInsets.all(10.0),
//               child: Card(
//                 elevation: 5,
//                 shape: RoundedRectangleBorder(
//                     borderRadius: BorderRadius.circular(10)),
//                 color: Colors.blue[200],
//                 child: Column(
//                   children: [
//                     SizedBox(
//                       height: screenHeight * 0.05,
//                     ),
//                     Padding(
//                       padding: const EdgeInsets.only(left: 10.0, right: 10),
//                       child: Text(
//                         "Selecteer de zorgbehoeften van uw cliënt",
//                         style: SizeScaler.getResponsiveTextStyle(
//                             context, 15, FontWeight.bold, Colors.black),
//                       ),
//                     ),
//                     FutureBuilder<List<Toepassing>>(
//                       future: DataAPI().distinctToepassing(),
//                       builder: (context, snapshot) {
//                         if (snapshot.hasData) {
//                           final toepassingen = snapshot.data!;
//                           final limitedToepassingen =
//                               toepassingen.take(5).toList(); // Limit to 5 items
//                           return SelectableList<Toepassing, String?>(
//                             items: limitedToepassingen,
//                             itemBuilder:
//                                 (context, toepassing, selected, onTap) =>
//                                     ListTile(
//                               title: Text(toepassing.toepassing),
//                               selected: selected,
//                               onTap: onTap,
//                             ),
//                             valueSelector: (toepassing) =>
//                                 toepassing.toepassing,
//                             selectedValue: selectedToepassing,
//                             onItemSelected: (toepassing) {
//                               setState(() {
//                                 selectedToepassing = toepassing
//                                     .toepassing; // Assign selected item
//                               });
//                             },
//                             onItemDeselected: (toepassing) {
//                               setState(() {
//                                 selectedToepassing = null; // Deselect the item
//                               });
//                             },
//                           );
//                         } else if (snapshot.hasError) {
//                           return Center(child: Text("${snapshot.error}"));
//                         } else {
//                           return const Center(
//                               child: CircularProgressIndicator());
//                         }
//                       },
//                     ),
//                   ],
//                 ),
//               ),
//             ),
//           ),
//         ),
//       ),
//     );
//   }
// }
