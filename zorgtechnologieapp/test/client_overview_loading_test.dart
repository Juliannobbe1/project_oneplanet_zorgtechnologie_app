import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:mockito/mockito.dart';
import 'package:zorgtechnologieapp/pages/home_page.dart';

class MockNavigatorObserver extends Mock implements NavigatorObserver {}

//! Ignore Data fetching errors, this test is pure testing the loading time of one page to another

void main() {
  testWidgets(
      'Clicking Keuzegids button navigates to ClientOverview performance test',
      (WidgetTester tester) async {
    // Create a mock navigator observer
    final mockObserver = MockNavigatorObserver();

    // Build our app and trigger a frame.
    await tester.pumpWidget(
      ProviderScope(
        child: MaterialApp(
          home: const HomePage(),
          navigatorObservers: [mockObserver],
        ),
      ),
    );

    // Verify that we are on the home page.
    expect(find.text('Welcome'), findsOneWidget);

    // Tap the Keuzegids button.
    final startTime = DateTime.now();
    await tester.tap(find.text('Keuzegids'));
    await tester.pumpAndSettle();

    // Use pumpAndSettle to ensure that the navigation has completed.
    // You might need to adjust the duration based on your app's navigation speed.
    await tester.pumpAndSettle(const Duration(seconds: 1));

    // Verify that we are on the Clienten Overzicht page.
    expect(find.text('Clienten Overzicht'), findsOneWidget);

    // Calculate the loading time
    final loadingTime = DateTime.now().difference(startTime).inMilliseconds;

    // Ensure that the loading time is faster than 1289 seconds.
    expect(loadingTime, lessThan(1000));
  });
}
