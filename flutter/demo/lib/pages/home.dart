import 'package:flutter/material.dart';
import 'package:demo/widgets/cat_card_list.dart';

class MyHomePage extends StatefulWidget {
  MyHomePage({Key? key, required this.title}) : super(key: key);

  final String title;

  @override
  _MyHomePageState createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  double initialX = 0;
  double distance = 0;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
        appBar: AppBar(
          title: Text(widget.title),
        ),
        body: GestureDetector(
          behavior: HitTestBehavior.opaque,
          onHorizontalDragStart: (DragStartDetails e) {
            initialX = e.globalPosition.dx;
            //print(e.velocity);
          },
          onHorizontalDragUpdate: (DragUpdateDetails e) {
            distance = e.globalPosition.dx - initialX;
            //print(e.velocity);
          },
          onHorizontalDragEnd: (DragEndDetails e) {
            if (distance > 40.0) {
              Navigator.of(context).pushNamed('about');
            }
          },
          child: Container(
            // Center is a layout widget. It takes a single child and positions it
            // in the middle of the parent.
            child: Center(
              child: CatCardList(),
            ),
          ),
        ));
  }
}
