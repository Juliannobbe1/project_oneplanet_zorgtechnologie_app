import 'dart:convert';
import 'dart:io';

import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:zorgtechnologieapp/models/clients.dart';
import 'package:zorgtechnologieapp/models/products.dart';
import 'package:zorgtechnologieapp/pages/products_page.dart';

import '../handlers/data_api_handler.dart';
import '../handlers/responsive_layout_handler.dart';

class ProductImageScreen extends StatefulWidget {
  const ProductImageScreen({super.key});

  @override
  ProductImageScreenState createState() => ProductImageScreenState();
}

class ProductImageScreenState extends State<ProductImageScreen> {
  @override
  void initState() {
    super.initState();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Product Image'),
      ),
      body: Center(
        child: FutureBuilder<List<Clients>>(
          future: DataAPI().latestClient(),
          builder: (context, snapshot) {
            if (snapshot.connectionState == ConnectionState.waiting) {
              return const CircularProgressIndicator();
            } else if (snapshot.hasError) {
              return Text('Error: ${snapshot.error}');
            } else {
              final dataList = snapshot.data!;
              return Scaffold(
                body: Center(
                  child: ListView.builder(
                    itemCount: dataList.length,
                    itemBuilder: (BuildContext context, int index) {
                      final product = dataList[index];
                      return Padding(
                        padding: const EdgeInsets.all(8.0),
                        child: Text('${product.iD}'),
                      );
                    },
                  ),
                ),
              );

              //     Image.memory(base64.decode(imageBase64)),
              //   ),
              // );
            }
          },
        ),
      ),
    );
  }
}
