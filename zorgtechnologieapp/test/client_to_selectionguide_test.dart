import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:zorgtechnologieapp/main.dart';
import 'package:zorgtechnologieapp/pages/client_overview_page.dart';

void main() {
  testWidgets('Unittest - navigation to selection guide',
      (WidgetTester tester) async {
    // Build app and trigger a frame.
    await tester.pumpWidget(
      const ProviderScope(
        child: PreferredOrientationWrapper(
          child: MaterialApp(
            home: ClientOverview(),
          ),
        ),
      ),
    );

    // Verify that we are on the client page.
    expect(find.text('Clienten Overzicht'), findsOneWidget);

    // Tap the nieuwe client button.
    await tester.tap(find.text('Nieuwe Client'));
    await tester.pumpAndSettle();

    // Verify that we are on the keuze gids page.
    expect(find.text('Welkom bij de keuzegids'), findsOneWidget);
  });
}
