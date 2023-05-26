import 'package:flutter/material.dart';
import 'package:zorg_tech_keuze_app/handlers/get_products.dart';

import 'models/products.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Flutter Demo',
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      home: const HomePage(),
    );
  }
}

class HomePage extends StatelessWidget {
  const HomePage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Homepage'),
      ),
      body: TextButton(
        onPressed: () {
          Navigator.of(context).push(
              MaterialPageRoute(builder: (context) => const ProductPage()));
        },
        child: const Text('Go To Products'),
      ),
    );
  }
}

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
