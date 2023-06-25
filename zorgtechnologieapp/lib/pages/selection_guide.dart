import 'package:auto_size_text/auto_size_text.dart';
import 'package:flutter/material.dart';
import 'package:zorgtechnologieapp/widgets/futurebuilder.dart';
import 'package:uuid/uuid.dart';

import '../handlers/data_api_handler.dart';
import '../handlers/responsive_layout_handler.dart';

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
  var uuid = const Uuid();
  int selectedBehoefteIndex = -1;
  String? zorgbehoefte;
  String? clientID;

  void handleZorgbehoefteSelected(int index, String item) async {
    // final client = await DataAPI().latestClient();
    var v4 = uuid.v4();
    setState(() {
      // latestClient = client[0].iD;
      clientID = v4;
      selectedBehoefteIndex = index;
      zorgbehoefte = item;
    });
    DataAPI().createClient(v4, zorgbehoefte!);
    DataAPI()
        .createClientRelationship(v4, "e040d519-dcc5-4969-86c3-54006f21656c");
  }

  void handle2ItemSelected(int index, String item) {
    setState(() {
      selectedBehoefteIndex = index;
      zorgbehoefte = item;
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
                          SizedBox(
                            height: selectedBehoefteIndex == -1 ? 500 : 80,
                            child: FutureDataWidget(
                              fetchData: DataAPI().distinctProbleem(),
                              widgetType: FutureWidgetType.selectableList,
                              dataType: FutureDataType.probleemSelect,
                              onItemSelected: handleZorgbehoefteSelected,
                            ),
                          ),
                          //! change to right selectable
                          // selectedBehoefteIndex != -1
                          //     ? Column(
                          //         children: [
                          //           // DataAPI().createClient(id, probleem),
                          //           Padding(
                          //             padding: const EdgeInsets.only(
                          //                 left: 10, right: 10),
                          //             child: Text(
                          //               "Selecteer de zorgbehoeften van uw cliënt",
                          //               style:
                          //                   SizeScaler.getResponsiveTextStyle(
                          //                       context,
                          //                       15,
                          //                       FontWeight.bold,
                          //                       Colors.black),
                          //             ),
                          //           ),
                          //           SizedBox(
                          //             height: 375,
                          //             child: FutureDataWidget(
                          //               fetchData:
                          //                   DataAPI().distinctToepassing(),
                          //               widgetType:
                          //                   FutureWidgetType.selectableList,
                          //               dataType:
                          //                   FutureDataType.toepassingSelect,
                          //               onItemSelected: (int selectedItemIndex,
                          //                   String item) {},
                          //             ),
                          //           ),
                          //         ],
                          //       )
                          //     : Container(),
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
                            "Resultaat",
                            style: SizeScaler.getResponsiveTextStyle(
                                context, 20, FontWeight.bold, Colors.black),
                          ),

                          // ! Replace with algorithme function

                          selectedBehoefteIndex != -1
                              ? //Text('$latestClient')
                              FutureDataWidget(
                                  fetchData: DataAPI().recommendedProducts(
                                      "e040d519-dcc5-4969-86c3-54006f21656c",
                                      clientID!),
                                  widgetType: FutureWidgetType.gridView,
                                  dataType: FutureDataType.product,
                                  countRow: 1,
                                )
                              : Container()
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
