import 'dart:io';
import 'package:shelf/shelf.dart';
import 'package:shelf/shelf_io.dart';

void main() async {
  final handler = const Pipeline().addHandler((Request request) {
    return Response.ok('RODA Dart Backend is alive!');
  });

  final server = await serve(handler, InternetAddress.anyIPv4, 8080);
  print('Server running on localhost:${server.port}');
}
