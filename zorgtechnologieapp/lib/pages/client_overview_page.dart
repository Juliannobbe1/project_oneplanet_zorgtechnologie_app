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
      floatingActionButtonLocation: FloatingActionButtonLocation.centerFloat,
      floatingActionButton: SizedBox(
        height: 100,
        width: 250,
        child: FloatingActionButton(
          shape: const RoundedRectangleBorder(
              borderRadius: BorderRadius.all(Radius.circular(10))),
          onPressed: () {
            Navigator.of(context).push(
              MaterialPageRoute(
                builder: (context) => const SelectionGuidePage(),
              ),
            );
          },
          child: Center(
              child: Text(
            "Nieuwe client",
            style: SizeScaler.getResponsiveTextStyle(
                context, 18, FontWeight.bold, Colors.white),
          )),
        ),
      ),
      appBar: AppBar(),
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
          ],
        ),
      ),
    );
  }
}
