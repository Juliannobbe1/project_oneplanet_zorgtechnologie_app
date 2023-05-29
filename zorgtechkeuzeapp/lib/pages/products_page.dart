import 'package:flutter/material.dart';

import '../handlers/get_products.dart';
import '../handlers/responsive_layout_handler.dart';
import '../models/products.dart';

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
        body: PhoneProductPage(
          screenWidth: screenWidth,
        ));
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
      body: FutureBuilder<List<Product>>(
        future: ApiCall().getProducts(),
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
                    padding: const EdgeInsets.fromLTRB(15.0, 10.0, 15.0, 10.0),
                    child: Material(
                      elevation: 5,
                      borderRadius: const BorderRadius.all(Radius.circular(10)),
                      child: Container(
                        decoration: BoxDecoration(
                          borderRadius: const BorderRadius.all(
                            Radius.circular(10),
                          ),
                          color: Colors.blue[500],
                        ),
                        child: ListTile(
                            title: Text(
                              product.productNaam,
                              style: SizeScaler.getResponsiveTextStyle(
                                  context, 18, FontWeight.bold, Colors.white),
                            ),
                            subtitle: Text(
                              'Categorie: ${product.categorie}',
                              style: SizeScaler.getResponsiveTextStyle(
                                  context, 17, FontWeight.normal, Colors.white),
                            ),
                            trailing: SingleProductView(
                              product: product,
                            )),
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
    );
  }
}

class PhoneProductPage extends StatelessWidget {
  final double screenWidth;
  const PhoneProductPage({super.key, required this.screenWidth});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: Theme.of(context).colorScheme.inversePrimary,
        title: const Text("Product page"),
      ),
      body: Padding(
        padding: EdgeInsets.only(top: screenWidth * 0.05),
        child: FutureBuilder<List<Product>>(
          future: ApiCall().getProducts(),
          builder: (context, snapshot) {
            if (snapshot.hasData) {
              return ListView(
                children: [
                  ...snapshot.data!.map(
                    (product) => Padding(
                      padding: EdgeInsets.fromLTRB(
                          screenWidth * 0.05,
                          screenWidth * 0.03,
                          screenWidth * 0.05,
                          screenWidth * 0.03),
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
                              product.productNaam,
                              style: SizeScaler.getResponsiveTextStyle(
                                  context, 18, FontWeight.bold, Colors.white),
                            ),
                            subtitle: Text(
                              'Categorie: ${product.categorie}',
                              style: SizeScaler.getResponsiveTextStyle(
                                  context, 17, FontWeight.normal, Colors.white),
                            ),
                            trailing: SingleProductView(
                              product: product,
                            ),
                          ),
                        ),
                      ),
                    ),
                  ),
                ],
              );
            } else if (snapshot.hasError) {
              return Text('${snapshot.error}');
            } else {
              return const Center(child: CircularProgressIndicator());
            }
          },
        ),
      ),
    );
  }
}

class SingleProductView extends StatelessWidget {
  final Product product;
  const SingleProductView({super.key, required this.product});

  @override
  Widget build(BuildContext context) {
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
                      product.productNaam,
                      style: SizeScaler.getResponsiveTextStyle(
                          context, 20, FontWeight.bold, Colors.black),
                    ),
                    const SizedBox(height: 10),
                    // Text('Product Name: ${product.productNaam}'),
                    // Text('Category: ${product.categorie}'),
                    Text(
                      product.beschrijving,
                      style: SizeScaler.getResponsiveTextStyle(
                          context, 20, FontWeight.normal, Colors.black),
                    ),
                    const SizedBox(height: 5),
                    Text(
                      'Category: ${product.categorie}',
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
                    Text('Link: ${product.link}',
                        style: SizeScaler.getResponsiveTextStyle(
                            context, 20, FontWeight.normal, Colors.black)),

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
  }
}
