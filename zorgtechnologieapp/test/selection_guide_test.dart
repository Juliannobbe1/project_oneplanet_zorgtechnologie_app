import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:mockito/mockito.dart';
import 'package:nock/nock.dart';
import 'package:zorgtechnologieapp/handlers/data_api_handler.dart';
import 'package:zorgtechnologieapp/main.dart';
import 'package:zorgtechnologieapp/pages/selection_guide.dart';

class MockNavigatorObserver extends Mock implements NavigatorObserver {}

void main() {
  setUpAll(() {
    nock.init();
  });

  setUp(() {
    nock.cleanAll();
  });
  testWidgets('Unit test - select problem', (WidgetTester tester) async {
    final mockObserver = MockNavigatorObserver();
    final probleeminterceptor =
        nock(kApiBaseUrl).get("/client/distinct-problem")
          ..reply(
            200,
            jsonEncode([
              "Verwarring en desorientatie",
              "Medicatiebeheer",
            ]),
          );

    await tester.pumpWidget(
      ProviderScope(
        child: PreferredOrientationWrapper(
          child: MaterialApp(
            home: const SelectionGuidePage(),
            navigatorObservers: [mockObserver],
          ),
        ),
      ),
    );

    await tester.pumpAndSettle(const Duration(seconds: 1));

    // Verify that we are on the page.
    expect(find.text('Welkom bij de keuzegids'), findsOneWidget);
    expect(probleeminterceptor.isDone, true);

    await tester.dragUntilVisible(
      find.text('Verwarring en desorientatie'),
      find.byKey(const Key("SelectionGuide | Care Needs List")),
      const Offset(0, 1), // delta to move
    );
    await tester.tap(find.text('Verwarring en desorientatie'));
    expect(find.text('Verwarring en desorientatie'), findsOneWidget);
  });

  testWidgets('Unit Test - selection guide exit test',
      (WidgetTester tester) async {
    // Create a mock navigator observer
    final mockObserver = MockNavigatorObserver();

    await tester.pumpWidget(
      ProviderScope(
        child: PreferredOrientationWrapper(
          child: MaterialApp(
            home: const SelectionGuidePage(),
            navigatorObservers: [mockObserver],
          ),
        ),
      ),
    );

    // Verify that on the selection guide page.
    expect(find.text('Welkom bij de keuzegids'), findsOneWidget);

    final exitButton = find.byKey(const Key("exitButton"));
    expect(exitButton, findsOneWidget);

    // in test not vissible
    await tester.dragUntilVisible(
      exitButton,
      find.byType(SingleChildScrollView),
      const Offset(0, 50), // delta to move
    );

    await tester.tap(exitButton);

    await tester.pumpAndSettle(const Duration(seconds: 2));

    // Verify that on the home page.
    expect(find.text('Welcome'), findsOneWidget);
  });
}
