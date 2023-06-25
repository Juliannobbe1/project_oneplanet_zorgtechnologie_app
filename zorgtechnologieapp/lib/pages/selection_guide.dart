import 'dart:developer';

import 'package:auto_size_text/auto_size_text.dart';
import 'package:flutter/material.dart';
import 'package:zorgtechnologieapp/pages/home_page.dart';
import 'package:zorgtechnologieapp/widgets/futurebuilder.dart';
import 'package:uuid/uuid.dart';

import '../handlers/data_api_handler.dart';
import '../handlers/responsive_layout_handler.dart';

class SelectionGuidePage extends StatelessWidget {
  const SelectionGuidePage({super.key});

  @override
  Widget build(BuildContext context) {
    final deviceType = ResponsiveLayout.getDeviceType(
        context); // Determine the device type (tablet, desktop, or phone)
    double screenWidth =
        MediaQuery.of(context).size.width; // Get the screen width
    double screenHeight =
        MediaQuery.of(context).size.height; // Get the screen height

    return Scaffold(
      backgroundColor: Colors.indigo[50],
      appBar: AppBar(
        leading: const Icon(Icons.menu), // Display a menu icon in the app bar
        title: const Text(
          "Welkom bij de keuzegids",
        ),
      ),
      body: Column(
        children: [
          if (deviceType ==
                  DeviceType
                      .tablet || // Conditionally render the TabletSelectionScreen for tablets and desktops
              deviceType == DeviceType.desktop) ...[
            TabletSelectionScreen(
              screenWidth: screenWidth,
              screenHeight: screenHeight,
            )
          ] else ...[
            // Conditionally render the PhoneSelectionScreen for phones
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

// Widget for the tablet selection screen
class TabletSelectionScreen extends StatefulWidget {
  // Dimensions of the tablet screen
  final double screenWidth;
  final double screenHeight;

  // Constructor
  const TabletSelectionScreen({
    Key? key,
    required this.screenWidth,
    required this.screenHeight,
  }) : super(key: key);

  // Create state for the tablet selection screen
  @override
  TabletSelectionScreenState createState() => TabletSelectionScreenState();
}

class TabletSelectionScreenState extends State<TabletSelectionScreen> {
  var uuid = const Uuid(); // Uuid generator instance
  var api = DataAPI(); // DataAPI instance
  int selectedBehoefteIndex = -1; // Index of the selected zorgbehoefte
  int selectedProductIndex = -1; // Index of the selected product
  String? product; // Selected product
  String? zorgbehoefte; // Selected zorgbehoefte
  String? clientID; // Client ID

  // Callback function when a zorgbehoefte is selected
  void handleZorgbehoefteSelected(int index, String item) async {
    var v4 = uuid.v4(); // Generate a unique client ID using Uuid
    setState(() {
      clientID = v4; // Update the client ID
      selectedBehoefteIndex = index; // Update the selected zorgbehoefte index
      zorgbehoefte = item; // Update the selected zorgbehoefte
    });
  }

  // Callback function when a product is selected
  void handleProductSelected(int index, String item) async {
    setState(() {
      selectedBehoefteIndex = index; // Update the selected zorgbehoefte index
      product = item; // Update the selected product
    });
  }

  @override
  Widget build(BuildContext context) {
    final screenWidth = widget.screenWidth; // Get the screen width
    final screenHeight = widget.screenHeight; // Get the screen height

    return Padding(
      padding: EdgeInsets.fromLTRB(
        screenWidth * 0.02, // Set left padding based on the screen width
        screenHeight * 0.025, // Set top padding based on the screen height
        screenWidth * 0.02, // Set right padding based on the screen width
        screenHeight * 0.05, // Set bottom padding based on the screen height
      ),
      child: Column(
        children: [
          // Welcome text
          Padding(
            padding: const EdgeInsets.fromLTRB(20.0, 5.0, 15.0, 15.0),
            child: Text(
              "Welcome to the choice guide. The guide will ask you some questions to help you find the right care technology to assist your client with their care needs. Select one of the options below to get started.",
              style: SizeScaler.getResponsiveTextStyle(
                context,
                15,
                FontWeight.normal,
                Colors.black,
              ),
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
                        borderRadius: BorderRadius.circular(10),
                      ),
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
                              "Select the care needs of your client",
                              style: SizeScaler.getResponsiveTextStyle(
                                context,
                                15,
                                FontWeight.bold,
                                Colors.black,
                              ),
                            ),
                          ),
                          SizedBox(
                            height: selectedBehoefteIndex == -1 ? 500 : 80,
                            child: FutureDataWidget(
                              fetchData: api.distinctProbleem(),
                              widgetType: FutureWidgetType.selectableList,
                              dataType: FutureDataType.probleemSelect,
                              onItemSelected: handleZorgbehoefteSelected,
                            ),
                          ),
                        ],
                      ),
                    ),
                  ),
                ),
              ),

              // Results container
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
                        borderRadius: BorderRadius.circular(10),
                      ),
                      color: Colors.blue[200],
                      child: Column(
                        children: [
                          SizedBox(
                            height: screenHeight * 0.05,
                          ),
                          Text(
                            "Result",
                            style: SizeScaler.getResponsiveTextStyle(
                              context,
                              20,
                              FontWeight.bold,
                              Colors.black,
                            ),
                          ),
                          selectedBehoefteIndex != -1
                              ? Expanded(
                                  flex: 6,
                                  child: FutureDataWidget(
                                    fetchData: api.recommendedProducts(
                                      "e040d519-dcc5-4969-86c3-54006f21656c",
                                      zorgbehoefte!,
                                    ),
                                    widgetType: FutureWidgetType.selectableList,
                                    dataType: FutureDataType.recommendProduct,
                                    onItemSelected: handleProductSelected,
                                  ),
                                )
                              : Container(
                                  height: screenHeight * 0.55,
                                ),
                          Expanded(
                            child: Row(
                              children: [
                                Expanded(
                                  flex: 1,
                                  child: Padding(
                                    padding: const EdgeInsets.all(10.0),
                                    child: Align(
                                      alignment: Alignment.bottomRight,
                                      child: FloatingActionButton.extended(
                                        onPressed: () {
                                          // Save function
                                          if (zorgbehoefte != null &&
                                              product != null) {
                                            Navigator.of(context).push(
                                              MaterialPageRoute(
                                                builder: (context) =>
                                                    const HomePage(),
                                              ),
                                            );

                                            api.createClient(
                                              clientID!,
                                              zorgbehoefte!,
                                            );
                                            api.createClientRelationship(
                                              clientID!,
                                              "e040d519-dcc5-4969-86c3-54006f21656c",
                                            );
                                            api.createRecommendationRelationship(
                                              clientID!,
                                              "e040d519-dcc5-4969-86c3-54006f21656c",
                                              product!,
                                            );
                                          } else {
                                            log("test"); // Log a test message
                                          }
                                        },
                                        icon: const Icon(Icons.save),
                                        label: const Text("Save"),
                                        backgroundColor:
                                            Colors.greenAccent[700],
                                      ),
                                    ),
                                  ),
                                ),
                                Padding(
                                  padding: const EdgeInsets.all(10.0),
                                  child: Align(
                                    alignment: Alignment.bottomRight,
                                    child: FloatingActionButton.extended(
                                      onPressed: () {
                                        Navigator.of(context).push(
                                          MaterialPageRoute(
                                            builder: (context) =>
                                                const HomePage(),
                                          ),
                                        );
                                      },
                                      icon: const Icon(Icons.exit_to_app),
                                      label: const Text("Stop"),
                                      backgroundColor: Colors.redAccent[700],
                                    ),
                                  ),
                                ),
                              ],
                            ),
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

class PhoneSelectionScreen extends StatefulWidget {
  final double screenWidth;
  final double screenHeight;
  const PhoneSelectionScreen(
      {super.key, required this.screenWidth, required this.screenHeight});

  @override
  State<PhoneSelectionScreen> createState() => _PhoneSelectionScreenState();
}

class _PhoneSelectionScreenState extends State<PhoneSelectionScreen> {
  String? selectedToepassing; // Selected application

  @override
  Widget build(BuildContext context) {
    final screenWidth = widget.screenWidth; // Get the screen width
    final screenHeight = widget.screenHeight; // Get the screen height

    return Expanded(
      flex: 1,
      child: Padding(
        padding: EdgeInsets.fromLTRB(
          screenWidth * 0.05, // Set left padding based on screen width
          screenHeight * 0.025, // Set top padding based on screen height
          screenWidth * 0.05, // Set right padding based on screen width
          screenHeight * 0.025, // Set bottom padding based on screen height
        ),
        child: Card(
          elevation: 5,
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(10),
          ),
          color: Colors.blue[200],
          child: Column(
            children: [
              SizedBox(
                height: screenHeight * 0.05,
              ),
              const Padding(
                padding: EdgeInsets.only(left: 10.0, right: 10),
                child: AutoSizeText(
                  "Selecteer de zorgbehoeften van uw cliënt", // Select the care needs of your client
                  maxFontSize: 25,
                  minFontSize: 17,
                  style: TextStyle(fontWeight: FontWeight.bold),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
