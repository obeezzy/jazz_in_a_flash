import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';

class PianoKeyboard extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Text('C E G B\u266D',
        style: GoogleFonts.lato(
          textStyle: Theme.of(context).textTheme.display1,
          fontSize: 36,
        ));
  }
}
