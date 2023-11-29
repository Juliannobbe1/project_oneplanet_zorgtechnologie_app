import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:mockito/mockito.dart';
import 'package:zorgtechnologieapp/main.dart';
import 'package:zorgtechnologieapp/pages/client_overview_page.dart';

class MockNavigatorObserver extends Mock implements NavigatorObserver {}

//! Ignore Data fetching log errors, this test is pure testing going of one page to another

void main() {
  testWidgets(
      'Clicking new recommmendation button navigates to selection guide test',
      (WidgetTester tester) async {
    // Create a mock navigator observer
    final mockObserver = MockNavigatorObserver();

    // Build our app and trigger a frame.
    await tester.pumpWidget(
      ProviderScope(
        child: PreferredOrientationWrapper(
          child: MaterialApp(
            home: const ClientOverview(),
            navigatorObservers: [mockObserver],
          ),
        ),
      ),
    );

    // Verify that we are on the client page.
    expect(find.text('Clienten Overzicht'), findsOneWidget);

    // Tap the nieuwe client button.
    await tester.tap(find.text('Nieuwe Client'));
    await tester.pumpAndSettle();

    // Use pumpAndSettle to ensure that the navigation has completed.
    // You might need to adjust the duration based on your app's navigation speed.
    await tester.pumpAndSettle(const Duration(seconds: 1));

    // Verify that we are on the keuze gids page.
    expect(find.text('Welkom bij de keuzegids'), findsOneWidget);
  });
}
