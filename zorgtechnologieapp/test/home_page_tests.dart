import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:nock/nock.dart';
import 'package:zorgtechnologieapp/handlers/data_api_handler.dart';
import 'package:zorgtechnologieapp/main.dart';
import 'package:zorgtechnologieapp/pages/home_page.dart';

void main() {
  setUpAll(() {
    nock.init();
  });

  setUp(() {
    nock.cleanAll();
  });

  testWidgets('Home-page - Navigation to SelectionGuide',
      (WidgetTester tester) async {
    final newestProductsInterceptor = nock(kApiBaseUrl).get("/product/newest")
      ..reply(
        200,
        jsonEncode(
          [
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
          ],
        ),
      );

    final clientInterceptor = nock(kApiBaseUrl)
        .get("/client/wordtverzorgd/e040d519-dcc5-4969-86c3-54006f21656c")
      ..reply(
        200,
        jsonEncode(
          [
            {
              "ID": "ff51619d-253e-402f-812c-21a7fb15b6b1",
              "probleem": "Slaapstoornissen",
            },
          ],
        ),
      );

    final productsInterceptor = nock(kApiBaseUrl).get("/product")
      ..reply(
        200,
        jsonEncode(
          [
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
            },
          ],
        ),
      );

    final productsForClientInterceptor = nock(kApiBaseUrl)
        .get("/product/client/ff51619d-253e-402f-812c-21a7fb15b6b1")
      ..reply(
        200,
        jsonEncode(
          [
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
            },
          ],
        ),
      );

    // Build app and trigger a frame.
    await tester.pumpWidget(
      const ProviderScope(
        child: PreferredOrientationWrapper(
          child: MaterialApp(
            home: HomePage(),
          ),
        ),
      ),
    );

    expect(newestProductsInterceptor.isDone, isTrue);

    await tester.tap(find.text("Keuzegids"));
    await tester.pumpAndSettle();

    expect(clientInterceptor.isDone, isTrue);
    expect(productsInterceptor.isDone, isTrue);
    expect(productsForClientInterceptor.isDone, isTrue);

    expect(find.text("Clienten Overzicht"), findsOne);
  });

  testWidgets('Home-page - Navigation to ProductPage',
      (WidgetTester tester) async {
    final newestProductsInterceptor = nock(kApiBaseUrl).get("/product/newest")
      ..reply(
        200,
        jsonEncode(
          [
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
          ],
        ),
      );

    final productsInterceptor = nock(kApiBaseUrl).get("/product")
      ..persist()
      ..reply(
        200,
        jsonEncode(
          [
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
            },
          ],
        ),
      );

    // Build app and trigger a frame.
    await tester.pumpWidget(
      const ProviderScope(
        child: PreferredOrientationWrapper(
          child: MaterialApp(
            home: HomePage(),
          ),
        ),
      ),
    );

    expect(newestProductsInterceptor.isDone, isTrue);

    await tester.tap(find.text("Technologie-catalogus"));
    await tester.pumpAndSettle();

    expect(productsInterceptor.isDone, isTrue);

    expect(find.text("Technologie Overzicht"), findsOne);
  });

  testWidgets('Home-page - Shows most recent HealthcareTechnologies',
      (WidgetTester tester) async {
    final newestProducts = [
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
      },
      {
        "beschrijving":
            "Een comfortabele stoel die mensen helpt bij het opstaan en gaan zitten. Het heeft een elektrische liftfunctie verstelbare positie en zachte bekleding.",
        "ID": "6eb3e14c-83b1-42ba-a63f-352b6433ec3a",
        "leverancierID": "45e22d68-9632-42b9-83ad-6ff5a4e577b0",
        "link": "https://example.com/sta-op-stoel",
        "naam": "Sta-op Stoel",
        "prijs": 599.99,
        "imageBase64":
            "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk+A8AAQUBAScY42YAAAAASUVORK5CYII="
      },
      {
        "beschrijving":
            "Een steunbeugel die kan worden ge\u00efnstalleerd in de badkamer om extra ondersteuning en stabiliteit te bieden. Het heeft een roestvrijstalen constructie en een geribbeld oppervlak voor grip.",
        "ID": "f9820126-a81b-45f2-a7c9-a4304130a059",
        "leverancierID": "45e22d68-9632-42b9-83ad-6ff5a4e577b0",
        "link": "https://example.com/steunbeugel-badkamer",
        "naam": "Steunbeugel voor Badkamer",
        "prijs": 39.99,
        "imageBase64":
            "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk+A8AAQUBAScY42YAAAAASUVORK5CYII="
      },
      {
        "beschrijving":
            "Een opvouwbare toiletsteun die extra stabiliteit biedt bij het opstaan en gaan zitten. Het is gemakkelijk op te bergen en heeft antislipvoeten voor veiligheid.",
        "ID": "507be385-e85b-44c6-9ede-7615652f4492",
        "leverancierID": "45e22d68-9632-42b9-83ad-6ff5a4e577b0",
        "link": "https://example.com/opvouwbare-toiletsteun",
        "naam": "Opvouwbare Toiletsteun",
        "prijs": 49.99,
        "imageBase64":
            "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk+A8AAQUBAScY42YAAAAASUVORK5CYII="
      },
      {
        "beschrijving":
            "Een draadloze oplader die het mogelijk maakt om je telefoon draadloos op te laden. Het is compatibel met de meeste moderne smartphones en heeft een slank ontwerp.",
        "ID": "be4f32d9-5843-4104-9f00-a8bfdf96f11e",
        "leverancierID": "45e22d68-9632-42b9-83ad-6ff5a4e577b0",
        "link": "https://example.com/draadloze-oplader",
        "naam": "Draadloze Oplader",
        "prijs": 29.99,
        "imageBase64":
            "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk+A8AAQUBAScY42YAAAAASUVORK5CYII="
      },
      {
        "beschrijving":
            "Een beveiligingscamera die je huis of kantoor bewaakt. Het heeft nachtzicht bewegingsdetectie en kan live videobeelden streamen naar je smartphone.",
        "ID": "35fdf7f3-0296-4cce-b491-8080b2d16c19",
        "leverancierID": "259a92a3-370a-4c57-a7c2-88c5c89d8dd8",
        "link": "https://example.com/beveiligingscamera",
        "naam": "Beveiligingscamera",
        "prijs": 129.99,
        "imageBase64":
            "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk+A8AAQUBAScY42YAAAAASUVORK5CYII="
      },
    ];

    final newestProductsInterceptor = nock(kApiBaseUrl).get("/product/newest")
      ..reply(
        200,
        jsonEncode(
          newestProducts,
        ),
      );

    final productsInterceptor = nock(kApiBaseUrl).get("/product")
      ..persist()
      ..reply(
        200,
        jsonEncode(
          newestProducts,
        ),
      );

    // Build app and trigger a frame.
    await tester.pumpWidget(
      const ProviderScope(
        child: PreferredOrientationWrapper(
          child: MaterialApp(
            home: HomePage(),
          ),
        ),
      ),
    );

    await tester.pumpAndSettle();
    expect(newestProductsInterceptor.isDone, isTrue);
    expect(productsInterceptor.isDone, isTrue);

    for (var product in newestProducts) {
      expect(find.text(product["naam"] as String), findsOne);
    }
  });
}
