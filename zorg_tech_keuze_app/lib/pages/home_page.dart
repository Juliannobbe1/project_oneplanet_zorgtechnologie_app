import 'package:flutter/material.dart';
import 'package:zorg_tech_keuze_app/handlers/get_products.dart';
import 'package:zorg_tech_keuze_app/handlers/responsive_layout_handler.dart';
import 'package:zorg_tech_keuze_app/models/products.dart';
import 'package:zorg_tech_keuze_app/pages/products_page.dart';

class HomePage extends StatelessWidget {
  const HomePage({super.key});

  @override
  Widget build(BuildContext context) {
    final TextStyle standardTextSize = SizeScaler.getResponsiveTextStyle(
        context, 20, FontWeight.bold, Colors.white);
    final TextStyle titleTextSize = SizeScaler.getResponsiveTextStyle(
        context, 25, FontWeight.bold, Colors.white);

    return Scaffold(
      backgroundColor: const Color.fromRGBO(231, 235, 244, 1),
      appBar: AppBar(
        leading: const Icon(Icons.menu),
        title: Text(
          "Welkom terug {{gebruiker}}",
          style: titleTextSize,
        ),
      ),
      body: Column(
        children: [
          Padding(
            padding: const EdgeInsets.fromLTRB(15.0, 20.0, 15.0, 5.0),
            child: AspectRatio(
              aspectRatio: 16 / 5,
              child: Container(
                decoration: BoxDecoration(
                  borderRadius: const BorderRadius.all(
                    Radius.circular(10),
                  ),
                  color: Colors.blue[900],
                ),
                // color: const Color.fromRGBO(105, 52, 254, 1),
                // color: Colors.blue[700],
                child: Center(
                  child: TextButton(
                    style: TextButton.styleFrom(
                      fixedSize: const Size(300, 100),
                    ),
                    onPressed: () {
                      Navigator.of(context).push(MaterialPageRoute(
                          builder: (context) => const ProductPage()));
                    },
                    child: Text("Keuzegids", style: standardTextSize),
                  ),
                ),
              ),
            ),
          ),

          Padding(
            padding: const EdgeInsets.all(15.0),
            child: AspectRatio(
              aspectRatio: 16 / 5,
              child: Container(
                decoration: BoxDecoration(
                  borderRadius: const BorderRadius.all(
                    Radius.circular(10),
                  ),
                  color: Colors.blue[800],
                ),
                child: Center(
                  child: TextButton(
                    onPressed: () {
                      Navigator.of(context).push(MaterialPageRoute(
                          builder: (context) => const ProductPage()));
                    },
                    child:
                        Text("Technologie-catalogus", style: standardTextSize),
                  ),
                ),
              ),
            ),
          ),

          Padding(
            padding: const EdgeInsets.only(right: 165.0, top: 7.5),
            child: Text(
              "Nieuwste producten:",
              style: SizeScaler.getResponsiveTextStyle(
                  context, 21, FontWeight.bold, Colors.black),
            ),
          ),

          // comment section & recommended videos
          FutureBuilder<List<Product>>(
            future: ApiCall().newestProducts(),
            builder: (context, snapshot) {
              if (snapshot.hasData) {
                final products = snapshot.data!;
                return SizedBox(
                  height: 325, // Specify the desired height for the ListView
                  child: ListView.builder(
                    itemCount: products.length,
                    itemBuilder: (context, index) {
                      final product = products[index];
                      return Padding(
                        padding:
                            const EdgeInsets.fromLTRB(15.0, 10.0, 15.0, 10.0),
                        child: Container(
                          decoration: BoxDecoration(
                            borderRadius: const BorderRadius.all(
                              Radius.circular(10),
                            ),
                            color: Colors.blue[500],
                          ),
                          height: 75,
                          child: ListTile(
                            title: Text(
                              product.productNaam,
                              style: SizeScaler.getResponsiveTextStyle(
                                  context, 20, FontWeight.bold, Colors.white),
                            ),
                            subtitle: Text(
                              'Categorie: ${product.categorie}',
                              style: SizeScaler.getResponsiveTextStyle(
                                  context, 18, FontWeight.normal, Colors.white),
                            ),
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
          )

          // Expanded(
          //   child: ListView.builder(
          //     itemCount: 5,
          //     itemBuilder: (context, index) {
          //       return Padding(
          //         padding: const EdgeInsets.fromLTRB(15.0, 10.0, 15.0, 10.0),
          //         child: Container(
          //           decoration: BoxDecoration(
          //             borderRadius: const BorderRadius.all(
          //               Radius.circular(10),
          //             ),
          //             color: Colors.blue[500],
          //           ),
          //           height: 100,
          //         ),
          //       );
          //     },
          //   ),
          // )
        ],
      ),
    );
  }
}

//     return Scaffold(
//       appBar: AppBar(
//         title: const Text('Home'),
//       ),
//       body: Center(
//         child: SingleChildScrollView(
//           child: Column(
//             children: [
//               Padding(
//                 padding: const EdgeInsets.all(8.0),
//                 child: AspectRatio(
//                   aspectRatio: 16 / 9,
//                   child: Container(
//                     color: Colors.deepPurple[400],
//                   ),
//                 ),
//               ),

//               // comment section & recommended videos
//               Expanded(
//                 child: ListView.builder(
//                   itemCount: 8,
//                   itemBuilder: (context, index) {
//                     return Padding(
//                       padding: const EdgeInsets.all(8.0),
//                       child: Container(
//                         color: Colors.deepPurple[300],
//                         height: 120,
//                       ),
//                     );
//                   },
//                 ),
//               ),
//             ],
//           ),
//         ),
//       ),
//     );
//   }
// }
