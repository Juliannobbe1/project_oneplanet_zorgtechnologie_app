import 'package:flutter/material.dart';

import '../handlers/data_api_handler.dart';
import '../widgets/futurebuilder.dart';

class SandBox extends StatelessWidget {
  const SandBox({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: FutureDataWidget(
        fetchData: DataAPI().newestProducts,
        widgetType: FutureWidgetType.gridView,
        countRow: 1,
      ),
    );
  }
}
