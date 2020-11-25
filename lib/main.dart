import 'package:flutter/material.dart';
import 'src/routes/flash_card_page.dart';

void main() {
  runApp(JazzApp());
}

class JazzApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Jazz In A Flash',
      theme: ThemeData(
        primarySwatch: Colors.green,
        visualDensity: VisualDensity.adaptivePlatformDensity,
      ),
      home: FlashCardPage(),
    );
  }
}
