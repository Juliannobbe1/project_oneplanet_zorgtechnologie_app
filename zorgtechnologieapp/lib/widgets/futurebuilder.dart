import 'package:flutter/material.dart';
import 'package:zorgtechnologieapp/models/clients.dart';
import '../handlers/responsive_layout_handler.dart';
import '../models/products.dart';
import '../pages/products_page.dart';

typedef DataFetcher = Future<List<dynamic>> Function();

enum FutureWidgetType { selectableList, gridView }

class FutureDataWidget extends StatefulWidget {
  final DataFetcher fetchData;
  final int? countRow;
  final FutureWidgetType widgetType;

  const FutureDataWidget(
      {Key? key,
      required this.fetchData,
      this.countRow,
      required this.widgetType})
      : super(key: key);

  @override
  FutureDataWidgetState createState() => FutureDataWidgetState();
}

class FutureDataWidgetState extends State<FutureDataWidget> {
  late Future<List<dynamic>> _dataFuture;
  late int countRow;
  late FutureWidgetType widgetType;

  @override
  void initState() {
    super.initState();
    _dataFuture = widget.fetchData();
    widgetType = widget.widgetType;
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
            return gridBuildWidget(context, dataList, countRow); //, countRow);
          } else {
            return selectableListWidget(context, dataList);
          }
        }
      },
    );
  }

  Widget selectableListWidget(BuildContext context, List<dynamic> dataList) {
    return ListView.builder(
      itemCount: dataList.length,
      itemBuilder: (context, index) {
        final data = dataList[index];

        if (selectedItemIndex != -1 && selectedItemIndex != index) {
          return Container(); // Return an empty container to hide the non-selected items
        }

        return Padding(
          padding: const EdgeInsets.all(10.0),
          child: probleemSelectTile(data, index),
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
              } else {
                selectedItemIndex = index; // Select the item
              }
            });
          },
        ),
      ),
    );
  }

  Widget gridBuildWidget(
      BuildContext context, List<dynamic> dataList, int count) {
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
          if (data is Product) {
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
                    child: productListTile(
                      data,
                    )),
              ),
            );
          }
          return null;
        },
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
}
