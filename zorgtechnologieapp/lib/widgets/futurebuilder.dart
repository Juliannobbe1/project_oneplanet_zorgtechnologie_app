import 'package:flutter/material.dart';

import '../handlers/responsive_layout_handler.dart';
import '../models/products.dart';
import '../pages/products_page.dart';

typedef DataFetcher = Future<List<dynamic>> Function();

class ScreenWithFetcher extends StatefulWidget {
  final DataFetcher fetchData;
  final int count;

  const ScreenWithFetcher(
      {Key? key, required this.fetchData, required this.count})
      : super(key: key);

  @override
  ScreenWithFetcherState createState() => ScreenWithFetcherState();
}

class ScreenWithFetcherState extends State<ScreenWithFetcher> {
  late Future<List<dynamic>> _dataFuture;
  late int count;

  @override
  void initState() {
    super.initState();
    _dataFuture = widget.fetchData();
    count = widget.count;
  }

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

          return buildScreenWithData(context, dataList, count);
        }
      },
    );
  }

  Widget buildScreenWithData(
      BuildContext context, List<dynamic> dataList, int count) {
    double screenWidth = MediaQuery.of(context).size.width;
    double screenHeight = MediaQuery.of(context).size.height;
    return Expanded(
      child: GridView.builder(
        gridDelegate: SliverGridDelegateWithFixedCrossAxisCount(
          crossAxisCount: count, // Number of columns in the grid
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
                    child: productListTile(data)),
              ),
            );
          }
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
