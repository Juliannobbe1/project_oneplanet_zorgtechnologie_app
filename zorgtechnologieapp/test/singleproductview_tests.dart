import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:nock/nock.dart';
import 'package:zorgtechnologieapp/handlers/data_api_handler.dart';
import 'package:zorgtechnologieapp/main.dart';
import 'package:zorgtechnologieapp/pages/products_page.dart';

void main() {
  setUpAll(() {
    nock.init();
  });

  setUp(() {
    nock.cleanAll();
  });

  testWidgets('SingleProductView - Shows all HealthcareTechnology-information',
      (WidgetTester tester) async {
    final products = [
      {
        "beschrijving":
            "Een gehoorbeschermer die het gehoor beschermt tegen harde geluiden en gehoorverlies voorkomt. Het is lichtgewicht verstelbaar en comfortabel om te dragen.",
        "ID": "0b1b9708-9711-404e-944d-01b3659f15d5",
        "leverancierID": "45e22d68-9632-42b9-83ad-6ff5a4e577b0",
        "link": "https://example.com/gehoorbeschermer",
        "naam": "Gehoorbeschermer",
        "prijs": 19.99,
        "imageBase64":
            "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk+A8AAQUBAScY42YAAAAASUVORK5CYII="
      }
    ];

    final productsInterceptor = nock(kApiBaseUrl).get("/product")
      ..reply(
        200,
        jsonEncode(
          products,
        ),
      );

    // Build app and trigger a frame.
    await tester.pumpWidget(
      const ProviderScope(
        child: PreferredOrientationWrapper(
          child: MaterialApp(
            home: SingleProductView(
              productId: "0b1b9708-9711-404e-944d-01b3659f15d5",
            ),
          ),
        ),
      ),
    );

    await tester.pumpAndSettle();
    expect(productsInterceptor.isDone, isTrue);

    await tester.tap(
        find.byKey(ValueKey("SingleProductViewButton | ${products[0]["ID"]}")));
    await tester.pumpAndSettle();

    expect(find.text(products[0]["naam"] as String), findsOne);
    expect(find.text(products[0]["beschrijving"] as String), findsOne);
    expect(find.textContaining(products[0]["link"] as String), findsOne);
    expect(find.textContaining(products[0]["prijs"].toString()), findsOne);
  });

  testWidgets(
      'SingleProductView - Shows all available HealthcareTechnology-information',
      (WidgetTester tester) async {
    final products = [
      {
        "beschrijving":
            "Een gehoorbeschermer die het gehoor beschermt tegen harde geluiden en gehoorverlies voorkomt. Het is lichtgewicht verstelbaar en comfortabel om te dragen.",
        "ID": "0b1b9708-9711-404e-944d-01b3659f15d5",
        "leverancierID": "45e22d68-9632-42b9-83ad-6ff5a4e577b0",
        "link": null,
        "naam": "Gehoorbeschermer",
        "prijs": null,
        "imageBase64":
            "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk+A8AAQUBAScY42YAAAAASUVORK5CYII="
      }
    ];

    final productsInterceptor = nock(kApiBaseUrl).get("/product")
      ..reply(
        200,
        jsonEncode(
          products,
        ),
      );

    // Build app and trigger a frame.
    await tester.pumpWidget(
      const ProviderScope(
        child: PreferredOrientationWrapper(
          child: MaterialApp(
            home: SingleProductView(
              productId: "0b1b9708-9711-404e-944d-01b3659f15d5",
            ),
          ),
        ),
      ),
    );

    await tester.pumpAndSettle();
    expect(productsInterceptor.isDone, isTrue);

    await tester.tap(
        find.byKey(ValueKey("SingleProductViewButton | ${products[0]["ID"]}")));
    await tester.pumpAndSettle();

    expect(find.text(products[0]["naam"] as String), findsOne);
    expect(find.text(products[0]["beschrijving"] as String), findsOne);
    expect(find.text("Prijs: Niet beschikbaar"), findsOne);
    expect(find.text("Link: Niet beschikbaar"), findsOne);
  });
}
