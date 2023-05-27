import 'package:flutter/material.dart';
import 'package:zorg_tech_keuze_app/handlers/get_products.dart';
import 'package:zorg_tech_keuze_app/models/products.dart';

class ProductPage extends StatelessWidget {
  const ProductPage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text("Product page"),
      ),
      body: FutureBuilder<List<Product>>(
          future: ApiCall().getProducts(),
          builder: (context, snapshot) {
            if (snapshot.hasData) {
              return ListView(
                children: [
                  ...snapshot.data!.map((e) => ListTile(
                        title: Text(e.productNaam),
                        subtitle: Text(e.beschrijving),
                      ))
                ],
              );
            } else if (snapshot.hasError) {
              return Text('$snapshot.error');
            } else {
              return const Center(child: CircularProgressIndicator());
            }
          }),
    );
  }
}
