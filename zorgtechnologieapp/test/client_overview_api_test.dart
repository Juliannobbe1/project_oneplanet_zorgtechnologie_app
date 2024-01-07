import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:nock/nock.dart';
import 'package:zorgtechnologieapp/handlers/data_api_handler.dart';
import 'package:zorgtechnologieapp/main.dart';
import 'package:zorgtechnologieapp/pages/client_overview_page.dart';

void main() {
  setUpAll(() {
    nock.init();
  });

  setUp(() {
    nock.cleanAll();
  });

  testWidgets('Unittest - clientoverview screen', (WidgetTester tester) async {
    final clientinterceptor = nock(kApiBaseUrl)
        .get("/client/wordtverzorgd/8b5f14d4-dac9-4c44-a9b6-6e2e8f15fd4b")
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

    expect(clientinterceptor.isDone, true);
    await tester.pumpAndSettle();

    expect(find.text("Probleem: Veiligheid en toezicht"), findsOneWidget);
  });
}
