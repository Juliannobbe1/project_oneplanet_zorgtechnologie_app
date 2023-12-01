import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:nock/nock.dart';
import 'package:zorgtechnologieapp/main.dart';
import 'package:zorgtechnologieapp/pages/client_overview_page.dart';

void main() {
  setUpAll(() {
    nock.init();
  });

  setUp(() {
    nock.cleanAll();
  });

  testWidgets('Load data in clientoverview screen',
      (WidgetTester tester) async {
    final clientinterceptor = nock("http://192.168.72.182:5001")
        .get("/client/wordtverzorgd/e040d519-dcc5-4969-86c3-54006f21656c")
      ..reply(
        200,
        jsonEncode([
          {
            "probleem": "Veiligheid en toezicht",
            "ID": "2e7cdd22-6d64-4e43-a8c6-9c6d3f3a7b3e"
          },
        ]),
      );

    await tester.pumpWidget(const ProviderScope(
        child: PreferredOrientationWrapper(
            child: MaterialApp(home: ClientOverview()))));

    // Use nock.cleanAll() to reset the interceptor and then check if there are no more pending mock requests
    nock.cleanAll();
    expect(clientinterceptor.isDone, true);
  });
}

//   testWidgets('Load data in clientoverview screen',
//       (WidgetTester tester) async {
//     final productinteceptor = nock("http://192.168.72.182:5001")
//         .get("/product/client/2e7cdd22-6d64-4e43-a8c6-9c6d3f3a7b3e")
//       ..reply(
//         200,
//         jsonEncode([
//           {
//             "beschrijving":
//                 "Een gehoorbeschermer die het gehoor beschermt tegen harde geluiden en gehoorverlies voorkomt. Het is lichtgewicht verstelbaar en comfortabel om te dragen.",
//             "ID": "0b1b9708-9711-404e-944d-01b3659f15d5",
//             "leverancierID": "45e22d68-9632-42b9-83ad-6ff5a4e577b0",
//             "link": "https://example.com/gehoorbeschermer",
//             "naam": "Gehoorbeschermer",
//             "prijs": 19.99,
//             "imageBase64": null
//           },
//         ]),
//       );

//     await tester.pumpWidget(const ProviderScope(
//         child: PreferredOrientationWrapper(
//       MaterialApp(
//         home: Scaffold(
//           body: clientSelectTile())))));

//     // Use nock.cleanAll() to reset the interceptor and then check if there are no more pending mock requests
//     nock.cleanAll();
//     expect(productinteceptor.isDone, true);
//   });
// }
