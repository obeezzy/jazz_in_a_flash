import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';

class ChordNameView extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Text('Cmaj7',
        style: GoogleFonts.lato(
          textStyle: Theme.of(context).textTheme.display1,
          fontSize: 48,
        ));
  }
}
