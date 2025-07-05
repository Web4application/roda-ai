import 'dart:io';
import 'dart:convert';

import 'package:shelf/shelf.dart';
import 'package:shelf/shelf_io.dart';
import 'package:shelf_router/shelf_router.dart';
import 'package:shelf_cors_headers/shelf_cors_headers.dart';

// AI prompt handler
Response _askHandler(Request request) async {
  final body = await request.readAsString();
  final data = jsonDecode(body);

  final prompt = data['prompt'] ?? 'No prompt provided';
  final reply = '🧠 Dart RODA says: "$prompt" received successfully.';

  return Response.ok(jsonEncode({'reply': reply}), headers: {
    'Content-Type': 'application/json'
  });
}

void main() async {
  final router = Router();

  router.post('/ask', _askHandler);

  final handler = const Pipeline()
      .addMiddleware(logRequests())
      .addMiddleware(corsHeaders())
      .addHandler(router);

  final server = await serve(handler, InternetAddress.anyIPv4, 8080);
  print('✅ RODA Dart backend listening on port \${server.port}');
}
