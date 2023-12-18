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

  testWidgets('Integrationtest - clientoverview screen',
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

    expect(clientinterceptor.isDone, true);
  });
}
