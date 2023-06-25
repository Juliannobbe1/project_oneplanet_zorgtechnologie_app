import 'package:flutter/material.dart';
import 'package:zorgtechnologieapp/models/toepassing.dart';

import '../handlers/data_api_handler.dart';
import '../handlers/responsive_layout_handler.dart';
import '../models/products.dart';
import '../widgets/futurebuilder.dart';

class ProductPage extends StatelessWidget {
  const ProductPage({super.key});

  @override
  Widget build(BuildContext context) {
    double screenWidth = MediaQuery.of(context).size.width;
    return Scaffold(
        appBar: AppBar(
          backgroundColor: Theme.of(context).colorScheme.inversePrimary,
          title: const Text("Product page"),
        ),
        body: const TabletProductPage());
  }
}

class TabletProductPage extends StatelessWidget {
  const TabletProductPage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: Theme.of(context).colorScheme.inversePrimary,
        title: const Text("Product page"),
      ),
      body: FutureDataWidget(
          fetchData: DataAPI().newestProducts(),
          countRow: 2,
          widgetType: FutureWidgetType.gridView,
          dataType: FutureDataType.product),
    );
  }
}

// class SingleProductView extends StatelessWidget {
//   final Product product;
//   const SingleProductView({super.key, required this.product});
//
//   @override
//   Widget build(BuildContext context) {
//     return IconButton(
//       icon: const Icon(
//         Icons.info,
//         color: Colors.black,
//       ),
//       onPressed: () {
//         showDialog(
//           context: context,
//           builder: (context) => Dialog(
//             shape: RoundedRectangleBorder(
//               borderRadius: BorderRadius.circular(10),
//             ),
//             child: Container(
//               padding: const EdgeInsets.all(16),
//               constraints: const BoxConstraints(maxHeight: 600),
//               child: SingleChildScrollView(
//                 child: Column(
//                   crossAxisAlignment: CrossAxisAlignment.start,
//                   children: [
//                     Text(
//                       product.naam,
//                       style: SizeScaler.getResponsiveTextStyle(
//                           context, 20, FontWeight.bold, Colors.black),
//                     ),
//                     const SizedBox(height: 10),
//                     // Text('Product Name: ${product.productNaam}'),
//                     // Text('Category: ${product.categorie}'),
//                     Text(
//                       product.beschrijving,
//                       style: SizeScaler.getResponsiveTextStyle(
//                           context, 20, FontWeight.normal, Colors.black),
//                     ),
//                     const SizedBox(height: 5),
//                     // Text(
//                     //   'Category: ${product.categorie}',
//                     //   style: SizeScaler.getResponsiveTextStyle(
//                     //       context, 20, FontWeight.normal, Colors.black),
//                     // ),
//                     // const SizedBox(height: 5),
//                     Text(
//                       'Prijs: ${product.prijs}',
//                       style: SizeScaler.getResponsiveTextStyle(
//                           context, 20, FontWeight.normal, Colors.black),
//                     ),
//                     const SizedBox(height: 5),
//                     Text('Link: ${product.link}',
//                         style: SizeScaler.getResponsiveTextStyle(
//                             context, 20, FontWeight.normal, Colors.black)),
//
//                     Row(
//                       mainAxisAlignment: MainAxisAlignment.end,
//                       children: [
//                         TextButton(
//                           child: const Text('Close'),
//                           onPressed: () => Navigator.pop(context),
//                         ),
//                       ],
//                     ),
//                   ],
//                 ),
//               ),
//             ),
//           ),
//         );
//       },
//     );
//   }
// }

class SingleProductView extends StatelessWidget {
  final String productId;

  const SingleProductView({Key? key, required this.productId})
      : super(key: key);

  Future<Product> fetchProduct() async {
    List<Product> products = await DataAPI().getProducts();
    return products.firstWhere((product) => product.iD == productId);
  }

  @override
  Widget build(BuildContext context) {
    return FutureBuilder<Product>(
      future: fetchProduct(),
      builder: (context, snapshot) {
        if (snapshot.hasData) {
          Product product = snapshot.data!;
          return IconButton(
            icon: const Icon(
              Icons.info,
              color: Colors.black,
            ),
            onPressed: () {
              showDialog(
                context: context,
                builder: (context) => Dialog(
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(10),
                  ),
                  child: Container(
                    padding: const EdgeInsets.all(16),
                    constraints: const BoxConstraints(maxHeight: 600),
                    child: SingleChildScrollView(
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text(
                            product.naam,
                            style: SizeScaler.getResponsiveTextStyle(
                                context, 20, FontWeight.bold, Colors.black),
                          ),
                          const SizedBox(height: 10),
                          Text(
                            product.beschrijving,
                            style: SizeScaler.getResponsiveTextStyle(
                                context, 20, FontWeight.normal, Colors.black),
                          ),
                          const SizedBox(height: 5),
                          Text(
                            'Prijs: ${product.prijs}',
                            style: SizeScaler.getResponsiveTextStyle(
                                context, 20, FontWeight.normal, Colors.black),
                          ),
                          const SizedBox(height: 5),
                          Text(
                            'Link: ${product.link}',
                            style: SizeScaler.getResponsiveTextStyle(
                                context, 20, FontWeight.normal, Colors.black),
                          ),
                          Row(
                            mainAxisAlignment: MainAxisAlignment.end,
                            children: [
                              TextButton(
                                child: const Text('Close'),
                                onPressed: () => Navigator.pop(context),
                              ),
                            ],
                          ),
                        ],
                      ),
                    ),
                  ),
                ),
              );
            },
          );
        } else if (snapshot.hasError) {
          return IconButton(
            icon: const Icon(
              Icons.info,
              color: Colors.black,
            ),
            onPressed: () {
              // Handle error state
              showDialog(
                context: context,
                builder: (context) => AlertDialog(
                  title: const Text('Error'),
                  content: const Text('Failed to fetch product details.'),
                  actions: [
                    TextButton(
                      child: const Text('Close'),
                      onPressed: () => Navigator.pop(context),
                    ),
                  ],
                ),
              );
            },
          );
        } else {
          return IconButton(
            icon: const Icon(
              Icons.info,
              color: Colors.black,
            ),
            onPressed: () {
              // Display loading state
              showDialog(
                context: context,
                builder: (context) => const Center(
                  child: CircularProgressIndicator(),
                ),
              );
            },
          );
        }
      },
    );
  }
}
