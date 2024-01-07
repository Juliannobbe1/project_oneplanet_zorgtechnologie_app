import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:logger/logger.dart';
import 'package:zorgtechnologieapp/models/clients.dart';
import 'package:zorgtechnologieapp/models/toepassing.dart';
import 'package:zorgtechnologieapp/providers/logging_provider/logging_provider.dart';
import '../handlers/data_api_handler.dart';
import '../handlers/responsive_layout_handler.dart';
import '../models/products.dart';
import '../pages/products_page.dart';

typedef SelectedItemCallback = void Function(
    int selectedItemIndex, String item);

enum FutureWidgetType {
  selectableList,
  gridView
} // Enum to represent different types of future widgets

enum FutureDataType {
  product, // Data type representing product
  probleemSelect, // Data type representing problem selection
  toepassingSelect, // Data type representing application selection
  clients, // Data type representing clients
  recommendProduct // Data type representing recommended product
}

class FutureDataWidget extends ConsumerStatefulWidget {
  final Future<List<dynamic>> fetchData; // Future that fetches data
  final int? countRow; // Number of rows
  final FutureWidgetType widgetType; // Type of future widget
  final FutureDataType dataType; // Type of future data
  final SelectedItemCallback? onItemSelected; // Callback for item selection

  const FutureDataWidget({
    super.key,
    required this.fetchData,
    this.countRow,
    required this.widgetType,
    required this.dataType,
    this.onItemSelected,
  });

  @override
  FutureDataWidgetState createState() => FutureDataWidgetState();
}

class FutureDataWidgetState extends ConsumerState<FutureDataWidget> {
  late Future<List<dynamic>> _dataFuture; // Future to fetch data
  late int countRow; // Number of rows in grid view
  late FutureWidgetType
      widgetType; // Type of widget (grid view or selectable list)
  late FutureDataType dataType; // Type of data to display
  late Logger _logger;

  @override
  void initState() {
    super.initState();
    _dataFuture = widget.fetchData; // Fetch data from the widget
    widgetType = widget.widgetType; // Set widget type
    dataType = widget.dataType; // Set data type
  }

  int selectedItemIndex = -1; // Index of selected item

  @override
  Widget build(BuildContext context) {
    _logger = ref.watch(loggingProvider);

    return FutureBuilder<List<dynamic>>(
      future: _dataFuture,
      builder: (context, snapshot) {
        if (snapshot.connectionState == ConnectionState.waiting) {
          _logger.t("Retrieving $dataType data...");
          return const CircularProgressIndicator(); // Show loading indicator while data is being fetched
        } else if (snapshot.hasError) {
          _logger.e("Error fetching data: ${snapshot.error}");
          return Text(
              'Error: ${snapshot.error}'); // Show error message if data fetching fails
        } else {
          final dataList = snapshot.data!;

          if (widgetType == FutureWidgetType.gridView) {
            countRow = widget.countRow!;
            return gridBuildWidget(context, dataList, countRow,
                dataType); // Build grid view widget
          } else {
            return selectableListWidget(context, dataList, selectedItemIndex,
                dataType); // Build selectable list widget
          }
        }
      },
    );
  }

  Widget selectableListWidget(BuildContext context, List<dynamic> dataList,
      int selectedItemIndex, FutureDataType dataType) {
    _logger.t(
        "Building selectableList with selectedItemIndex '$selectedItemIndex', dataType '$dataType' and item amount '${dataList.length}'");
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
                      : dataType == FutureDataType.recommendProduct
                          ? productSelect(data, index)
                          : Container(), // Replace 'null' with an empty Container widget
        );
      },
    );
  }

  Widget productSelect(Product product, int index) {
    return Material(
      elevation: 10,
      borderRadius: BorderRadius.circular(10),
      child: Ink(
        decoration: BoxDecoration(
          borderRadius: BorderRadius.circular(10),
          color: selectedItemIndex == index ? Colors.blue : Colors.blue[100],
        ),
        child: ListTile(
          leading: Image.memory(base64.decode(product.imageBase64!)),
          // Display the image of the product
          title: Text(
            product.naam,
            style: SizeScaler.getResponsiveTextStyle(
              context,
              15,
              FontWeight.bold,
              Colors.black,
            ),
          ),
          // Display the name of the product
          subtitle: Text(
            limitStringCharacters(product.beschrijving, 50),
            // Limit the description text to 85 characters
            style: const TextStyle(fontSize: 16),
          ),
          trailing: SingleProductView(
            productId: product.iD,
          ),
          // Display a custom widget for a single product view
          onTap: () {
            setState(() {
              if (selectedItemIndex == index) {
                selectedItemIndex = -1; // Deselect the item
                widget.onItemSelected!(-1, "");
                _logger.t(
                    "Deselected product '${product.iD}' with name '${product.naam}'");
              } else {
                selectedItemIndex = index; // Select the item
                widget.onItemSelected!(index, product.iD);
                _logger.t(
                    "Selected product '${product.iD}' with name '${product.naam}'");
              }
            });
          },
          // Handle tap events for the list tile
        ),
      ),
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
          // Display the problem text of the client
          onTap: () {
            setState(() {
              if (selectedItemIndex == index) {
                selectedItemIndex = -1; // Deselect the item
                widget.onItemSelected!(-1, "");
                _logger.t("Deselected problem '${client.probleem}'");
              } else {
                selectedItemIndex = index; // Select the item
                widget.onItemSelected!(index, client.probleem);
                _logger.t("Selected problem '${client.probleem}'");
              }
            });
          },
          // Handle tap events for the list tile
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
          // Display client ID
          leading: Text(
            'Client: 1',
            style: SizeScaler.getResponsiveTextStyle(
              context,
              18,
              FontWeight.bold,
              Colors.black,
            ),
          ),
          // Display client problem
          title: Text(
            "Probleem: ${client.probleem}",
            style: SizeScaler.getResponsiveTextStyle(
              context,
              18,
              FontWeight.bold,
              Colors.black,
            ),
          ),
          contentPadding: const EdgeInsets.all(20),
          subtitle: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              FutureBuilder<List<Product>>(
                future:
                    DataAPI(logger: _logger).getProductsForClient(client.iD!),
                builder: (context, snapshot) {
                  if (snapshot.hasData) {
                    _logger.t(
                        "Amount of products retrieved: '${snapshot.data!.length}'");
                    final productList = snapshot.data!;
                    final productNames =
                        productList.map((product) => product.naam).join(', ');
                    // Display the products used by the client
                    return Text(
                      'Maakt gebruik van: $productNames',
                      style: SizeScaler.getResponsiveTextStyle(
                        context,
                        18,
                        FontWeight.normal,
                        Colors.black,
                      ),
                    );
                  } else if (snapshot.hasError) {
                    _logger.e(
                        "An error occurred fetching the products: '${snapshot.error}'");
                    // Display an error message if there's an error
                    return Text(
                      'Error: ${snapshot.error}',
                      style: SizeScaler.getResponsiveTextStyle(
                        context,
                        18,
                        FontWeight.bold,
                        Colors.black,
                      ),
                    );
                  }
                  // Show a loading indicator while fetching the products
                  return const CircularProgressIndicator();
                },
              ),
            ],
          ),
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
          // Display the application name
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
                _logger.t("Deselected toepassing '${toepassing.toepassing}'");
              } else {
                selectedItemIndex = index; // Select the item
                _logger.t("Selected toepassing '${toepassing.toepassing}'");
              }
            });
          },
        ),
      ),
    );
  }

  Widget gridBuildWidget(BuildContext context, List<dynamic> dataList,
      int count, FutureDataType dataType) {
    double screenHeight = MediaQuery.of(context).size.height;
    return Expanded(
      child: GridView.builder(
          gridDelegate: SliverGridDelegateWithFixedCrossAxisCount(
            crossAxisCount: count, // Number of columns in the grid
            childAspectRatio: screenHeight > 900
                ? 3.5
                : count >= 2
                    ? 3.75
                    : 5.5, // Width to height ratio of each grid item
          ),
          itemCount: dataList.length,
          itemBuilder: (context, index) {
            final data = dataList[index];
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
                        ? productListTile(context, data)
                        : clientsListTile(context, data)),
              ),
            );
          }),
    );
  }
}

String limitStringCharacters(String text, int limit) {
  if (text.length <= limit) {
    return text;
  } else {
    return '${text.substring(0, limit)}...';
  }
}

// Generate the tile for each product
Widget productListTile(BuildContext context, Product product) {
  return Card(
    margin: const EdgeInsets.all(10),
    shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(10)),
    child: ListTile(
      leading: product.imageBase64 != null
          ? Image.memory(
              base64.decode(product.imageBase64!),
              key: ValueKey(
                "productListTileImage | ${product.iD}",
              ),
            )
          : Icon(
              Icons.image_not_supported_rounded,
              key: ValueKey(
                "productListTilePlaceholderImage | ${product.iD}",
              ),
            ),
      // Display the product name
      title: Text(
        product.naam,
        style: SizeScaler.getResponsiveTextStyle(
            context, 18, FontWeight.bold, Colors.black),
      ),
      // Display a truncated description of the product
      subtitle: Text(limitStringCharacters(product.beschrijving, 85),
          style: const TextStyle(fontSize: 16)),
      trailing: SingleProductView(
        productId: product.iD,
      ),
      contentPadding: const EdgeInsets.symmetric(horizontal: 10, vertical: 5),
      dense: true,
      enabled: false,
      selected: true,
      selectedTileColor: Colors.white10,
    ),
  );
}

// Generate the tile for each client
Widget clientsListTile(BuildContext context, Clients client) {
  return ListTile(
    // Display client ID
    leading: Text(
      'Client: ${client.iD}',
      style: SizeScaler.getResponsiveTextStyle(
          context, 18, FontWeight.bold, Colors.white),
    ),
    // Display client problem
    title: Text(
      client.probleem,
      style: SizeScaler.getResponsiveTextStyle(
          context, 18, FontWeight.bold, Colors.white),
    ),
    contentPadding: const EdgeInsets.all(20),
    // Display "Maakt gebruik van: " (translated: "Uses: ")
    subtitle: Text(
      'Maakt gebruik van: ',
      style: SizeScaler.getResponsiveTextStyle(
          context, 16, FontWeight.bold, Colors.white),
    ),
  );
}
