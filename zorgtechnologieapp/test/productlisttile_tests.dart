import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:nock/nock.dart';
import 'package:zorgtechnologieapp/handlers/data_api_handler.dart';
import 'package:zorgtechnologieapp/main.dart';
import 'package:zorgtechnologieapp/models/products.dart';
import 'package:zorgtechnologieapp/widgets/futurebuilder.dart';

class ProductListTileBuilder extends StatelessWidget {
  final Product product;

  const ProductListTileBuilder({super.key, required this.product});

  @override
  Widget build(BuildContext context) {
    return productListTile(context, product);
  }
}

void main() {
  setUpAll(() {
    nock.init();
  });

  setUp(() {
    nock.cleanAll();
  });

  testWidgets(
      'productListTile - Shows all necessary information of a HealthcareTechnology',
      (WidgetTester tester) async {
    final product = Product(
      iD: "0b1b9708-9711-404e-944d-01b3659f15d5",
      naam: "Gehoorbeschermer",
      beschrijving:
          "Een gehoorbeschermer die het gehoor beschermt tegen harde geluiden en gehoorverlies voorkomt. Het is lichtgewicht verstelbaar en comfortabel om te dragen.",
      prijs: 19.99,
      link: "https://example.com/gehoorbeschermer",
      imageBase64:
          "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk+A8AAQUBAScY42YAAAAASUVORK5CYII=",
    );

    final productsInterceptor = nock(kApiBaseUrl).get("/product")
      ..reply(200, [
        {
          "beschrijving":
              "Een gehoorbeschermer die het gehoor beschermt tegen harde geluiden en gehoorverlies voorkomt. Het is lichtgewicht verstelbaar en comfortabel om te dragen.",
          "ID": "0b1b9708-9711-404e-944d-01b3659f15d5",
          "link": "https://example.com/gehoorbeschermer",
          "naam": "Gehoorbeschermer",
          "prijs": 19.99,
          "imageBase64":
              "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk+A8AAQUBAScY42YAAAAASUVORK5CYII="
        }
      ]);

    // Build app and trigger a frame.
    await tester.pumpWidget(
      ProviderScope(
        child: PreferredOrientationWrapper(
          child: MaterialApp(
            home: ProductListTileBuilder(
              product: product,
            ),
          ),
        ),
      ),
    );

    await tester.pumpAndSettle();
    expect(productsInterceptor.isDone, isTrue);

    expect(
        find.byKey(ValueKey(
          "productListTileImage | ${product.iD}",
        )),
        findsOne);
    expect(find.text(product.naam), findsOne);
    expect(
        find.text(
          limitStringCharacters(
            product.beschrijving,
            85,
          ),
        ),
        findsOne);
  });

  testWidgets(
      'productListTile - Shows all necessary information of a HealthcareTechnology without an image',
      (WidgetTester tester) async {
    final product = Product(
      iD: "0b1b9708-9711-404e-944d-01b3659f15d5",
      naam: "Gehoorbeschermer",
      beschrijving:
          "Een gehoorbeschermer die het gehoor beschermt tegen harde geluiden en gehoorverlies voorkomt. Het is lichtgewicht verstelbaar en comfortabel om te dragen.",
      prijs: 19.99,
      link: "https://example.com/gehoorbeschermer",
      imageBase64: null,
    );

    final productsInterceptor = nock(kApiBaseUrl).get("/product")
      ..reply(200, [
        {
          "beschrijving":
              "Een gehoorbeschermer die het gehoor beschermt tegen harde geluiden en gehoorverlies voorkomt. Het is lichtgewicht verstelbaar en comfortabel om te dragen.",
          "ID": "0b1b9708-9711-404e-944d-01b3659f15d5",
          "link": "https://example.com/gehoorbeschermer",
          "naam": "Gehoorbeschermer",
          "prijs": 19.99,
          "imageBase64": null,
        }
      ]);

    // Build app and trigger a frame.
    await tester.pumpWidget(
      ProviderScope(
        child: PreferredOrientationWrapper(
          child: MaterialApp(
            home: ProductListTileBuilder(
              product: product,
            ),
          ),
        ),
      ),
    );

    await tester.pumpAndSettle();
    expect(productsInterceptor.isDone, isTrue);

    expect(
        find.byKey(
          ValueKey(
            "productListTilePlaceholderImage | ${product.iD}",
          ),
        ),
        findsOne);
    expect(find.text(product.naam), findsOne);
    expect(
        find.text(
          limitStringCharacters(
            product.beschrijving,
            85,
          ),
        ),
        findsOne);
  });
}
