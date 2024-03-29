import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:zorgtechnologieapp/providers/logging_provider/logging_provider.dart';

import '../handlers/data_api_handler.dart';
import '../handlers/responsive_layout_handler.dart';
import '../widgets/futurebuilder.dart';
import 'selection_guide.dart';

class ClientOverview extends ConsumerWidget {
  const ClientOverview({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final logger = ref.watch(loggingProvider);

    return Scaffold(
      backgroundColor: Colors.indigo[50],
      appBar: AppBar(
        backgroundColor: Colors.blue,
        title: Text(
          "Clienten Overzicht", // App bar title
          style: SizeScaler.getResponsiveTextStyle(
              context,
              16,
              FontWeight.bold,
              Colors
                  .white), // Define the text style using SizeScaler for responsive text sizing
        ),
      ),
      body: Padding(
        padding: const EdgeInsets.all(50.0),
        child: Column(
          children: [
            Expanded(
              child: FutureDataWidget(
                fetchData: DataAPI(logger: logger).providedClient(
                    "8b5f14d4-dac9-4c44-a9b6-6e2e8f15fd4b"), // Fetch client data using DataAPI
                widgetType: FutureWidgetType
                    .selectableList, // Display a selectable list of clients
                dataType:
                    FutureDataType.clients, // Specify the data type as clients
              ),
            ),

            // Button for adding a new client
            FloatingActionButton.extended(
              onPressed: () {
                Navigator.of(context).push(
                  MaterialPageRoute(
                    builder: (context) => const SelectionGuidePage(),
                  ),
                );
              },
              icon: const Icon(Icons.add,
                  size: 50.0), // Add icon to the floating action button
              label: Text(
                'Nieuwe Client', // Button label
                style: SizeScaler.getResponsiveTextStyle(
                    context,
                    16,
                    FontWeight.bold,
                    Colors
                        .black), // Define the text style using SizeScaler for responsive text sizing
              ),
            ),
          ],
        ),
      ),
    );
  }
}
