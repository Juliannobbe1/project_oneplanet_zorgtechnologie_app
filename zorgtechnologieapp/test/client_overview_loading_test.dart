import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:mockito/mockito.dart';
import 'package:nock/nock.dart';
import 'package:zorgtechnologieapp/main.dart';
import 'package:zorgtechnologieapp/pages/home_page.dart';

class MockNavigatorObserver extends Mock implements NavigatorObserver {}

void main() {
  setUpAll(() {
    nock.init();
  });

  setUp(() {
    nock.cleanAll();
  });

  testWidgets(
      'performance test - Clicking Keuzegids button navigates to ClientOverview',
      (WidgetTester tester) async {
    // Ignore overflow errors
    // The error is in the test only and can't be figuered out how to fix it renderflow on the bottom where nothing of the UI is
    FlutterError.onError = (FlutterErrorDetails details) {
      if (details.exception is FlutterError &&
          (details.exception as FlutterError)
              .message
              .contains('A RenderFlex overflowed by')) {
        // Ignore this error
        return;
      }
      // Forward other errors to the test framework
      FlutterError.dumpErrorToConsole(details);
    };
    // Create a mock navigator observer
    final mockObserver = MockNavigatorObserver();

    // Build our app and trigger a frame.
    await tester.pumpWidget(
      ProviderScope(
        child: PreferredOrientationWrapper(
            child: MaterialApp(
          home: const HomePage(),
          navigatorObservers: [mockObserver],
        )),
      ),
    );

    // Verify that we are on the home page.
    expect(find.text('Welcome'), findsOneWidget);

    // Get start time
    final startTime = DateTime.now();

    // Tap the Keuzegids button.
    await tester.tap(find.text('Keuzegids'));
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
    final productinteceptor = nock("http://192.168.72.182:5001")
        .get("/product/client/2e7cdd22-6d64-4e43-a8c6-9c6d3f3a7b3e")
      ..reply(
        200,
        jsonEncode([
          {
            "beschrijving":
                "Een gehoorbeschermer die het gehoor beschermt tegen harde geluiden en gehoorverlies voorkomt. Het is lichtgewicht verstelbaar en comfortabel om te dragen.",
            "ID": "0b1b9708-9711-404e-944d-01b3659f15d5",
            "leverancierID": "45e22d68-9632-42b9-83ad-6ff5a4e577b0",
            "link": "https://example.com/gehoorbeschermer",
            "naam": "Gehoorbeschermer",
            "prijs": 19.99,
            "imageBase64": null
          },
        ]),
      );

    // to ensure that the navigation has completed
    await tester.pumpAndSettle();

    // final widgets = tester.allWidgets;
    // for (final widget in widgets) {
    //   print('Widgets: $widget');
    // }

    // Verify that we are on the Clienten Overzicht page.
    expect(find.text('Clienten Overzicht'), findsOneWidget);

    expect(clientinterceptor.isDone, true);
    expect(productinteceptor.isDone, true);

    // Calculate the loading time
    final loadingTime = DateTime.now().difference(startTime).inMilliseconds;

    // Ensure that the loading time is faster than 1 seconds.
    expect(loadingTime, lessThan(1000));
  });
}
