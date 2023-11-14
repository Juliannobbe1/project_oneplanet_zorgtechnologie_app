import 'package:logger/logger.dart';
import 'package:riverpod_annotation/riverpod_annotation.dart';

part 'logging_provider.g.dart';

@riverpod
Logger logging(LoggingRef ref) {
  return Logger(level: Level.info);
}
