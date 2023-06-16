import 'package:flutter/material.dart';

import '../handlers/data_api_handler.dart';
import '../handlers/responsive_layout_handler.dart';
import '../widgets/futurebuilder.dart';
import 'selection_guide.dart';

class ClientOverview extends StatelessWidget {
  const ClientOverview({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(
          "Clienten Overzicht ",
          style: SizeScaler.getResponsiveTextStyle(
              context, 16, FontWeight.bold, Colors.white),
        ),
      ),
      body: Padding(
        padding: const EdgeInsets.all(50.0),
        child: Column(
          children: [
            Expanded(
              child: FutureDataWidget(
                fetchData: DataAPI().providedClient(1),
                widgetType: FutureWidgetType.selectableList,
                dataType: FutureDataType.clients,
              ),
            ),
            FloatingActionButton.extended(
              onPressed: () {
                Navigator.of(context).push(
                  MaterialPageRoute(
                    builder: (context) => const SelectionGuidePage(),
                  ),
                );
              },
              icon: const Icon(Icons.add, size: 50.0),
              label: Text(
                'Nieuwe Client',
                style: SizeScaler.getResponsiveTextStyle(
                    context, 16, FontWeight.bold, Colors.white),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
