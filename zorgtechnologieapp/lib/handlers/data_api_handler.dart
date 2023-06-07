import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:http/http.dart';
import 'package:selectable_list/selectable_list.dart';

import '../models/products.dart';
import '../models/toepassing.dart';

class DataAPI {
  String baseUrl = 'http://172.16.1.149:5001';

  Future<List<dynamic>> fetchData(String endpoint) async {
    String url = '$baseUrl$endpoint';
    Response response = await get(Uri.parse(url));
    if (response.statusCode == 200) {
      final List<dynamic> result = jsonDecode(response.body);
      return result;
    } else {
      throw Exception(response.reasonPhrase);
    }
  }

  Future<List<Product>> getProducts() async {
    List<dynamic> result = await fetchData('/product');
    return result
        .map((e) => Product.fromJson(e as Map<String, dynamic>))
        .toList();
  }

  Future<List<Product>> newestProducts() async {
    List<dynamic> result = await fetchData('/product/newest');
    return result
        .map((e) => Product.fromJson(e as Map<String, dynamic>))
        .toList();
  }

  Future<List<HeeftToepassing>> toepassingProducts() async {
    List<dynamic> result = await fetchData('/toepassing/HEEFT_TOEPASSING');
    return result
        .map((e) => HeeftToepassing.fromJson(e as Map<String, dynamic>))
        .toList();
  }

  Future<List<Toepassing>> distinctToepassing() async {
    List<dynamic> result = await fetchData('/toepassing/distinct');
    return result
        .map((toepassing) => Toepassing(toepassing: toepassing))
        .toList();
  }
}

class ListBuilder extends StatefulWidget {
  final Function(String?) onSelectedToepassingChanged;

  const ListBuilder({
    super.key,
    required this.onSelectedToepassingChanged,
  });

  @override
  ListBuilderState createState() => ListBuilderState();
}

class ListBuilderState extends State<ListBuilder> {
  String? selectedToepassing;

  @override
  Widget build(BuildContext context) {
    return FutureBuilder<List<Toepassing>>(
      future: DataAPI().distinctToepassing(),
      builder: (context, snapshot) {
        if (snapshot.hasData) {
          final toepassingen = snapshot.data!;
          final limitedToepassingen =
              toepassingen.take(5).toList(); // Limit to 5 items
          return SelectableList<Toepassing, String?>(
            items: limitedToepassingen,
            itemBuilder: (context, toepassing, selected, onTap) => Card(
              elevation: 2.0,
              shape: RoundedRectangleBorder(
                borderRadius: BorderRadius.circular(
                    10.0), // Set the border radius to make the edges round
              ),
              color: Colors.blue[100],
              child: ListTile(
                title: Text(toepassing.toepassing),
                selected: selected,
                onTap: onTap,
              ),
            ),
            valueSelector: (toepassing) => toepassing.toepassing,
            selectedValue: selectedToepassing,
            onItemSelected: (toepassing) {
              setState(() {
                selectedToepassing =
                    toepassing.toepassing; // Assign selected item
                widget.onSelectedToepassingChanged(selectedToepassing);
                print('Selected item: $selectedToepassing');
              });
            },
            onItemDeselected: (toepassing) {
              setState(() {
                selectedToepassing = null; // Deselect the item
                widget.onSelectedToepassingChanged(selectedToepassing);
              });
            },
          );
        } else if (snapshot.hasError) {
          return Center(child: Text("${snapshot.error}"));
        } else {
          return const Center(child: CircularProgressIndicator());
        }
      },
    );
  }
}
