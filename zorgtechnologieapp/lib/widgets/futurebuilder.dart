import 'package:flutter/material.dart';
import 'package:zorgtechnologieapp/models/clients.dart';
import 'package:zorgtechnologieapp/models/toepassing.dart';
import '../handlers/responsive_layout_handler.dart';
import '../models/products.dart';
import '../pages/products_page.dart';
// import '../pages/selection_guide.dart';

// typedef DataFetcher = Future<List<dynamic>> Function();
typedef SelectedItemCallback = void Function(
    int selectedItemIndex, String item);

enum FutureWidgetType { selectableList, gridView }

enum FutureDataType { product, probleemSelect, toepassingSelect, clients }

class FutureDataWidget extends StatefulWidget {
  final Future<List<dynamic>> fetchData;
  final int? countRow;
  final FutureWidgetType widgetType;
  final FutureDataType dataType;
  final SelectedItemCallback? onItemSelected;

  const FutureDataWidget(
      {Key? key,
      required this.fetchData,
      this.countRow,
      required this.widgetType,
      required this.dataType,
      this.onItemSelected})
      : super(key: key);

  @override
  FutureDataWidgetState createState() => FutureDataWidgetState();
}

class FutureDataWidgetState extends State<FutureDataWidget> {
  late Future<List<dynamic>> _dataFuture;
  late int countRow;
  late FutureWidgetType widgetType;
  late FutureDataType dataType;

  @override
  void initState() {
    super.initState();
    _dataFuture = widget.fetchData;
    widgetType = widget.widgetType;
    dataType = widget.dataType;
  }

  int selectedItemIndex = -1;

  @override
  Widget build(BuildContext context) {
    return FutureBuilder<List<dynamic>>(
      future: _dataFuture,
      builder: (context, snapshot) {
        if (snapshot.connectionState == ConnectionState.waiting) {
          return const CircularProgressIndicator();
        } else if (snapshot.hasError) {
          return Text('Error: ${snapshot.error}');
        } else {
          final dataList = snapshot.data!;

          if (widgetType == FutureWidgetType.gridView) {
            countRow = widget.countRow!;
            return gridBuildWidget(context, dataList, countRow, dataType);
          } else {
            return selectableListWidget(
                context, dataList, selectedItemIndex, dataType);
          }
        }
      },
    );
  }

  Widget selectableListWidget(BuildContext context, List<dynamic> dataList,
      int selectedItemIndex, FutureDataType dataType) {
    return ListView.builder(
      itemCount: dataList.length,
      itemBuilder: (context, index) {
        final data = dataList[index];

        if (selectedItemIndex != -1 && selectedItemIndex != index) {
          return Container(); // Return an empty container to hide the non-selected items
        }

        return Padding(
          padding: const EdgeInsets.all(10.0),
          child: dataType == FutureDataType.probleemSelect
              ? probleemSelectTile(data, index)
              : dataType == FutureDataType.toepassingSelect
                  ? toepassingSelectTile(data, index)
                  : dataType == FutureDataType.clients
                      ? clientSelectTile(data, index)
                      : Container(), // Replace 'null' with an empty Container widget
        );
      },
    );
  }

  Widget probleemSelectTile(Clients client, int index) {
    return Material(
      elevation: 10,
      borderRadius: BorderRadius.circular(10),
      child: Ink(
        decoration: BoxDecoration(
          borderRadius: BorderRadius.circular(10),
          color: selectedItemIndex == index ? Colors.blue : Colors.blue[100],
        ),
        child: ListTile(
          title: Text(
            client.probleem,
            style: SizeScaler.getResponsiveTextStyle(
              context,
              14,
              FontWeight.bold,
              selectedItemIndex == index ? Colors.white : Colors.black,
            ),
          ),
          onTap: () {
            setState(() {
              if (selectedItemIndex == index) {
                selectedItemIndex = -1; // Deselect the item
                widget.onItemSelected!(-1, "");
              } else {
                selectedItemIndex = index; // Select the item
                widget.onItemSelected!(index, client.probleem);
              }
            });
          },
        ),
      ),
    );
  }

  Widget clientSelectTile(Clients client, int index) {
    return Material(
      elevation: 10,
      borderRadius: BorderRadius.circular(10),
      child: Ink(
        decoration: BoxDecoration(
          borderRadius: BorderRadius.circular(10),
          color: selectedItemIndex == index ? Colors.blue : Colors.blue[100],
        ),
        child: ListTile(
          leading: Text(
            'Client: ${client.iD}',
            style: SizeScaler.getResponsiveTextStyle(
                context, 18, FontWeight.bold, Colors.black),
          ),
          title: Text(
            "Probleem: ${client.probleem}",
            style: SizeScaler.getResponsiveTextStyle(
                context, 18, FontWeight.bold, Colors.black),
          ),
          contentPadding: const EdgeInsets.all(20),
          subtitle: Text(
            'Maakt gebruik van: ',
            style: SizeScaler.getResponsiveTextStyle(
                context, 18, FontWeight.bold, Colors.black),
          ),
          onTap: () {
            // Navigator.of(context).push(MaterialPageRoute(
            //   builder: (context) =>
            //       const SelectionGuidePage(),
            // ));
          },
        ),
      ),
    );
  }

  Widget toepassingSelectTile(Toepassing toepassing, int index) {
    return Material(
      elevation: 10,
      borderRadius: BorderRadius.circular(10),
      child: Ink(
        decoration: BoxDecoration(
          borderRadius: BorderRadius.circular(10),
          color: selectedItemIndex == index ? Colors.blue : Colors.blue[100],
        ),
        child: ListTile(
          title: Text(
            toepassing.toepassing,
            style: SizeScaler.getResponsiveTextStyle(
              context,
              14,
              FontWeight.bold,
              selectedItemIndex == index ? Colors.white : Colors.black,
            ),
          ),
          onTap: () {
            setState(() {
              if (selectedItemIndex == index) {
                selectedItemIndex = -1; // Deselect the item
              } else {
                selectedItemIndex = index; // Select the item
              }
            });
          },
        ),
      ),
    );
  }

  Widget gridBuildWidget(BuildContext context, List<dynamic> dataList,
      int count, FutureDataType dataType) {
    // double screenWidth = MediaQuery.of(context).size.width;
    double screenHeight = MediaQuery.of(context).size.height;
    return Expanded(
      child: GridView.builder(
          gridDelegate: SliverGridDelegateWithFixedCrossAxisCount(
            crossAxisCount: count, //count, // Number of columns in the grid
            childAspectRatio: screenHeight > 900
                ? 3.5
                : 4.5, // Width to height ratio of each grid item
          ),
          itemCount: dataList.length,
          itemBuilder: (context, index) {
            final data = dataList[index];
            // if (data is Product) {
            return Padding(
              padding: const EdgeInsets.fromLTRB(20, 25, 20, 5),
              child: Material(
                elevation: 10,
                borderRadius: const BorderRadius.all(Radius.circular(10)),
                child: Container(
                    decoration: BoxDecoration(
                      borderRadius: const BorderRadius.all(
                        Radius.circular(10),
                      ),
                      color: Colors.blue[500],
                    ),
                    child: dataType == FutureDataType.product
                        ? productListTile(data)
                        : clientsListTile(data)),
              ),
            );
          }
          // return null;
          // },
          ),
    );
  }

  //generate for each tile what needs to be on the tile
  Widget productListTile(Product product) {
    return ListTile(
      title: Text(
        product.naam,
        style: SizeScaler.getResponsiveTextStyle(
            context, 18, FontWeight.bold, Colors.white),
      ),
      trailing: SingleProductView(
        productId: product.iD,
      ),
    );
  }

  Widget clientsListTile(Clients client) {
    return ListTile(
      leading: Text(
        'Client: ${client.iD}',
        style: SizeScaler.getResponsiveTextStyle(
            context, 18, FontWeight.bold, Colors.white),
      ),
      title: Text(
        client.probleem,
        style: SizeScaler.getResponsiveTextStyle(
            context, 18, FontWeight.bold, Colors.white),
      ),
      contentPadding: const EdgeInsets.all(20),
      subtitle: Text(
        'Maakt gebruik van: ',
        style: SizeScaler.getResponsiveTextStyle(
            context, 16, FontWeight.bold, Colors.white),
      ),
    );
  }
}
